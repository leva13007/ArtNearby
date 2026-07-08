from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomRegistrationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Реєстрація успішна!")

            # Handle additional fields based on user type
            if user_type == 'company':
                company_name = form.cleaned_data.get('company_name')
                address = form.cleaned_data.get('address')
                phone = form.cleaned_data.get('phone')
                tax_id = form.cleaned_data.get('tax_id')

                # Save company-specific data (you might want to create a CompanyProfile model)
                # Example: CompanyProfile.objects.create(user=user, company_name=company_name, ...)

            return redirect("index")
        else:
            messages.error(request, "Помилка при реєстрації. Перевірте дані.")
    else:
        form = CustomRegistrationForm()

    return render(
        request,
        template_name="find_it/auth_system/registrate.html",
        context={"form": form},
    )

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Ласкаво просимо, {username}!")
                return redirect("index")
            else:
                messages.error(request, "Невірне ім'я користувача або пароль")
    else:
        form = AuthenticationForm()

    return render(request, template_name="find_it/auth_system/login.html", context = {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Ви вийшли з облікового запису")
    return redirect("index")

def profile_view(request):
    "user = get_object_or_404(User, id=id)"
    return render(request, 'find_it/profile_show.html')