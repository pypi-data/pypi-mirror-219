===============
Ebook converter
===============

This is impudent ripoff of the bits from `Calibre project`_, and is aimed only
for converter thing.

My motivation is to have only converter for ebooks run from commandline,
without all of those bells and whistles Calibre has, and with cleanest more
*pythonic* approach.


Requirements
------------

To build and run ebook converter, you'll need:

- Python 3.6 or newer
- `Liberation fonts`_
- setuptools
- ``pdftohtml``, ``pdfinfo`` and ``pdftoppm`` from `poppler`_ project for
  conversion from PDF available in ``$PATH``

No Python2 support. Even if Calibre probably still is able to run on Python2, I
do not have an intention to support it.


What's supported
----------------

To be able to perform some optimization and make converter more reliable and
easy to use, first I need to remove some of the features, which are totally not
crucial in my opinion, although they might be re-added later, like, for
instance there is no automatic language translations depending on the locale
settings.

First of all, I'm in the process of getting rid of strongly coupled things to
QT libraries, and GUI code as well. Second, I'll try to minimize all
modifications from third parties (external modules copied into Calibre project
for instance), and make a huge cleanup. I'm not sure if I find time and
strength for doing it completely, but I'll try.

Windows is not currently supported, because of the original spaghetti code.
This may change in the future, after cleanup of mentioned pasta would be
completed.

So called `Kindle periodical` format is not supported, since all we do care are
local files. If there would be downloaded periodical thing (using Calibre for
example), it would be treated as common book.


Input formats
~~~~~~~~~~~~~

Currently, I've tested following input formats:

- Microsoft Word 2007 and up (``docx``)
- EPUB, both v2 and v3 (``epub``)
- LibreOffice (``odt``)
- Pure text files (``txt``)
- Several PalmOS (``pdb``) readers support:

  - Plucker
  - Adobe Reader for PalmOS
  - eReader various formats
  - Weasel Reader
  - Haodoo Reader

- Rich Text Format (``rtf``)
- Mobipocket (``mobi``)
- Kindle (``azw3``, ``azw4``, …)
- FictionBook (``fb2``)
- Hyper Text Markup Language (``html``)
- Adobe Portable Document Format (``pdf``)
- Broadband eBooks (shortened as BBeB) (``lrf``)

Note, that old Microsoft doc format is not supported, although old documents
can be fairly easy converted using text processors programs, like Microsoft
Word or LibreOffice to supported formats.


Output formats
~~~~~~~~~~~~~~

Currently, following formats are supported:

- Broadband eBooks (shortened as BBeB) (``lrf``)
- EPUB v2 (``epub``)
- Mobipocket (``mobi``)
- Microsoft Word (``docx``)
- zipped HTML file with additional assets, like images (``htmlz``)
- Text (``txt``)


Installation
------------

Ebook converter is somewhere in between in alpha and beta stage, therefore I
didn't place it on `pypi`_ yet.

Preferred way for installation is to use virtualenv (or any other virtualenv
managers), i.e:

.. code:: shell-session

   $ python -m venv venv
   $ . venv/bin/activate
   (venv) $ git clone https://github.com/gryf/ebook-converter
   (venv) $ cd ebook-converter
   (venv) $ pip install -r requirements.txt .

Simple as that. And from now on, you can issue converter:

.. code:: shell-session

   (venv) $ ebook-converter book.docx book.lrf


License
-------

This work is licensed on GPL3 license, like the original work. See LICENSE file
for details.


.. _Calibre project: https://calibre-ebook.com/
.. _pypi: https://pypi.python.org
.. _Liberation fonts: https://github.com/liberationfonts/liberation-fonts
.. _Kindle periodical: https://sellercentral.amazon.com/gp/help/external/help.html?itemID=202047960&language=en-US
.. _poppler: https://poppler.freedesktop.org/
