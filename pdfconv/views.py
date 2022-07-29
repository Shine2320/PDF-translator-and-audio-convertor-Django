from lib2to3.pytree import convert
import mimetypes
from os import stat
from django.shortcuts import render,redirect
from django.http import HttpResponse
import PyPDF2
from datetime import datetime
from gtts import gTTS
from django.contrib.auth.models import User
from pdfconv.functions import handle_uploaded_file
from pdfconv.models import UserAudio, UserPDF
from .forms import NewUserForm, PDFForm, PDFtranslate
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout 
from django.utils.crypto import get_random_string
from googletrans import Translator

def home(request):
    return render(request,'home.html')

def usersignup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="usersignup.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)            
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("user_home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")


def user_home(request):
    
    return render(request, 'user_home.html')
def user_pdf_upload(request):
    if request.method == 'POST':  
        pdf_upload = PDFForm(request.POST, request.FILES)  
        if pdf_upload.is_valid(): 
            user_pdf=UserPDF()
            unique_id = get_random_string(length=32)
            request.session['unique_id'] = unique_id
            print(unique_id)
            user_instance=User.objects.get(id=request.user.id)
            user_pdf.user = user_instance
            user_pdf.unique_id = unique_id #add this line
            user_pdf.pdffile = request.FILES['file']
            user_pdf.save()
            handle_uploaded_file(request.FILES['file']) 
            user_file_name=UserPDF.objects.values('pdffile').filter(user=request.user.id,unique_id=unique_id)  
            # path of the PDF file
            path = open("media/"+user_file_name[0]['pdffile'], 'rb')        
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
            filename=user_file_name[0]['pdffile']
            dummy,filename=filename.split('/')
            filename,dummy=filename.split('_')
            tts = gTTS(text)
            tts.save("media/audio/"+filename+"converted.mp3")
            audio_save=UserAudio()
            audio_save.pdf=user_pdf
            audio_save.filename=filename+"converted.mp3"
            audio_save.save()
            status="success" 
            messages.success(request, "PDF Converted Successfully" )
            return render(request,"user_pdf_upload.html",context={'pdf_upload':pdf_upload,'status':status})
    else:
        pdf_upload = PDFForm()  
        return render(request,"user_pdf_upload.html",context={'pdf_upload':pdf_upload})
      
def user_audio_play(request):
    user_file_name=UserAudio.objects.values('filename').filter(pdf__user=request.user.id,pdf__unique_id=request.session['unique_id'])
    filename = user_file_name[0]['filename']
    return render(request,"user_audio_play.html",context={'filename':filename})
    
def user_audio_download(request):
    user_file_name=UserAudio.objects.values('filename').filter(pdf__user=request.user.id,pdf__unique_id=request.session['unique_id'])
    path = open("media/audio/"+user_file_name[0]['filename'], 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type("media/audio/"+user_file_name[0]['filename'])
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    filename=user_file_name[0]['filename']
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    messages.success(request, "Audio File Has Started Downloading" )
    # Return the response value
    return response

def user_pdf_translate(request):
    if request.method == 'POST':
        pdf_upload = PDFtranslate(request.POST, request.FILES)  
        if pdf_upload.is_valid(): 
            user_pdf=UserPDF()
            unique_id = get_random_string(length=32)
            request.session['unique_id'] = unique_id
            print(unique_id)
            user_instance=User.objects.get(id=request.user.id)
            user_pdf.user = user_instance
            user_pdf.unique_id = unique_id #add this line
            user_pdf.pdffile = request.FILES['file']
            user_pdf.save()
            handle_uploaded_file(request.FILES['file']) 
            user_file_name=UserPDF.objects.values('pdffile').filter(user=request.user.id,unique_id=unique_id)  
            # path of the PDF file
            path = open("media/"+user_file_name[0]['pdffile'], 'rb')  
            pdfReader = PyPDF2.PdfFileReader(path)
            # count=pdfReader.numPages
            # for i in range(count):
            text =''
            count=pdfReader.numPages

            for i in range(count):
                from_page = pdfReader.getPage(i)
                # # extracting the text from the PDF
                text += from_page.extractText()
            translator = Translator(service_urls=['translate.googleapis.com'])
            data=translator.translate(text,dest=request.POST['to_language'])
            print(data.text)
            text = data.text
            form = PDFtranslate()
            messages.success(request, "PDF Translated Successfully" )
            return render(request, 'user_pdf_translate.html',context={'text':text,'translate':form })
    form = PDFtranslate()
    return render(request, 'user_pdf_translate.html',context={'translate':form})

