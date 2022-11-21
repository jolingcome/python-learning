#pypdf:主要用来处理 pdf 文件，包括了常见的分离、合并、裁剪、转换、加密、解密等功能。
#pdfplumber提取PDF文字
#https://zhuanlan.zhihu.com/p/344384506
from PyPDF2 import PdfFileReader
import pdfplumber
reader=PdfFileReader(r"C:\yangling2\桌面\test.pdf")
print(reader)

#总页数
# number_of_pages=len(reader.pages)
# print(number_of_pages)

#第一页
# with pdfplumber.open(r"C:\yangling2\桌面\test.pdf") as pdf:
#     page01=pdf.pages[0] #指定页码
#     text=page01.extract_text() #提取文本
#     print(text)

# #提取所有pdf文字并写入文本中
# with pdfplumber.open(r"C:\yangling2\桌面\test.pdf") as pdf:
#     for page in pdf.pages:
#         text=page.extract_text()
#         text_file=open(r"C:\yangling2\桌面\test.txt",mode='a',encoding='utf-8')
#         text_file.write(text)

# #提取pdf表格
# with pdfplumber.open(r"C:\yangling2\桌面\test.pdf") as pdf:
#     page01=pdf.pages[0]
#     table1=page01.extract_table() #提取单个表格
#     # table2=page01.extract_tables() #提取多个表格
#     print(table1)

#提取表格，保存为excel文件
# from openpyxl import Workbook
# with pdfplumber.open(r"C:\yangling2\桌面\test.pdf") as pdf:
#     page01=pdf.pages[0]
#     table=page01.extract_table()
#     workbook=Workbook()
#     sheet=workbook.active
#     for row in table:
#         sheet.append(row)
#     workbook.save(filename=r"C:\yangling2\桌面\test.xlsx")

# PyPDF2 中有两个最常用的类：PdfFileReader和PdfFileWriter，分别用于读取 PDF 和写入 PDF。
# 其中PdfFileReader传入参数可以是一个打开的文件对象，也可以是表示文件路径的字符串。
# 而PdfFileWriter则必须传入一个以写方式打开的文件对象
# #分割
# from PyPDF2 import PdfFileReader,PdfFileWriter
# file_reader=PdfFileReader(r"C:\yangling2\桌面\test.pdf")
# #getNumPages()获取总页数
# for page in range(file_reader.getNumPages()):
#     #实例化对象
#     file_writer=PdfFileWriter()
#     #将遍历的每一页添加到实例化对象中
#     file_writer.addPage(file_reader.getPage(page))
#     with open("C:\yangling2\桌面\{}.pdf".format(page),'wb') as out:
#         file_writer.write(out)

# #合并pdf
# file_writer=PdfFileWriter()
# for page in range(2): #2个文件
#     #循环读取需要合并的pdf文件
#     file_reader=PdfFileReader("C:\yangling2\桌面\{}.pdf".format(page))
#     #遍历每个pdf的每一页
#     for page in range(file_reader.getNumPages()):
#         #写入实例化对象中
#         file_writer.addPage(file_reader.getPage(page))
# with open("C:\yangling2\桌面\合并.pdf",'wb') as out:
#     file_writer.write(out)

# #pdf旋转
# file_read=PdfFileReader(r"C:\yangling2\桌面\test.pdf")
# file_writer=PdfFileWriter()
# page=file_reader.getPage(0).rotateClockwise(90) #第1页顺时针旋转90度
# file_writer.addPage(page)
# with open(r"C:\yangling2\桌面\旋转.pdf",'wb') as out:
#     file_writer.write(out)

# # PDF加密解密
# file_read=PdfFileReader(r"C:\yangling2\桌面\test.pdf")
# file_writer=PdfFileWriter()
# for page in range(file_reader.getNumPages()):
#     file_writer.addPage(file_reader.getPage(page))
# file_writer.encrypt('123456') #设置密码
# with open(r"C:\yangling2\桌面\test.pdf",'wb') as out:
#     file_writer.write(out)

# # PDF解密
# # from PyPDF2 import PdfFileReader,PdfFileWriter
# # file_read=PdfFileReader(r"C:\yangling2\桌面\test.pdf")
# # file_read.decrypt('123456')
# # file_writer=PdfFileWriter()
# # for page in range(file_read.getNumPages()):
# #     file_writer.addPage(file_read.getPage(page))
# # with open(r"C:\yangling2\桌面\解密后.pdf",'wb') as out:
# #     file_writer.write(out)

# # PDF添加水印
from PyPDF2 import  PdfFileReader, PdfFileWriter
from copy import copy
sy = PdfFileReader("D:\\pdffiles\\水印.pdf")
mark_page = sy.getPage(0) # 水印所在的页数
# 读取添加水印的文件
file_reader = PdfFileReader("D:\\pdffiles\\Python编码规范中文版.pdf")
file_writer = PdfFileWriter()

for page in range(file_reader.getNumPages()):
    # 读取需要添加水印每一页pdf
    source_page = file_reader.getPage(page)
    new_page = copy(mark_page) #
    new_page.mergePage(source_page) # new_page(水印)在下面，source_page原文在上面
    file_writer.addPage(new_page)

with open("D:\\pdffiles\\添加水印后.pdf",'wb') as out:
    file_writer.write(out)

