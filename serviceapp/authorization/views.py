from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import MechanicRegistrationForm, MechanicAuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceForm, OrderForm
from .models import Service, Order, Mechanic


@login_required
def mechanic_dashboard(request):
    mechanic = get_object_or_404(Mechanic, user=request.user)
    services = mechanic.services.all()
    orders = mechanic.orders.all()

    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.mechanic = mechanic
            service.save()
            return redirect('mechanic_dashboard')
    else:
        service_form = ServiceForm()

    return render(request, 'main/mechanic_dashboard.html', {
        'services': services,
        'orders': orders,
        'service_form': service_form,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        if 'start' in request.POST:
            order.status = 'in_progress'
        elif 'complete' in request.POST:
            order.status = 'completed'
        order.save()
        return redirect('mechanic_dashboard')

    return render(request, 'main/order_detail.html', {'order': order})

@login_required
def profile_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        price = request.POST.get('price')
        if category and price:
            # Сохранение новой услуги
            Service.objects.create(user=request.user, category=category, price=price)
            return redirect('profile')  # Перезагрузка страницы

    # Получение списка услуг для текущего пользователя
    services = Service.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {
        'user': request.user,
        'services': services,
    })

def doLogout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = MechanicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            print(form.errors)
    else:
        form = MechanicRegistrationForm()

    return render(request, "main/registration.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'main/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})
