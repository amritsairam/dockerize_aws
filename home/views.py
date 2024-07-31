# #username amrits password hiranmayi
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from main import rag
from .forms import DocumentQueryForm

def index(request):
    """
    Handles the main application page where users can upload a PDF and submit a query.
    
    If the user is not authenticated, they are redirected to the login page.
    On a POST request, it processes the form, saves the uploaded PDF to a temporary
    location, and retrieves an answer using the `rag` function. The result is then
    rendered on a 'result.html' template.
    
    If the request method is GET, it displays the form for user input on the 'index.html' template.
    
    Args:
        request (HttpRequest): The request object containing metadata about the request.
        
    Returns:
        HttpResponse: Renders 'index.html' with the form if GET, or 'result.html' with the answer if POST.
    """
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
    """
    Handles user authentication and login.
    
    On a POST request, it authenticates the user with the provided username and password.
    If authentication is successful, the user is logged in and redirected to the main application page.
    If authentication fails, an error message is displayed on the 'login.html' template.
    
    Args:
        request (HttpRequest): The request object containing metadata about the request.
        
    Returns:
        HttpResponse: Renders 'login.html' with an error message if authentication fails, or redirects to '/' if successful.
    """
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
    """
    Logs out the current user and redirects to the login page.
    
    Args:
        request (HttpRequest): The request object containing metadata about the request.
        
    Returns:
        HttpResponse: Redirects to the '/login' URL after logging out.
    """
    logout(request)
    return redirect('/login')

# Create your views here.
