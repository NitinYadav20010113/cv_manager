# from _typeshed import Self
import docx2txt
import cv2, time
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os, subprocess,time
import PyPDF2
from PyPDF2 import PdfReader 
import traceback
import fitz  # PyMuPDF  


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

class Textgenerator:
    dirloc = ""
    
    def to_raw(string):
        return fr"{string}"

    # def pprocessor(text):
        # txt = text.replace('\n\n','  ')
        # txt = text.replace('\n','  ')
        # txt = txt.replace('\t','  ')
        # return txt
    def file2txt(file,dirloc=dirloc):
    # write some code here
    # extension=
        # This If condition will run if the file extension is docx
        if file.lower().endswith('.docx'):
            text=docx2txt.process(file)
            return text
        
        elif file.lower().endswith('.pdf'):
            text=extract_text_from_pdf(file)
            if text=='':
                text=pdftotxt(file,dirloc)
            return text
        
        elif file.lower().endswith('.doc'):
            command = [
                'libreoffice', 
                '--headless', 
                '--convert-to', 'docx', 
                '--outdir', dirloc, 
                file
                ]
            try:
                subprocess.run(command, check=True)
                print('Able to convert the doc file to the docx file ..............................')
            except:
                traceback.print_exc()
            # subprocess.check_output(['lowriter','--convert-to','docx','--outdir',dirloc,file])
            f_name =file.split('/')[-1].split('.')[0]
            print("f_name: ", f_name)
            f_name=f_name+'.docx'
            docx_path=os.path.join(dirloc,f_name)
            text = docx2txt.process(docx_path)
            try:
                os.remove(os.path.join(dirloc,f_name))
            except:
                traceback.print_exc()
            return text

    

def pdftotxt(file,dirloc):
    """ This function extract the text from the pdf file 
    Args:
        file (str): complete path of the file 
        dirloc (str):Path of the directory 

    Returns:
        text(str): A string consisting of the complete text from the pdf file 
    """
    text1 = ""
    pdfs = file
    time.sleep(3)
    file_rcount=0
    while file_rcount<5:
        try:
            pages = convert_from_path(pdfs, 350)
            file_rcount=5
            break
        except:
            traceback.print_exc()
            pass
        time.sleep(0.4)
        file_rcount+=1
        
    images=[]
    i = 1
    for page in pages:
        image_name =str(dirloc)+"/"+ "Page_" + str(i) + ".jpg"  
        page.save(image_name, "JPEG")
        image_name=cv2.imread(image_name)
        images.append(image_name)
          
        text=pytesseract.image_to_string(image_name)
        text1 = text1 + text
        try:
            image_name =str(dirloc)+"/"+ "Page_" + str(i) + ".jpg"  
            os.remove(image_name)
        except:
            pass
        i = i+1
    return text1

