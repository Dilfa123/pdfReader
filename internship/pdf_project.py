from PyPDF2 import PdfReader
import pandas as pd
import imaplib
import os
import re
import email
import platform
from tkinter import *
from tkinter import ttk,messagebox,filedialog
import logging
import sqlite3



emailUser='dilfakottayil@gmail.com'
email_pass='ktsr qvke vpth csag'
imap_server='imap.gmail.com'
download_dir='invoices'


   

def collect_invoice_from_mail():
    try:
       
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(emailUser, email_pass)
        mail.select("inbox")
        status, messages = mail.search(None, 'SUBJECT "invoice"')
        os.makedirs(download_dir, exist_ok=True)

        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename and filename.endswith('.pdf'):
                    filepath = os.path.join(download_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
        mail.logout()
        messagebox.showinfo("Success", "Invoices downloaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {str(e)}")

def get_invoice_data(file_path):
    invoice_list=[]
    invoice_no_re = r'Invoice\s*Number[:\s]*([A-Z0-9-]+)'
    date_re = r'Date[:\s]*((?:\d{1,2}[/-]){2}\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|(?:\d{1,2}\s)?[a-z]*\s\d{4})'
    amount_re = r'Total(?:\s*Amount)?[:=]?\s*(?:Rs\.?|₹|\$)?\s*([\d,]+\.\d{2}|\d+)'

    

    for file in os.listdir(download_dir):
        if file.endswith('.pdf'):
            file_path=os.path.join(download_dir,file)
            with open(file_path,'rb')as f:
                pdf=PdfReader(f)
                full_text=''
                for page in pdf.pages:
                    page_text=page.extract_text()
                    full_text+=page_text+'\n'
            invoice_no=re.search(invoice_no_re,full_text)
            date=re.search(date_re,full_text)
            amount=re.search(amount_re,full_text)


        print(full_text)
        invoice_list.append({
            'File':file,
            'Invoice Number':invoice_no.group(1)if invoice_no else 'Not Found',
            'Date':date.group(1)if date else 'Not Found',
            'Total Amount':amount.group(1) if amount else 'Not Found'})
    return invoice_list
def upload_invoice():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        result = get_invoice_data(file_path)  # This function should handle a single PDF
        if result:
            get_invoice_data.append(result)
            insert_row_to_table(result)
            messagebox.showinfo("Success", f"Extracted invoice '{result['Invoice Number']}'.")







# def save_to_sqlite(data):
#     try:
#         con = sqlite3.connect('invoice_data.db')
#         cursor = con.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS invoices (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 file_name TEXT,
#                 invoice_num TEXT,
#                 date TEXT,
#                 amount TEXT
#             )
#         ''')
#         for item in data:
#             cursor.execute('''
#                 INSERT INTO invoices(file_name, invoice_num, date, amount)
#                 VALUES (?, ?, ?, ?)
#             ''', (item['File'], item['Invoice Number'], item['Date'], item['Total Amount']))
#         con.commit()
#         con.close()
#         messagebox.showinfo("Success", "Data saved to SQLite database.")
#     except Exception as e:
#         messagebox.showerror("Error", f"SQLite Save Failed: {str(e)}")

logging.basicConfig(filename="invoice_app.log", level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
def save_to_excel():
    try:
        invoice_data = get_invoice_data(download_dir)  # Get fresh data

        if not invoice_data:
            messagebox.showwarning("No Data", "No invoice data found.")
            return

        df = pd.DataFrame(invoice_data)
        file_path = "invoice_collection.xlsx"
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Data saved to {file_path}")

        if platform.system() == "Windows":
            os.startfile(file_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Excel: {str(e)}")
def handle_select_pdf():
    collect_invoice_from_mail()
    extracted = get_invoice_data(download_dir)
    populate_treeview(extracted)


def create_main_window():
    global root
    root = Tk()
    root.title("Invoice Uploader")
    root.geometry("750x500")
    return root

def setup_labels_buttons(root):
    Label(root, text="Upload an Invoice PDF", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Select PDF", command=upload_invoice).pack(pady=5)
    Button(root, text="Save to Excel", command=save_to_excel).pack(pady=5)

def setup_table(root):
    global tree
    table_frame = Frame(root)
    table_frame.pack(pady=20, fill="both", expand=True)

    tree = ttk.Treeview(table_frame, columns=("File", "Invoice Number", "Date", "Total Amount"), show='headings')
    for col in ("File", "Invoice Number", "Date", "Total Amount"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

def upload_invoice():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        result = get_invoice_data(file_path)
        if result:
            get_invoice_data.append(result)
            insert_row_to_table(result)
            messagebox.showinfo("Success", f"Extracted invoice '{result['Invoice Number']}'.")

def insert_row_to_table(row):
    tree.insert('', END, values=(row['File'], row['Invoice Number'], row['Date'], row['Total Amount']))

def generate_summary_report():
    data = get_invoice_data(download_dir)
    if not data:
        messagebox.showwarning("No Data", "No invoice data to summarize.")
        return

    df = pd.DataFrame(data)

    # Clean amount column
    df['Total Amount'] = df['Total Amount'].replace('[^0-9.]', '', regex=True)
    df['Total Amount'] = pd.to_numeric(df['Total Amount'], errors='coerce')

    # Convert dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if df['Date'].isnull().all():
        messagebox.showerror("Error", "Could not parse any invoice dates.")
        return

    # Group by month
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_summary = df.groupby('Month')['Total Amount'].sum()

    # Convert to DataFrame for Excel
    summary_df = monthly_summary.reset_index()
    summary_df.columns = ['Month', 'Total Amount']

    summary_path = "generate_summery.xlsx"
    summary_df.to_excel(summary_path, index=False)
    messagebox.showinfo("Report Generated", f"Summary saved to {summary_path}")
    os.startfile(summary_path)


# ---------------------------- Main ---------------------------- #
def populate_treeview(data):
    # Clear existing data
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert new data
    for row in data:
        tree.insert('', 'end', values=(row['File'], row['Invoice Number'], row['Date'], row['Total Amount']))
def setup_ui():
    global root, tree

    root = Tk()
    root.title("Invoice Uploader")

    label = Label(root, text="Upload an Invoice PDF", font=("Arial", 14))
    label.pack(pady=10)

    select_btn = Button(root, text="Select PDF", command=handle_select_pdf)
    select_btn.pack(pady=5)

    save_btn = Button(root, text="Save to Excel", command=save_to_excel)
    save_btn.pack(pady=5)

    # ✅ Add report button here
    report_btn = Button(root, text="Generate Report", command=generate_summary_report)
    report_btn.pack(pady=5)
    
    columns = ("File", "Invoice Number", "Date", "Total Amount")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(padx=10, pady=10)
    # Button(root, text="Save to SQLite", command=lambda: save_to_sqlite(get_invoice_data(download_dir))).pack(pady=5)

    root.mainloop()
if __name__ == "__main__":
    logging.info("Starting Invoice Uploader Application")
    setup_ui()

    





                    



