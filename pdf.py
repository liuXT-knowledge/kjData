from aip import AipOcr
import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
import sys,os,glob,time
""" 你的 APPID AK SK """
APP_ID = '28444379'
API_KEY = 'AmMF08KRfDRYWFVVDRjdiFV8'
SECRET_KEY = 'O3pylpsn6cZtzYIITiap2KqRvYc3gGqL'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

rootPath = r'E:\Download\BaiduNetdiskDownload\2022初级会计网校课程\实务\【03】习题强化班-冯雅竹（0906讲全）\讲义'
kj_txtFile = []
for value in os.listdir(rootPath):
    kj_txtFile.append(rootPath + "\\"+value[0:4]+".txt")
kj_filePath = []
for file_abs in glob.glob(rootPath+'\*'):
    kj_filePath.append(file_abs)

pdfPage = 1
'''def get_file_content(filePath):
    if(filePath.endswith('.pdf')):
        try:
            f = pdfplumber.open(filePath)
            pdfPage = len(f.pages)
            #print(pdfPage)
        except PDFSyntaxError:
            return None
    with open(filePath, "rb") as fp:
        return fp.read()'''
for index,v in enumerate(kj_filePath):
    if(v.endswith('.pdf')):
        try:
            f = pdfplumber.open(v)
            pdfPage = len(f.pages)
        except PDFSyntaxError:
            sys.exit(0)
    with open(v, "rb") as fp:
        file_rd =  fp.read()
    if file_rd is None:
        sys.exit(0)
    options = {}
    text = []
    for num in range(1,pdfPage+1):
        options['pdf_file_num'] = str(num)
        res_file = client.basicAccuratePdf(file_rd,options)
        time.sleep(10)
        if('words_result' in res_file):
            for i,value in enumerate(res_file['words_result']):
                text.append(f'{value["words"]}' + '\n')
    with open(kj_txtFile[index],'w',encoding='utf-8') as file:
        file.write(''.join(text))


