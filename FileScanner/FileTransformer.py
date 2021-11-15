#아직 hwp를 이미지로 바꾸는 건 성공 못함...
#hwp -> pdf 하려면 특정 라이브러리 설치해야 하는데 이 방법 말고 다른 방법 찾고 있어용.

#-*- coding: utf-8 -*-
#pdf to jpg 코드에 필요한 라이브러리
import os
from contextlib import suppress

#word to pdf 코드에 필요한 라이브러리
import comtypes
import ntpath
from pdf2jpg import pdf2jpg

import win32com.client

#pdf 파일을 jpg로 바꿔준다.
#pdf가 여러장일 경우 dir을 생성하여 그 안에 이미지 여러 장 생성.
#이 때 dir의 이름은 파일명.pdf_dir이 되며
#dir 내 이미지 이름은 순서대로 0, 1, 2..._파일명.pdf.jpg가 된다.
#파일명에 한글이 섞여도 잘 작동한다.
def pdf_to_jpg(file):
    dest = os.path.dirname(file)
    if not os.path.isdir(dest):
        os.mkdir(dest)
    pdf2jpg.convert_pdf2jpg(file, dest, dpi = 300, pages ='ALL')


#word 파일을 먼저 pdf로 바꿔준다.
def word_to_pdf(file):
    dest = os.path.dirname(file)

    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(file)

    file_name = ntpath.basename(file)
    output_file_path = os.path.join(dest, file_name + ".pdf")
    doc.SaveAs(output_file_path, FileFormat=17)
    doc.Close()
    return output_file_path

def word_to_jpg(file):
    with suppress(KeyError): pdf_to_jpg(word_to_pdf(file))
    #실행하면 에러는 뜨는데 실행되긴 됨. 근데 무슨 에러인지를 모르겠음...

def hwp_to_pdf(file):
    dest = os.path.dirname(file)

    hwp = win32com.client.gencache.EnsureDispatch('HWPFrame.HwpObject')
    hwp.RegisterModule('FilePathCheckDLL', 'SecurityModule')
    hwp.Open(os.path.join(dest, file))
    hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
    pre, ext = os.path.splitext(file)
    hwp.HParameterSet.HFileOpenSave.filename = os.path.join(dest,pre + ".pdf")
    hwp.HParameterSet.HFileOpenSave.Format = "PDF"
    hwp.HAction.Execute("FileSaveAs_s", hwp.HParameterSet.HFileOpenSave.HSet)
    hwp.Quit()
