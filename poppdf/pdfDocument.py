from poppdf.poppler import image_from_path, xml_from_path, text_from_path
from poppdf.common import parse_pages

class PdfPage():
    def __init__(self, page):
        self.text_lines=page["texts"]
        self.width=page["width"]
        self.height=page["height"]
        self.number=page["number"]
        self.image=None
        self.text=None

class PdfDocument():
    def __init__(self, path):

        self.pages=[]
        xml_data= xml_from_path(pdf_path=path)
        pages=parse_pages(xml_data)

        for p_num, p in pages.items():
            page=PdfPage(p)
            size=(p["width"], p["height"])
            page.image=image_from_path(pdf_path=path, first_page=p_num, last_page=p_num,size=size)[0]
            page.text = text_from_path(path, first_page=p_num, last_page=p_num)
            self.pages.append(page)


pdf=PdfDocument("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/pdf2text/pdf2/CS Invm Fds 3 - Credit Suisse (Lux) Emerging Market Corporate Investment Grade Bond Fund IA USD.pdf")
print(pdf.pages[1].text)