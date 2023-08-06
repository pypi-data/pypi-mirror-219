import os

from ebook_converter.customize.conversion import OutputFormatPlugin, \
    OptionRecommendation
from ebook_converter.ebooks.pdb import PDBError, get_writer, ALL_FORMAT_WRITERS


__license__ = 'GPL 3'
__copyright__ = '2009, John Schember <john@nachtimwald.com>'
__docformat__ = 'restructuredtext en'


class PDBOutput(OutputFormatPlugin):

    name = 'PDB Output'
    author = 'John Schember'
    file_type = 'pdb'
    commit_name = 'pdb_output'
    ui_data = {'formats': tuple(ALL_FORMAT_WRITERS)}

    options = {
        OptionRecommendation(name='format', recommended_value='doc',
            level=OptionRecommendation.LOW,
            short_switch='f', choices=list(ALL_FORMAT_WRITERS),
            help='Format to use inside the pdb container. Choices are: %s' %
                 sorted(ALL_FORMAT_WRITERS)),
        OptionRecommendation(name='pdb_output_encoding', recommended_value='cp1252',
            level=OptionRecommendation.LOW,
            help='Specify the character encoding of the output document. '
                 'The default is cp1252. Note: This option is not honored by '
                 'all formats.'),
        OptionRecommendation(name='inline_toc',
            recommended_value=False, level=OptionRecommendation.LOW,
            help='Add Table of Contents to beginning of the book.'),
    }

    def convert(self, oeb_book, output_path, input_plugin, opts, log):
        close = False
        if not hasattr(output_path, 'write'):
            close = True
            if not os.path.exists(os.path.dirname(output_path)) and os.path.dirname(output_path):
                os.makedirs(os.path.dirname(output_path))
            out_stream = open(output_path, 'wb')
        else:
            out_stream = output_path

        Writer = get_writer(opts.format)

        if Writer is None:
            raise PDBError('No writer available for format %s.' % format)

        setattr(opts, 'max_line_length', 0)
        setattr(opts, 'force_max_line_length', False)

        writer = Writer(opts, log)

        out_stream.seek(0)
        out_stream.truncate()

        writer.write_content(oeb_book, out_stream, oeb_book.metadata)

        if close:
            out_stream.close()
