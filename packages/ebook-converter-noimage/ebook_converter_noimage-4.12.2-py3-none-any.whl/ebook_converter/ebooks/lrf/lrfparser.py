import array
import itertools
import re
import sys

from ebook_converter.utils.config import OptionParser
from ebook_converter.utils.filenames import ascii_filename
from ebook_converter.ebooks.lrf.meta import LRFMetaFile
from ebook_converter.ebooks.lrf.objects import get_object, PageTree, \
        StyleObject, Font, Text, TOCObject, BookAttr, ruby_tags


class LRFDocument(LRFMetaFile):

    class temp(object):
        pass

    def __init__(self, stream):
        LRFMetaFile.__init__(self, stream)
        self.scramble_key = self.xor_key
        self.page_trees = []
        self.font_map = {}
        self.image_map = {}
        self.toc = ''
        self.keep_parsing = True

    def parse(self):
        self._parse_objects()
        self.metadata = LRFDocument.temp()
        for a in ('title', 'title_reading', 'author', 'author_reading',
                  'book_id', 'classification', 'free_text', 'publisher',
                  'label', 'category'):
            setattr(self.metadata, a, getattr(self, a))
        self.doc_info = LRFDocument.temp()
        for a in ('thumbnail', 'language', 'creator', 'producer', 'page'):
            setattr(self.doc_info, a, getattr(self, a))
        self.doc_info.thumbnail_extension = self.thumbail_extension()
        self.device_info = LRFDocument.temp()
        for a in ('dpi', 'width', 'height'):
            setattr(self.device_info, a, getattr(self, a))

    def _parse_objects(self):
        self.objects = {}
        self._file.seek(self.object_index_offset)
        obj_array = array.array("I", self._file.read(4 * 4 *
                                                     self.number_of_objects))
        if sys.byteorder == 'big':
            obj_array.byteswap()

        for i in range(self.number_of_objects):
            if not self.keep_parsing:
                break
            objid, objoff, objsize = obj_array[i*4:i*4+3]
            self._parse_object(objid, objoff, objsize)
        for obj in self.objects.values():
            if not self.keep_parsing:
                break
            if hasattr(obj, 'initialize'):
                obj.initialize()

    def _parse_object(self, objid, objoff, objsize):
        obj = get_object(self, self._file, objid, objoff, objsize,
                         self.scramble_key)
        self.objects[objid] = obj
        if isinstance(obj, PageTree):
            self.page_trees.append(obj)
        elif isinstance(obj, TOCObject):
            self.toc = obj
        elif isinstance(obj, BookAttr):
            self.ruby_tags = {}
            for h in ruby_tags.values():
                attr = h[0]
                if hasattr(obj, attr):
                    self.ruby_tags[attr] = getattr(obj, attr)

    def __iter__(self):
        for pt in self.page_trees:
            yield pt

    def write_files(self):
        for obj in itertools.chain(self.image_map.values(),
                                   self.font_map.values()):
            with open(obj.file, 'wb') as f:
                f.write(obj.stream)

    def to_xml(self, write_files=True):
        bookinfo = ('<BookInformation>\n<Info version="1.1">\n<BookInfo>\n'
                    '<Title reading="%s">%s</Title>\n'
                    '<Author reading="%s">%s</Author>\n'
                    '<BookID>%s</BookID>\n'
                    '<Publisher reading="">%s</Publisher>\n'
                    '<Label reading="">%s</Label>\n'
                    '<Category reading="">%s</Category>\n'
                    '<Classification reading="">%s</Classification>\n'
                    '<FreeText reading="">%s</FreeText>\n'
                    '</BookInfo>\n<DocInfo>\n' %
                    (self.metadata.title_reading, self.metadata.title,
                     self.metadata.author_reading, self.metadata.author,
                     self.metadata.book_id, self.metadata.publisher,
                     self.metadata.label, self.metadata.category,
                     self.metadata.classification, self.metadata.free_text))
        th = self.doc_info.thumbnail
        if th:
            prefix = ascii_filename(self.metadata.title)
            bookinfo += ('<CThumbnail file="%s" />\n' %
                         (prefix + '_thumbnail.' +
                          self.doc_info.thumbnail_extension))
            if write_files:
                with open(prefix + '_thumbnail.' +
                          self.doc_info.thumbnail_extension, 'wb') as f:
                    f.write(th)
        bookinfo += ('<Language reading="">%s</Language>\n'
                     '<Creator reading="">%s</Creator>\n'
                     '<Producer reading="">%s</Producer>\n'
                     '<SumPage>%s</SumPage>\n'
                     '</DocInfo>\n</Info>\n%s</BookInformation>\n' %
                     (self.doc_info.language, self.doc_info.creator,
                      self.doc_info.producer, self.doc_info.page, self.toc))
        pages = ''
        done_main = False
        pt_id = -1
        for page_tree in self:
            if not done_main:
                done_main = True
                pages += '<Main>\n'
                close = '</Main>\n'
                pt_id = page_tree.id
            else:
                pages += '<PageTree objid="%d">\n' % (page_tree.id,)
                close = '</PageTree>\n'
            for page in page_tree:
                pages += str(page)
            pages += close
        traversed_objects = [int(i) for i in re.findall(r'objid="(\w+)"',
                                                        pages)] + [pt_id]

        objects = '\n<Objects>\n'
        styles = '\n<Style>\n'
        for obj in self.objects:
            obj = self.objects[obj]
            if obj.id in traversed_objects:
                continue
            if isinstance(obj, (Font, Text, TOCObject)):
                continue
            if isinstance(obj, StyleObject):
                styles += str(obj)
            else:
                objects += str(obj)
        styles += '</Style>\n'
        objects += '</Objects>\n'
        if write_files:
            self.write_files()
        return ('<BBeBXylog version="1.0">\n' + bookinfo + pages + styles +
                objects + '</BBeBXylog>')


def option_parser():
    parser = OptionParser(usage='%prog book.lrf\nConvert an LRF file into '
                          'an LRS (XML UTF-8 encoded) file')
    parser.add_option('--output', '-o', default=None,
                      help='Output LRS file', dest='out')
    parser.add_option('--dont-output-resources', default=True,
                      action='store_false',
                      help='Do not save embedded image and font files to '
                      'disk', dest='output_resources')
    parser.add_option('--verbose', default=False, action='store_true',
                      dest='verbose', help='Be more verbose')
    return parser
