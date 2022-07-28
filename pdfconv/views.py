from django.shortcuts import render,redirect
from django.http import HttpResponse
import PyPDF2
from gtts import gTTS
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout 

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
				return redirect("home")
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