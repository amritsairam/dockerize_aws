# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.contrib.auth import logout

# #username amrits password hiranmayi
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from main import rag
from .forms import DocumentQueryForm

# def index(request):
#     if request.user.is_anonymous:
#         return redirect('/login')
#     return render(request, 'index.html')

def index(request):
    if request.user.is_anonymous:
        return redirect('/login')

    if request.method == 'POST':
        form = DocumentQueryForm(request.POST, request.FILES)
        if form.is_valid():
            query = form.cleaned_data['query']
            pdf = request.FILES['pdf']

            # Save the uploaded PDF to a temporary location
            pdf_path = f'/tmp/{pdf.name}'
            with open(pdf_path, 'wb') as temp_pdf:
                for chunk in pdf.chunks():
                    temp_pdf.write(chunk)

            # Get the answer using the rag function
            answer = rag(pdf_path, query)

            return render(request, 'result.html', {'answer': answer})
    else:
        form = DocumentQueryForm()
    
    return render(request, 'index.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/login')

# Create your views here.
