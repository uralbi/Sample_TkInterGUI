import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import PyPDF2

invoice_date = '03222022'
folder = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/1 PIERPASS/{invoice_date}/Orig/'

def concat_pdf(folder):
    path = os.path._getfullpathname(folder)

    pdfs = [rf'{path}Letter1.pdf', rf'{path}Letter2.pdf']

    merger = PdfFileMerger(strict=False)

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(rf"{path}Conf_Letters.pdf")

concat_pdf(folder)

def delete_pages_pdf(file, nums):
    """
    :param nums: iterable
    :return: none, saved file
    """
    pdf_f = rf'{file}'
    # file_read = open(pdf_f, 'rb')
    pdf_rd = PdfFileReader(pdf_f)
    pdf_wr = PdfFileWriter()
    to_delete = [n-1 for n in nums]
    pages = pdf_rd.numPages
    for n in range(pages):
        if n not in to_delete:
            pdf_wr.addPage(pdf_rd.getPage(n))
    output_file = f'{file[:-4]}_del_pages.pdf'
    with open(output_file, "wb") as out:
        pdf_wr.write(out)

def extract_pdf(nums):
    """
    :param nums: iterable numbers
    :return: none saved file
    """
    folder = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/PDF/'
    path = os.path._getfullpathname(folder)
    f_name = 'FNS.pdf'
    pdf_f = rf'{path}{f_name}'
    # file_read = open(pdf_f, 'rb')
    pdf_rd = PdfFileReader(pdf_f)
    pdf_wr = PdfFileWriter()
    get_pages = [n-1 for n in nums]
    pages = pdf_rd.numPages
    for n in range(pages):
        if n in get_pages:
            pdf_wr.addPage(pdf_rd.getPage(n))
    output_file = f'{path}{f_name[:-4]}_get_pages.pdf'
    with open(output_file, "wb") as out:
        pdf_wr.write(out)

def info_pdf():
    folder = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/PDF/'
    path = os.path._getfullpathname(folder)
    f_name = 'FNS.pdf'
    pdf_f = rf'{path}{f_name}'
    # file_read = open(pdf_f, 'rb')
    pdf_rd = PdfFileReader(pdf_f)
    t_pages = pdf_rd.getNumPages()
    l_pdf = pdf_rd.getPageLayout
    print(t_pages)


file = 'C:/Users/URAL KOZHOKMATOV/Downloads/UR-Downlight 2021.pdf'

# delete_pages_pdf(file,(1,2,3))
