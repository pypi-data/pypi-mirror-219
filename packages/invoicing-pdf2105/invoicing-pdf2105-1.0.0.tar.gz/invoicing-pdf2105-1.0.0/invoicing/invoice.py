import pandas as pd
import glob 
from fpdf import FPDF
from pathlib import Path
import os 


def generate (invoices_path, pdfs_path, image_path, product_id, product_name, 
              amount_purchased, price_per_unit, total_price): 
    """
    This function converts invoiceExcel files into PDF.
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
# invoices_path - parameter to define where is user's xslx files are located. 
# pdfs_path - directory in which function will store new pdfs. 
# image_path - path to the img. Also there are 
# 5 additional arguments, users will put columns name to make pdf columns creation more dynamic.
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        filename = Path(filepath).stem 
        # .stem converts from filename = Path(filename) -> PosixPath("invoices/10001-2023.1.18.xslx")
        # to Path(filepath).stem -> 10001-2023.1.18
        invoice_number, date = filename.split("-")
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_number}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
    
        df = pd.read_excel(filepath, sheet_name="Sheet 1") 
        # Command to read xslx files

        # This is the header
        columns = list(df.columns) 
        # We converting this value from .columns function to the list since  
        # .columns is defaultly the Index object 
        columns = [item.replace("_", " ").title() for item in columns] #reminder of the list comprehension stracture
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80,80,80)
        pdf.cell(w=30, h=8, txt=str(columns[0]), border=1) #fpdf expects str here, 
        #  As a value of txt arg, but defaultly there is a int value. That's why we've changed it
        pdf.cell(w=70, h=8, txt=str(columns[1]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[2]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[3]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[4]), border=1, ln=1)    



        # These are the values from xslx file
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80,80,80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)
        
        
        # To add the last row with a total value
        total_value = df[total_price].sum()
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=70, h=8, border=1)
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=30, h=8, txt=str(total_value), border=1, ln=1)

        #  Total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_value}", ln=1)

        # Company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=f"PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path) #to create PDF path. We will generate pdf's directory for a user
        pdf.output(f"{pdfs_path}/{filename}.pdf")