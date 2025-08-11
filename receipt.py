import subprocess
import os
import qrcode
from fpdf import FPDF
from user import UserProfile
from formatting import convert_from_db_datetime

class PDF(FPDF):
    def header(self):
        self.set_fill_color(231, 230, 230)
        self.set_xy(0, 0)
        self.set_font('helvetica', "", 12)
        self.cell(30, 12, "", ln=False, fill=True)
        self.cell(190, 12, '', ln=True, align="L", fill=True)
        self.set_xy(0, 12)
        self.cell(30, 12, "", ln=False, fill=True)
        self.cell(190, 12, 'UoG Clothing', ln=True, align="L", fill=True)

        self.image('images/tshirt.png', 10, 2, 20)

    def footer(self):
        self.set_xy(0, -24)
        self.set_fill_color(231, 230, 230)
        self.set_font('helvetica', "I", 12)
        self.cell(216, 12, 'UoG Clothing© 2023', ln=1, align="C", fill=True)
        self.set_xy(0, -12)
        self.cell(216, 12, 'Tel: 01242 123123    Email: sales@uogclothing.co.uk', align='C', fill=True)


class OrderReceipt(PDF):
    def __init__(self, order_details, receipt_type):
        PDF.__init__(self)
        self.order_details = order_details
        self.receipt_type = receipt_type
        self.pdf = PDF()

        # Save qrcode to temp file for use in pdf
        self.file_dir = os.path.dirname(os.path.realpath('__file__'))
        self.qr_path = os.path.join(self.file_dir, 'QrCode/QRCODE.png')
        data = """{"ORDER_ID": %s, "ORDER_DATE": %s}""" % (order_details[0].receipt_number, order_details[0].order_date)
        img = qrcode.make(data)
        img.save(self.qr_path)

    def generate_receipt(self):
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        file_name = "temp"
        if self.receipt_type == "RECEIPT":
            self.receipt_details()
            file_name = "UOGC-RECEIPT%d.pdf" % (self.order_details[0].receipt_number)
        elif self.receipt_type == "INVOICE":
            self.invoice_details()
            file_name = "UOGC-INVOICE%d.pdf" % (self.order_details[0].receipt_number)

        self.address()
        self.create_receipt_table()
        self.add_footnote()

        # Save and open the pdf in default pdf software
        pdf_path = os.path.join(self.file_dir, 'pdf/')
        full_path = os.path.join(pdf_path, file_name)
        self.pdf.output(full_path)
        subprocess.Popen([full_path], shell=True)

    def add_footnote(self):
        if self.receipt_type == "RECEIPT":
            self.pdf.cell(191, 12, "", ln=1, align='R')
            self.pdf.cell(191, 6, f"Items will be dispatched shortly", ln=1, align='R')
            self.pdf.cell(191, 6, "", ln=1, align='R')
            self.pdf.cell(191, 6, f"This is not an invoice", ln=1, align='R')
        elif self.receipt_type == "INVOICE":
            self.pdf.cell(191, 12, "", ln=1, align='R')
            self.pdf.cell(191, 6, f"Payment will be taken from your registered account", ln=1, align='R')

    def receipt_details(self):
        self.pdf.set_font("helvetica", "", 12)
        self.pdf.ln()
        self.pdf.set_font("helvetica", "", 24)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(80, 25, "ORDER RECEIPT", ln=1)
        self.pdf.image(self.qr_path, 156, 25, 50)  # images/MyQRCode1.png'
        self.pdf.set_y(50)
        self.pdf.set_font("helvetica", "", 10)
        self.pdf.cell(80, 8, "Thank you for your order", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_y(72)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Receipt Number:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{self.order_details[0].receipt_number}", ln=1, align='R')
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Order Date:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{convert_from_db_datetime(self.order_details[0].order_date)[0:10]}", ln=1, align='R')

    def invoice_details(self):
        self.pdf.set_font("helvetica", "", 12)
        self.pdf.ln()
        self.pdf.set_font("helvetica", "", 24)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(80, 25, "SALES INVOICE", ln=1)
        # self.pdf.image(self.qr_path, 156, 25, 50)  # images/MyQRCode1.png'
        self.pdf.set_y(50)
        self.pdf.set_font("helvetica", "", 10)
        self.pdf.cell(80, 8, "Thank you for your custom", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_y(72)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Invoice Number:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{self.order_details[0].receipt_number}", ln=1, align='R')
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Order Date:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{convert_from_db_datetime(self.order_details[0].order_date)[0:10]}", ln=1, align='R')

    def address(self):
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln()
        self.pdf.ln()
        # Company Address and Customer Address
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.cell(98, 6, "From:", ln=0)
        self.pdf.cell(93, 6, "Deliver To:" if self.receipt_type == "RECEIPT" else "To:", ln=1, align='R')

        self.pdf.set_font("helvetica", "", 14)
        self.pdf.cell(98, 6, "UoG Clothing Ltd.", ln=0)
        self.pdf.cell(
            93, 6, f"{UserProfile.current_user.first_name} {UserProfile.current_user.last_name}", ln=1, align='R'
        )

        self.pdf.cell(98, 6, "UoG Park Campus", ln=0)
        self.pdf.cell(93, 6, f"{UserProfile.current_user.address}", ln=1, align='R')

        self.pdf.cell(98, 6, "Cheltenham", ln=0)
        self.pdf.cell(93, 6, f"{UserProfile.current_user.city}", ln=1, align='R')

        self.pdf.cell(98, 6, "Gloucestershire", ln=0)
        self.pdf.cell(93, 6, f"{UserProfile.current_user.city}", ln=1, align='R')

        self.pdf.cell(98, 6, "GL52 1AA", ln=0)
        self.pdf.cell(93, 6, f"{UserProfile.current_user.postcode}", ln=1, align='R')
        self.pdf.ln()

    def create_receipt_table(self, columns=3):
        self.pdf.ln()
        # create header row
        column_header = [[30, "Item Code"], [130, "Description"], [30, "Price"]]

        self.pdf.set_font("helvetica", "B", 14)
        for i in range(0, columns):
            self.pdf.set_fill_color(231, 230, 230)
            self.pdf.cell(column_header[i][0], 6, column_header[i][1], ln=0, border=1, align='C', fill=True)
        self.pdf.ln()
        total = 0
        self.pdf.set_font("helvetica", "", 12)
        for i in range(len(self.order_details)):
            total += self.order_details[i].price
            self.pdf.cell(30, 6, f"IC-{str(self.order_details[i].item_code)}", ln=0, border=1, align='C')
            self.pdf.cell(130, 6, str(self.order_details[i].item_name[0:60]), ln=0, border=1, align='L')
            price = "{:.2f}".format(self.order_details[i].price)
            self.pdf.cell(30, 6, f"£{price}", ln=1, border=1, align='R')

        total = "{:.2f}".format(total)
        self.pdf.cell(30, 6, "", ln=0, border=0, align='C')
        self.pdf.cell(130, 6, "Total:", ln=0, border=1, align='R')
        self.pdf.cell(30, 6, f"£{total}", ln=1, border=1, align='R')

        if self.receipt_type == "INVOICE":
            vat_amount = (float(total) * 0.2)
            total_ex_vat = (float(total) - vat_amount)

            total_ex_vat = "{:.2f}".format(total_ex_vat)
            self.pdf.cell(30, 6, "", ln=0, border=0, align='C')
            self.pdf.cell(130, 6, "Total (Excluding VAT):", ln=0, border=1, align='R')
            self.pdf.cell(30, 6, f"£{total_ex_vat}", ln=1, border=1, align='R')

            vat_amount = "{:.2f}".format(vat_amount)
            self.pdf.cell(30, 6, "", ln=0, border=0, align='C')
            self.pdf.cell(130, 6, "VAT Amount:", ln=0, border=1, align='R')
            self.pdf.cell(30, 6, f"£{vat_amount}", ln=1, border=1, align='R')


class ReturnReceipt(PDF):
    def __init__(self, return_details):
        PDF.__init__(self)
        self.return_details = return_details
        self.pdf = PDF()
        self.file_dir = os.path.dirname(os.path.realpath('__file__'))

    def generate_receipt(self):
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        file_name = "UOGC-RETURN%d.pdf" % (self.return_details.stock_order_id)

        self.receipt_details()

        self.customer_address()
        self.return_advice()
        self.return_slip()

        # Save and open the pdf in default pdf software
        pdf_path = os.path.join(self.file_dir, 'pdf/')
        full_path = os.path.join(pdf_path, file_name)
        self.pdf.output(full_path)
        subprocess.Popen([full_path], shell=True)

    def receipt_details(self):
        self.pdf.set_font("helvetica", "", 12)
        self.pdf.ln()
        self.pdf.set_font("helvetica", "", 24)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(80, 25, "RETURNS RECEIPT", ln=1)
        # self.pdf.image(self.qr_path, 156, 25, 50)  # images/MyQRCode1.png'
        self.pdf.set_y(50)
        self.pdf.set_font("helvetica", "", 10)
        self.pdf.cell(80, 8, "Product return details", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_y(72)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Returns Number:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{self.return_details.stock_order_id}", ln=1, align='R')
        self.pdf.cell(98, 6, "", ln=0)
        self.pdf.cell(60, 6, f"Return Date:", ln=0, align='R')
        self.pdf.cell(33, 6, f"{self.return_details.return_date[0:10]}", ln=1, align='R')

    def customer_address(self):
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln()
        self.pdf.ln()
        # Company Address and Customer Address
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.cell(98, 6, "Return For:", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.cell(198, 6, f"{UserProfile.current_user.first_name} {UserProfile.current_user.last_name}", ln=1)
        self.pdf.cell(198, 6, f"{UserProfile.current_user.address}", ln=1)
        self.pdf.cell(198, 6, f"{UserProfile.current_user.city}", ln=1)
        self.pdf.cell(198, 6, f"{UserProfile.current_user.postcode}", ln=1)
        self.pdf.cell(198, 6, "", ln=1)
        self.pdf.ln()

    def return_slip(self):
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.cell(85, 6, "Return Address:", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.cell(85, 6, "UoG Clothing Ltd.", ln=0)
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.cell(106, 6, f"RETURNS NUMBER: {self.return_details.stock_order_id}", ln=1, align='R')
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.cell(85, 6, "UoG Park Campus", ln=1)
        self.pdf.cell(85, 6, "Cheltenham", ln=0)
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.cell(106, 6, f"Item Code: IC-{self.return_details.item_code}", align="R", ln=1)
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.cell(85, 6, "Gloucestershire", ln=0)
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.multi_cell(106, 6, f"{self.return_details.item_name}", align="R")
        self.pdf.set_font("helvetica", "", 14)
        self.pdf.set_y(246)
        self.pdf.cell(85, 6, "GL52 1AA", ln=1)

    def return_advice(self):
        self.pdf.cell(191, 12, "", ln=1)
        self.pdf.cell(191, 6, f"Please return the item using the returns slip below.", ln=1)
        self.pdf.cell(191, 3, "", ln=1)
        self.pdf.cell(
            191, 6, f"If you have multiple items to return please include a returns slip for each item.", ln=1
        )
        self.pdf.cell(191, 3, "", ln=1)
        self.pdf.cell(
            191, 6, f"A refund will be issues once the items have been received.", ln=1
        )
        self.pdf.cell(191, 24, "", ln=1)
        self.pdf.cell(
            191, 6, f"-----------------------------------------------------------------------------"
                    f"-------------------------------------", ln=1)
        self.pdf.cell(191, 12, "", ln=1)

