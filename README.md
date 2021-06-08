# poppdf

A python (3.6+) module that wraps poppler's pdftoimage, pdftohtml and pdftotext to extract informations from PDF.
## What information is extracted
 - image
 - text
 - infromation about the position of various text lines

## How to install

`pip install poppdf`

### Windows

Windows users will have to build or download poppler for Windows. I recommend [@oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) which is the most up-to-date. You will then have to add the `bin/` folder to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or use `poppler_path = r"C:\path\to\poppler-xx\bin" as an argument` in `convert_from_path`.

### Mac

Mac users will have to install [poppler for Mac](http://macappstore.org/poppler/).

### Linux

Most distros ship with `pdftoppm` and `pdftocairo`. If they are not installed, refer to your package manager to install `poppler-utils`

### Platform-independant (Using `conda`)

1. Install poppler: `conda install -c conda-forge poppler`
2. Install pdf2image: `pip install pdf2image`

## How does it work?

`from pdf2image import image_from_path, xml_from_path, text_from_path`

```py
from poppdf.pdfDocument import PdfDocument
```

Then simply do:

```py
pdf = PdfDocument('example.pdf')
```

And

```py
print(pdf.pages[1].text)
```
