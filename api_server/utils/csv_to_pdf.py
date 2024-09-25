import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import utils.pdf_watermark as pdf_watermark

from utils.path_dict import output_csv_dir, output_pdf_dir, input_img_dir


def csv_to_pdf(csv_name):
    output_csv_dir.mkdir(parents=True, exist_ok=True)
    output_pdf_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_csv_dir / (csv_name + ".csv")
    # convert to string for pdf lib
    pdf_path = str(output_pdf_dir / (csv_name + ".pdf"))

    df = pd.read_csv(csv_path)

    pdf = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # 將數據轉換為列表，第一行是表頭
    data = [df.columns.to_list()] + df.values.tolist()
    pdfmetrics.registerFont(TTFont("Sans-Regular", "NotoSansTC-Bold.ttf"))  # 宋體
    table = Table(data)

    style = TableStyle(
        [
            ("FONTNAME", (0, 0), (-1, -1), "Sans-Regular"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),  # 表頭背景
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # 表頭文字
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # 文字左右居中
            ("ALIGN", (4, 1), (4, -1), "LEFT"),  # 文字左右居中
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # 文字上下居中
            ("FONTSIZE", (0, 0), (-1, 0), 12),  # 表頭字體大小
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # 表頭底部內邊距
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),  # 表格背景顏色
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # 表格線顏色
        ]
    )
    table.setStyle(style)
    elements.append(table)
    pdf.build(elements)


def csv_to_pdf_with_watermark(csv_name, mode="text"):

    csv_to_pdf(csv_name)
    pdf_path = str(output_pdf_dir / (csv_name + ".pdf"))
    watermark_path = str(output_pdf_dir / ("watermark" + ".pdf"))
    pdf_watermark_path = str(output_pdf_dir / (csv_name + "_watermark" + ".pdf"))

    pdf_width, pdf_height = pdf_watermark.get_pdf_page_size(pdf_path)

    if mode == "text":

        watermark_x, watermark_y = 0, 0

        pdf_watermark.create_text_watermark(
            "KnoxHsu-Confidential",
            watermark_x,
            watermark_y,
            pdf_width,
            pdf_height,
            output=watermark_path,
        )

    elif mode == "image":
        image_path = str(input_img_dir / "watermark.png")

        img_width, img_height = pdf_watermark.get_image_size(image_path)
        watermark_x, watermark_y = (
            float(pdf_width) / 2 - img_width / 2,
            float(pdf_height) / 2 - img_height / 2,
        )

        pdf_watermark.create_image_watermark(
            image_path,
            watermark_x,
            watermark_y,
            pdf_width,
            pdf_height,
            output=watermark_path,
        )

    pdf_watermark.add_watermark(pdf_path, watermark_path, pdf_watermark_path)
