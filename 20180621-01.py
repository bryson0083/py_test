# -*- coding: utf-8 -*-
"""
docx、xlsx文件檔轉PDF透過叫用LibreOffice處理

Note:
	可以先把資料處理成docx或xlsx格式，再透過LibreOffice的功能把檔案轉成pdf檔

	windows cmd 直接轉的指令如下(測試docx跟xlsx都可以轉)
	"C:\Program Files (x86)\LibreOffice 5\program\soffice.exe" -headless -convert-to pdf:writer_pdf_Export -outdir C:\tar_dir D:\py_test\aaa.xlsx

Ref:
	https://stackoverflow.com/questions/45420221/libreoffice-5-command-line-convert-to-pdf-producing-error
	https://ask.libreoffice.org/en/question/50435/docx-to-pdf-on-windows-using-command-line-fails/
	https://michalzalecki.com/converting-docx-to-pdf-using-python/
	https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python
	https://michalzalecki.com/converting-docx-to-pdf-using-python/

"""
from subprocess import check_output

cmd = '"C:\\Program Files (x86)\\LibreOffice 5\\program\\soffice.exe" -headless -convert-to pdf:writer_pdf_Export -outdir C:\\tar_dir D:\\py_test\\aaa.xlsx'
check_output(cmd, shell=True)