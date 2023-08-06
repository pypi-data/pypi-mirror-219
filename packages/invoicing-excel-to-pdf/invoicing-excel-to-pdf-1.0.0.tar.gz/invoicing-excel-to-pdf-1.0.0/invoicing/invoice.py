# import openpyxl (its enough to download dependency)
import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path="Invoices", pdfs_path="PDFs", image_path="pythonhow.png",
             product_id='product_id', product_name='product_name',
             amount_purchased='amount_purchased', price_per_unit='price_per_unit', total_price='total_price'):
    """
    This function converts invoice Excel files into PDF invoices,
    by default folders are in the same directory as the project
    :param invoices_path: is supposed to be folder containing excel invoices
    :param pdfs_path: is supposed to be folder for output pdf invoices
    :param image_path: image to be displayed under pdf invoice
    names of columns in Excel invoice file:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        filepath = filepath.strip("~$")  # error handling

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem  # gets us string with name without path, format
        number, date = filename.split(sep="-")

        pdf.set_font("Times", "B", 20)
        pdf.cell(w=0, h=10, txt=f"Invoice nr. {number}", border=0, ln=1, align="L")
        pdf.cell(w=0, h=10, txt=f"Date {date}", border=0, ln=1, align="L")
        pdf.cell(w=0, h=10, border=0, ln=1, align="L")
        pdf.set_font("Times", size=12)
        pdf.cell(w=30, h=10, txt=f"Product ID", border=1, ln=0, align="L")  # Table labels
        pdf.cell(w=70, h=10, txt=f"Product Name", border=1, ln=0, align="L")
        pdf.cell(w=30, h=10, txt=f"Amount", border=1, ln=0, align="L")
        pdf.cell(w=30, h=10, txt=f"Price per Unit", border=1, ln=0, align="L")
        pdf.cell(w=30, h=10, txt=f"Total Price", border=1, ln=1, align="L")

        total = 0  # we could do sum(row["total_price"]) in comming for loop
        for index, row in df.iterrows():
            pdf.set_font("Helvetica", size=10)
            pdf.cell(w=30, h=10, txt=f"{row[product_id]}", border=1, ln=0, align="L")
            pdf.cell(w=70, h=10, txt=f"{row[product_name]}", border=1, ln=0, align="L")
            pdf.cell(w=30, h=10, txt=f"{row[amount_purchased]}", border=1, ln=0, align="L")
            pdf.cell(w=30, h=10, txt=f"{row[price_per_unit]}", border=1, ln=0, align="L")
            pdf.cell(w=30, h=10, txt=f"{row[total_price]}", border=1, ln=1, align="L")
            total += row[amount_purchased] * row[price_per_unit]  # or += row["total_price"]

        pdf.cell(w=160, h=10, border=1, ln=0, align="L")
        pdf.cell(w=30, h=10, txt=f"{total}", border=1, ln=1, align="L")
        pdf.cell(w=0, h=5, border=0, ln=1, align="L")  # empty cell after table
        pdf.set_font("Times", "B", 16)
        pdf.cell(w=0, h=10, txt=f"The total due amount is {total}", border=0, ln=1, align="L")
        pdf.cell(w=33, h=10, txt=f"PythonHow")
        pdf.image(image_path, w=10)

        pdf.set_y(270)  # self promotion :)
        pdf.set_x(180)
        pdf.set_font("Times", "U", 11)
        pdf.cell(w=25, h=6, txt="From portfolio:", border=0, align="C",
                 link="https://s1fam-portfolio-home-at8i55.streamlit.app")

        try:
            os.makedirs(pdfs_path)
        except FileExistsError:
            pass

        pdf.output(f"{pdfs_path}/{filename}.pdf")  # we generate files with pdf format


if __name__ == "__main__":
    generate()
