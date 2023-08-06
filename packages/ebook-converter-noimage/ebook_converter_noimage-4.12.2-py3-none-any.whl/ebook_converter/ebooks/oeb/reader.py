"""
Container-/OPF-based input OEBBook reader.
"""
import collections
import copy
import io
import mimetypes
import os
import re
import sys
import urllib.parse
import uuid

from lxml import etree

from ebook_converter import constants as const
from ebook_converter.ebooks.oeb import base
from ebook_converter.ebooks.oeb import parse_utils
from ebook_converter.ebooks.metadata import opf2 as opf_meta
from ebook_converter.ebooks.oeb.writer import OEBWriter
from ebook_converter.utils.xml_parse import safe_xml_fromstring
from ebook_converter.utils.cleantext import clean_xml_chars
from ebook_converter.utils.localization import get_lang
from ebook_converter.ptempfile import TemporaryDirectory
from ebook_converter.constants_old import __appname__, __version__
from ebook_converter.utils import entities
from ebook_converter import polyglot


class OEBReader(object):
    """Read an OEBPS 1.x or OPF/OPS 2.0 file collection."""

    COVER_SVG_XP = base.XPath('h:body//svg:svg[position() = 1]')
    COVER_OBJECT_XP = base.XPath('h:body//h:object[@data][position() = 1]')

    Container = base.DirContainer
    """Container type used to access book files.  Override in sub-classes."""

    DEFAULT_PROFILE = 'PRS505'
    """Default renderer profile for content read with this Reader."""

    TRANSFORMS = []
    """List of transforms to apply to content read with this Reader."""

    @classmethod
    def config(cls, cfg):
        """Add any book-reading options to the :class:`Config` object
        :param:`cfg`.
        """
        return

    @classmethod
    def generate(cls, opts):
        """Generate a Reader instance from command-line options."""
        return cls()

    def __call__(self, oeb, path):
        """Read the book at :param:`path` into the :class:`OEBBook` object
        :param:`oeb`.
        """
        self.oeb = oeb
        self.logger = self.log = oeb.logger
        oeb.container = self.Container(path, self.logger)
        oeb.container.log = oeb.log
        opf = self._read_opf()
        self._all_from_opf(opf)
        return oeb

    def _clean_opf(self, opf):
        nsmap = {}
        for elem in opf.iter(tag=etree.Element):
            nsmap.update(elem.nsmap)
        for elem in opf.iter(tag=etree.Element):
            if (parse_utils.namespace(elem.tag) in ('', const.OPF1_NS) and
                    ':' not in parse_utils.barename(elem.tag)):
                elem.tag = base.tag('opf', parse_utils.barename(elem.tag))
        nsmap.update(const.OPF2_NSMAP)
        attrib = dict(opf.attrib)
        nroot = etree.Element(base.tag('opf', 'package'),
                              nsmap={None: const.OPF2_NS}, attrib=attrib)
        metadata = etree.SubElement(nroot, base.tag('opf', 'metadata'),
                                    nsmap=nsmap)
        ignored = (base.tag('opf', 'dc-metadata'), base.tag('opf', 'x-metadata'))
        for elem in base.xpath(opf, 'o2:metadata//*'):
            if elem.tag in ignored:
                continue
            if parse_utils.namespace(elem.tag) in const.DC_NSES:
                tag = parse_utils.barename(elem.tag).lower()
                elem.tag = '{%s}%s' % (const.DC11_NS, tag)
            if elem.tag.startswith('dc:'):
                tag = elem.tag.partition(':')[-1].lower()
                elem.tag = '{%s}%s' % (const.DC11_NS, tag)
            metadata.append(elem)
        for element in base.xpath(opf, 'o2:metadata//o2:meta'):
            metadata.append(element)
        for tag in ('o2:manifest', 'o2:spine', 'o2:tours', 'o2:guide'):
            for element in base.xpath(opf, tag):
                nroot.append(element)
        return nroot

    def _read_opf(self):
        data = self.oeb.container.read(None)
        data = self.oeb.decode(data)
        data = base.XMLDECL_RE.sub('', data)
        data = re.sub(r'http://openebook.org/namespaces/oeb-package/1.0(/*)',
                      const.OPF1_NS, data)
        try:
            opf = etree.fromstring(data)
        except etree.XMLSyntaxError:
            data = entities.xml_replace_entities(clean_xml_chars(data),
                                                 encoding=None)
            try:
                opf = etree.fromstring(data)
                self.logger.warning('OPF contains invalid HTML named entities')
            except etree.XMLSyntaxError:
                data = re.sub(r'(?is)<tours>.+</tours>', '', data)
                data = data.replace('<dc-metadata>',
                                    '<dc-metadata xmlns:dc="'
                                    'http://purl.org/metadata/dublin_core">')
                opf = etree.fromstring(data)
                self.logger.warning('OPF contains invalid tours section')

        ns = parse_utils.namespace(opf.tag)
        if ns not in ('', const.OPF1_NS, const.OPF2_NS):
            raise base.OEBError('Invalid namespace %r for OPF document' % ns)
        opf = self._clean_opf(opf)
        return opf

    def _metadata_from_opf(self, opf):
        from ebook_converter.ebooks.metadata.opf2 import OPF
        from ebook_converter.ebooks.oeb.transforms.metadata import \
            meta_info_to_oeb_metadata
        stream = io.BytesIO(etree.tostring(opf, xml_declaration=True,
                                           encoding='utf-8'))
        o = OPF(stream)
        pwm = o.primary_writing_mode
        if pwm:
            self.oeb.metadata.primary_writing_mode = pwm
        mi = o.to_book_metadata()
        if not mi.language:
            mi.language = get_lang().replace('_', '-')
        self.oeb.metadata.add('language', mi.language)
        if not mi.book_producer:
            mi.book_producer = ('%(a)s (%(v)s) [http://%(a)s-ebook.com]' %
                                dict(a=__appname__, v=__version__))
        meta_info_to_oeb_metadata(mi, self.oeb.metadata, self.logger)
        m = self.oeb.metadata
        m.add('identifier', str(uuid.uuid4()), id='uuid_id', scheme='uuid')
        self.oeb.uid = self.oeb.metadata.identifier[-1]
        if not m.title:
            m.add('title', self.oeb.translate('Unknown'))
        has_aut = False
        for x in m.creator:
            if getattr(x, 'role', '').lower() in ('', 'aut'):
                has_aut = True
                break
        if not has_aut:
            m.add('creator', self.oeb.translate('Unknown'), role='aut')

    def _manifest_prune_invalid(self):
        '''
        Remove items from manifest that contain invalid data. This prevents
        catastrophic conversion failure, when a few files contain corrupted
        data.
        '''
        bad = []
        check = base.OEB_DOCS.union(base.OEB_STYLES)
        for item in list(self.oeb.manifest.values()):
            if item.media_type in check:
                try:
                    item.data
                except KeyboardInterrupt:
                    raise
                except Exception:
                    self.logger.exception('Failed to parse content in %s',
                                          item.href)
                    bad.append(item)
                    self.oeb.manifest.remove(item)
        return bad

    def _manifest_add_missing(self, invalid):
        import css_parser
        manifest = self.oeb.manifest
        known = set(manifest.hrefs)
        unchecked = set(manifest.values())
        cdoc = base.OEB_DOCS | base.OEB_STYLES
        invalid = set()
        while unchecked:
            new = set()
            for item in unchecked:
                data = None
                if (item.media_type in cdoc or
                        item.media_type[-4:] in ('/xml', '+xml')):
                    try:
                        data = item.data
                    except Exception:
                        self.oeb.log.exception('Failed to read from manifest '
                                               'entry with id: %s, ignoring',
                                               item.id)
                        invalid.add(item)
                        continue
                if data is None:
                    continue

                if (item.media_type in base.OEB_DOCS or
                        item.media_type[-4:] in ('/xml', '+xml')):
                    hrefs = [r[2] for r in base.iterlinks(data)]
                    for href in hrefs:
                        if isinstance(href, bytes):
                            href = href.decode('utf-8')
                        href, _ = urllib.parse.urldefrag(href)
                        if not href:
                            continue
                        try:
                            href = item.abshref(base.urlnormalize(href))
                            scheme = urllib.parse.urlparse(href).scheme
                        except Exception:
                            self.oeb.log.exception('Skipping invalid href: '
                                                   '%r', href)
                            continue
                        if not scheme and href not in known:
                            new.add(href)
                elif item.media_type in base.OEB_STYLES:
                    try:
                        urls = list(css_parser.getUrls(data))
                    except Exception:
                        urls = []
                    for url in urls:
                        href, _ = urllib.parse.urldefrag(url)
                        href = item.abshref(base.urlnormalize(href))
                        scheme = urllib.parse.urlparse(href).scheme
                        if not scheme and href not in known:
                            new.add(href)
            unchecked.clear()
            warned = set()
            for href in new:
                known.add(href)
                is_invalid = False
                for item in invalid:
                    if href == item.abshref(base.urlnormalize(href)):
                        is_invalid = True
                        break
                if is_invalid:
                    continue
                if not self.oeb.container.exists(href):
                    if href not in warned:
                        self.logger.warning('Referenced file %r not found',
                                            href)
                        warned.add(href)
                    continue
                if href not in warned:
                    self.logger.warning('Referenced file %r not in manifest',
                                        href)
                    warned.add(href)
                id, _ = manifest.generate(id='added')
                guessed = mimetypes.guess_type(href)[0]
                media_type = guessed or base.BINARY_MIME
                added = manifest.add(id, href, media_type)
                unchecked.add(added)

            for item in invalid:
                self.oeb.manifest.remove(item)

    def _manifest_from_opf(self, opf):
        manifest = self.oeb.manifest
        for elem in base.xpath(opf, '/o2:package/o2:manifest/o2:item'):
            id = elem.get('id')
            href = elem.get('href')
            media_type = elem.get('media-type', None)
            if media_type is None:
                media_type = elem.get('mediatype', None)
            if not media_type or media_type == 'text/xml':
                guessed = mimetypes.guess_type(href)[0]
                media_type = guessed or media_type or base.BINARY_MIME
            if hasattr(media_type, 'lower'):
                media_type = media_type.lower()
            fallback = elem.get('fallback')
            if href in manifest.hrefs:
                self.logger.warning('Duplicate manifest entry for %r', href)
                continue
            if not self.oeb.container.exists(href):
                self.logger.warning('Manifest item %r not found', href)
                continue
            if id in manifest.ids:
                self.logger.warning('Duplicate manifest id %r', id)
                id, href = manifest.generate(id, href)
            manifest.add(id, href, media_type, fallback)
        invalid = self._manifest_prune_invalid()
        self._manifest_add_missing(invalid)

    def _spine_add_extra(self):
        manifest = self.oeb.manifest
        spine = self.oeb.spine
        unchecked = set(spine)
        selector = base.XPath('h:body//h:a/@href')
        extras = set()
        while unchecked:
            new = set()
            for item in unchecked:
                if item.media_type not in base.OEB_DOCS:
                    # TODO: handle fallback chains
                    continue
                for href in selector(item.data):
                    href, _ = urllib.parse.urldefrag(href)
                    if not href:
                        continue
                    try:
                        href = item.abshref(base.urlnormalize(href))
                    except ValueError:  # Malformed URL
                        continue
                    if href not in manifest.hrefs:
                        continue
                    found = manifest.hrefs[href]
                    if found.media_type not in base.OEB_DOCS or \
                       found in spine or found in extras:
                        continue
                    new.add(found)
            extras.update(new)
            unchecked = new
        version = int(self.oeb.version[0])
        removed_items_to_ignore = getattr(self.oeb, 'removed_items_to_ignore',
                                          ())
        for item in sorted(extras):
            if item.href in removed_items_to_ignore:
                continue
            if version >= 2:
                self.logger.warning('Spine-referenced file %r not in spine',
                                    item.href)
            spine.add(item, linear=False)

    def _spine_from_opf(self, opf):
        spine = self.oeb.spine
        manifest = self.oeb.manifest
        for elem in base.xpath(opf, '/o2:package/o2:spine/o2:itemref'):
            idref = elem.get('idref')
            if idref not in manifest.ids:
                self.logger.warning('Spine item %r not found', idref)
                continue
            item = manifest.ids[idref]
            if (item.media_type.lower() in base.OEB_DOCS and
                    hasattr(item.data, 'xpath') and not
                    getattr(item.data, 'tag', '').endswith('}ncx')):
                spine.add(item, elem.get('linear'))
            else:
                if (hasattr(item.data, 'tag') and
                        item.data.tag and item.data.tag.endswith('}html')):
                    item.media_type = base.XHTML_MIME
                    spine.add(item, elem.get('linear'))
                else:
                    self.oeb.log.warning('The item %s is not a XML document.'
                                         ' Removing it from spine.', item.href)
        if len(spine) == 0:
            raise base.OEBError("Spine is empty")
        self._spine_add_extra()
        for val in base.xpath(opf,
                         '/o2:package/o2:spine/@page-progression-direction'):
            if val in {'ltr', 'rtl'}:
                spine.page_progression_direction = val

    def _guide_from_opf(self, opf):
        guide = self.oeb.guide
        manifest = self.oeb.manifest
        for elem in base.xpath(opf, '/o2:package/o2:guide/o2:reference'):
            ref_href = elem.get('href')
            path = base.urlnormalize(urllib.parse.urldefrag(ref_href)[0])
            if path not in manifest.hrefs:
                corrected_href = None
                for href in manifest.hrefs:
                    if href.lower() == path.lower():
                        corrected_href = href
                        break
                if corrected_href is None:
                    self.logger.warning('Guide reference %r not found',
                                        ref_href)
                    continue
                ref_href = corrected_href
            typ = elem.get('type')
            if typ not in guide:
                guide.add(typ, elem.get('title'), ref_href)

    def _find_ncx(self, opf):
        result = base.xpath(opf, '/o2:package/o2:spine/@toc')
        if result:
            id = result[0]
            if id not in self.oeb.manifest.ids:
                return None
            item = self.oeb.manifest.ids[id]
            self.oeb.manifest.remove(item)
            return item
        for item in self.oeb.manifest.values():
            if item.media_type == base.NCX_MIME:
                self.oeb.manifest.remove(item)
                return item
        return None

    def _toc_from_navpoint(self, item, toc, navpoint):
        children = base.xpath(navpoint, 'ncx:navPoint')
        for child in children:
            title = ''.join(base.xpath(child, 'ncx:navLabel/ncx:text/text()'))
            title = base.COLLAPSE_RE.sub(' ', title.strip())
            href = base.xpath(child, 'ncx:content/@src')
            if not title:
                self._toc_from_navpoint(item, toc, child)
                continue
            if (not href or not href[0]) and not base.xpath(child, 'ncx:navPoint'):
                # This node is useless
                continue
            if href and href[0]:
                href = item.abshref(base.urlnormalize(href[0]))
            else:
                href = ''
            path, _ = urllib.parse.urldefrag(href)
            if path and path not in self.oeb.manifest.hrefs:
                path = base.urlnormalize(path)
            if href and path not in self.oeb.manifest.hrefs:
                self.logger.warning('TOC reference %r not found', href)
                gc = base.xpath(child, 'ncx:navPoint')
                if not gc:
                    # This node is useless
                    continue
            id = child.get('id')
            klass = child.get('class', 'chapter')

            try:
                po = int(child.get('playOrder',
                                   self.oeb.toc.next_play_order()))
            except Exception:
                po = self.oeb.toc.next_play_order()

            authorElement = base.xpath(child,
                                  'descendant::calibre:meta[@name = "author"]')
            if authorElement:
                author = authorElement[0].text
            else:
                author = None

            descriptionElement = base.xpath(child,
                                       'descendant::calibre:meta[@name = '
                                       '"description"]')
            if descriptionElement:
                description = etree.tostring(descriptionElement[0],
                                             method='text',
                                             encoding='unicode').strip()
                if not description:
                    description = None
            else:
                description = None

            index_image = base.xpath(child,
                                'descendant::calibre:meta[@name = '
                                '"toc_thumbnail"]')
            toc_thumbnail = (index_image[0].text if index_image else None)
            if not toc_thumbnail or not toc_thumbnail.strip():
                toc_thumbnail = None

            node = toc.add(title, href, id=id, klass=klass,
                           play_order=po, description=description,
                           author=author, toc_thumbnail=toc_thumbnail)

            self._toc_from_navpoint(item, node, child)

    def _toc_from_ncx(self, item):
        if (item is None) or (item.data is None):
            return False
        self.log.debug('Reading TOC from NCX...')
        ncx = item.data
        title = ''.join(base.xpath(ncx, 'ncx:docTitle/ncx:text/text()'))
        title = base.COLLAPSE_RE.sub(' ', title.strip())
        title = title or str(self.oeb.metadata.title[0])
        toc = self.oeb.toc
        toc.title = title
        navmaps = base.xpath(ncx, 'ncx:navMap')
        for navmap in navmaps:
            self._toc_from_navpoint(item, toc, navmap)
        return True

    def _toc_from_tour(self, opf):
        result = base.xpath(opf, 'o2:tours/o2:tour')
        if not result:
            return False
        self.log.debug('Reading TOC from tour...')
        tour = result[0]
        toc = self.oeb.toc
        toc.title = tour.get('title')
        sites = base.xpath(tour, 'o2:site')
        for site in sites:
            title = site.get('title')
            href = site.get('href')
            if not title or not href:
                continue
            path, _ = urllib.parse.urldefrag(base.urlnormalize(href))
            if path not in self.oeb.manifest.hrefs:
                self.logger.warning('TOC reference %r not found', href)
                continue
            id = site.get('id')
            toc.add(title, href, id=id)
        return True

    def _toc_from_html(self, opf):
        if 'toc' not in self.oeb.guide:
            return False
        self.log.debug('Reading TOC from HTML...')
        itempath, frag = urllib.parse.urldefrag(self.oeb.guide['toc'].href)
        item = self.oeb.manifest.hrefs[itempath]
        html = item.data
        if frag:
            elems = base.xpath(html, './/*[@id="%s"]' % frag)
            if not elems:
                elems = base.xpath(html, './/*[@name="%s"]' % frag)
            elem = elems[0] if elems else html
            while elem != html and not base.xpath(elem, './/h:a[@href]'):
                elem = elem.getparent()
            html = elem
        titles = collections.defaultdict(list)
        order = []
        for anchor in base.xpath(html, './/h:a[@href]'):
            href = anchor.attrib['href']
            href = item.abshref(base.urlnormalize(href))
            path, frag = urllib.parse.urldefrag(href)
            if path not in self.oeb.manifest.hrefs:
                continue
            title = base.xml2text(anchor)
            title = base.COLLAPSE_RE.sub(' ', title.strip())
            if href not in titles:
                order.append(href)
            titles[href].append(title)
        toc = self.oeb.toc
        for href in order:
            toc.add(' '.join(titles[href]), href)
        return True

    def _toc_from_spine(self, opf):
        self.log.warning('Generating default TOC from spine...')
        toc = self.oeb.toc
        titles = []
        headers = []
        for item in self.oeb.spine:
            if not item.linear:
                continue
            html = item.data
            title = ''.join(base.xpath(html, '/h:html/h:head/h:title/text()'))
            title = base.COLLAPSE_RE.sub(' ', title.strip())
            if title:
                titles.append(title)
            headers.append('(unlabled)')
            for tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'strong'):
                expr = '/h:html/h:body//h:%s[position()=1]/text()'
                header = ''.join(base.xpath(html, expr % tag))
                header = base.COLLAPSE_RE.sub(' ', header.strip())
                if header:
                    headers[-1] = header
                    break
        use = titles
        if len(titles) > len(set(titles)):
            use = headers
        for title, item in zip(use, self.oeb.spine):
            if not item.linear:
                continue
            toc.add(title, item.href)
        return True

    def _toc_from_opf(self, opf, item):
        self.oeb.auto_generated_toc = False
        if self._toc_from_ncx(item):
            return
        # Prefer HTML to tour based TOC, since several LIT files
        # have good HTML TOCs but bad tour based TOCs
        if self._toc_from_html(opf):
            return
        if self._toc_from_tour(opf):
            return
        self._toc_from_spine(opf)
        self.oeb.auto_generated_toc = True

    def _pages_from_ncx(self, opf, item):
        if item is None:
            return False
        ncx = item.data
        if ncx is None:
            return False
        ptargets = base.xpath(ncx, 'ncx:pageList/ncx:pageTarget')
        if not ptargets:
            return False
        pages = self.oeb.pages
        for ptarget in ptargets:
            name = ''.join(base.xpath(ptarget, 'ncx:navLabel/ncx:text/text()'))
            name = base.COLLAPSE_RE.sub(' ', name.strip())
            href = base.xpath(ptarget, 'ncx:content/@src')
            if not href:
                continue
            href = item.abshref(base.urlnormalize(href[0]))
            id = ptarget.get('id')
            type = ptarget.get('type', 'normal')
            klass = ptarget.get('class')
            pages.add(name, href, type=type, id=id, klass=klass)
        return True

    def _find_page_map(self, opf):
        result = base.xpath(opf, '/o2:package/o2:spine/@page-map')
        if result:
            id = result[0]
            if id not in self.oeb.manifest.ids:
                return None
            item = self.oeb.manifest.ids[id]
            self.oeb.manifest.remove(item)
            return item
        for item in self.oeb.manifest.values():
            if item.media_type == base.PAGE_MAP_MIME:
                self.oeb.manifest.remove(item)
                return item
        return None

    def _pages_from_page_map(self, opf):
        item = self._find_page_map(opf)
        if item is None:
            return False
        pmap = item.data
        pages = self.oeb.pages
        for page in base.xpath(pmap, 'o2:page'):
            name = page.get('name', '')
            href = page.get('href')
            if not href:
                continue
            name = base.COLLAPSE_RE.sub(' ', name.strip())
            href = item.abshref(base.urlnormalize(href))
            type = 'normal'
            if not name:
                type = 'special'
            elif name.lower().strip('ivxlcdm') == '':
                type = 'front'
            pages.add(name, href, type=type)
        return True

    def _pages_from_opf(self, opf, item):
        if self._pages_from_ncx(opf, item):
            return
        if self._pages_from_page_map(opf):
            return
        return

    def _cover_from_html(self, hcover):
        from ebook_converter.ebooks import render_html_svg_workaround
        with TemporaryDirectory('_html_cover') as tdir:
            writer = OEBWriter()
            writer(self.oeb, tdir)
            path = os.path.join(tdir, polyglot.unquote(hcover.href))
            data = render_html_svg_workaround(path, self.logger)
            if not data:
                data = b''
        id, href = self.oeb.manifest.generate('cover', 'cover.jpg')
        item = self.oeb.manifest.add(id, href, base.JPEG_MIME, data=data)
        return item

    def _locate_cover_image(self):
        if self.oeb.metadata.cover:
            id = str(self.oeb.metadata.cover[0])
            item = self.oeb.manifest.ids.get(id, None)
            if item is not None and item.media_type in base.OEB_IMAGES:
                return item
            else:
                self.logger.warning('Invalid cover image @id %r', id)
        hcover = self.oeb.spine[0]
        if 'cover' in self.oeb.guide:
            href = self.oeb.guide['cover'].href
            item = self.oeb.manifest.hrefs[href]
            media_type = item.media_type
            if media_type in base.OEB_IMAGES:
                return item
            elif media_type in base.OEB_DOCS:
                hcover = item
        html = hcover.data
        if base.MS_COVER_TYPE in self.oeb.guide:
            href = self.oeb.guide[base.MS_COVER_TYPE].href
            item = self.oeb.manifest.hrefs.get(href, None)
            if item is not None and item.media_type in base.OEB_IMAGES:
                return item
        if self.COVER_SVG_XP(html):
            svg = copy.deepcopy(self.COVER_SVG_XP(html)[0])
            href = os.path.splitext(hcover.href)[0] + '.svg'
            id, href = self.oeb.manifest.generate(hcover.id, href)
            item = self.oeb.manifest.add(id, href, base.SVG_MIME, data=svg)
            return item
        if self.COVER_OBJECT_XP(html):
            object = self.COVER_OBJECT_XP(html)[0]
            href = hcover.abshref(object.get('data'))
            item = self.oeb.manifest.hrefs.get(href, None)
            if item is not None and item.media_type in base.OEB_IMAGES:
                return item
        return self._cover_from_html(hcover)

    def _ensure_cover_image(self):
        cover = self._locate_cover_image()
        if self.oeb.metadata.cover:
            self.oeb.metadata.cover[0].value = cover.id
            return
        self.oeb.metadata.add('cover', cover.id)

    def _manifest_remove_duplicates(self):
        seen = set()
        dups = set()
        for item in self.oeb.manifest:
            if item.href in seen:
                dups.add(item.href)
            seen.add(item.href)

        for href in dups:
            items = [x for x in self.oeb.manifest if x.href == href]
            for x in items:
                if x not in self.oeb.spine:
                    self.oeb.log.warning('Removing duplicate manifest item '
                                         'with id: %s', x.id)
                    self.oeb.manifest.remove_duplicate_item(x)

    def _all_from_opf(self, opf):
        self.oeb.version = opf.get('version', '1.2')
        self._metadata_from_opf(opf)
        self._manifest_from_opf(opf)
        self._spine_from_opf(opf)
        self._manifest_remove_duplicates()
        self._guide_from_opf(opf)
        item = self._find_ncx(opf)
        self._toc_from_opf(opf, item)
        self._pages_from_opf(opf, item)
        # self._ensure_cover_image()


def main(argv=sys.argv):
    reader = OEBReader()
    for arg in argv[1:]:
        oeb = reader(base.OEBBook(), arg)
        for name, doc in oeb.to_opf1().values():
            print(etree.tostring(doc, pretty_print=True))
        for name, doc in oeb.to_opf2(page_map=True).values():
            print(etree.tostring(doc, pretty_print=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
