import pdfplumber
import os
import re
import csv

regex_invoice = r"10\d{8}|40\d{8}"
regex_payment_amount = r'(?<=\s)\d{1,3}(?:,\d{3})*\.\d{2}(?=\s)'

pdf_directory = './payment_advice'
pdf_files = [pdf_file for pdf_file in os.listdir(pdf_directory) if pdf_file.endswith('.pdf')]

for f in pdf_files:
    text = ''
    
    with pdfplumber.open(os.path.join(pdf_directory, f)) as doc:
        for page in doc.pages:
            text += page.extract_text()
            
    invoices = re.findall(regex_invoice, text)
    payment_amounts = re.findall(regex_payment_amount, text)
    
    # Open CSV file for each PDF
    with open(f'output - {f}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Initialize CSV writer
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["Invoice No", "Payment Amount"])
        # Write to CSV
        for i in range(min(len(invoices), len(payment_amounts))):
            writer.writerow([invoices[i], payment_amounts[i]])

    print(f'Processed file: {f}, Data saved in: output - {f}.csv')
    # print(payment_amounts)

