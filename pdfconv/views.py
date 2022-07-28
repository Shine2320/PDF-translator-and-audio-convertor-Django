from django.shortcuts import render
from django.http import HttpResponse
import PyPDF2
from gtts import gTTS


def home(request):
    return render(request,'home.html')

def usersignup(request):
    if request.method == 'POST':
        
    return render(request,'usersignup.html')

def index(request):
    if request.method == "POST":

        print("hello")  
       # path of the PDF file
        path = open('pdfconv/static/pdf/file.pdf', 'rb')        
        # creating a PdfFileReader object
        pdfReader = PyPDF2.PdfFileReader(path)        
        # the page with which you want to start
        # this will read the page of 25th page.
        text =''
        count=pdfReader.numPages
        for i in range(count):
            from_page = pdfReader.getPage(i)
            # # extracting the text from the PDF
            text += from_page.extractText()        
        # reading the text
        tts = gTTS(text)
        tts.save("pdfconv/static/audio/hi.mp3")
    return render(request, 'index.html')

def about(request):

    return HttpResponse("<h1>About page</h1>")