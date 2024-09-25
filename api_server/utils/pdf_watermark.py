from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


def get_pdf_page_size(pdf_file):

    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    media_box = page.mediabox
    return media_box.width, media_box.height


def get_image_size(image_path):

    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def set_image_rotate(image_path, degree):

    with Image.open(image_path) as img:
        img = img.rotate(degree)
    return img


def create_image_watermark(
    image_path, x, y, pdf_width, pdf_height, output="watermark_image.pdf"
):
    c = canvas.Canvas(output, pagesize=(pdf_width, pdf_height))
    img = ImageReader(image_path)
    c.drawImage(img, x, y, mask="auto")
    c.save()


def create_text_watermark(
    watermark_text, x, y, pdf_width, pdf_height, output="watermark_text.pdf"
):
    c = canvas.Canvas(output, pagesize=(pdf_width, pdf_height))
    c.setFont("Helvetica", 50)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)
    c.translate(150, 250)
    c.rotate(45)
    c.drawString(x, y, watermark_text)
    c.save()


def add_watermark(input_pdf, watermark_pdf, output_pdf):
    
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(input_pdf)
    watermark_reader = PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)
