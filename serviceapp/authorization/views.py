from django.contrib.auth import login
from .forms import MechanicRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import AvatarForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mechanic, Service
from django.contrib.auth import login, authenticate
from .forms import MechanicRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ServiceForm
from .models import Service, Mechanic
from .forms import AvatarForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from django.http import JsonResponse

'''
@login_required
def all_orders(request):
    # Получаем все заказы, которые имеют статус 'new'
    orders = Order.objects.filter(status='new')
    return render(request, 'main/all_orders.html', {'orders': orders})
'''

@login_required
def order_detail(request, order_id):
    # Получаем заказ по ID
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_detail.html', {'order': order})

@login_required
def take_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'new':
        order.mechanic = request.user.mechanic
        order.status = 'in_progress'
        order.save()
    return JsonResponse({'status': 'success', 'message': 'Order taken successfully!'})

@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.mechanic == request.user.mechanic and order.status == 'in_progress':
        order.status = 'completed'
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order completed successfully!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot complete this order.'})


@login_required
def update_avatar(request):
    mechanic = request.user.mechanic
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=mechanic)

        print("Form data:", request.POST)
        print("File data:", request.FILES)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print("Form errors:", form.errors)
    else:
        form = AvatarForm(instance=mechanic)

    return render(request, 'main/profile.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST' and 'avatar' in request.FILES:
        avatar = request.FILES['avatar']
        mechanic = Mechanic.objects.get(user=request.user)
        mechanic.avatar = avatar
        mechanic.save()
        return redirect('profile')

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            mechanic = Mechanic.objects.get(user=request.user)
            mechanic.avatar = avatar
            mechanic.save()

        category = request.POST.get('category')
        price = request.POST.get('price')
        if category and price:
            mechanic = Mechanic.objects.get(user=request.user)
            Service.objects.create(mechanic=mechanic, category=category, price=price)
            return redirect('profile')

        if 'delete_service' in request.POST:
            service_id = request.POST.get('service_id')
            if service_id:
                service = Service.objects.get(id=service_id)
                service.delete()
                return redirect('profile')


    mechanic = Mechanic.objects.get(user=request.user)
    services = Service.objects.filter(mechanic=mechanic)
    completed_orders = Order.objects.filter(mechanic=mechanic, status='completed')
    new_orders = Order.objects.filter(mechanic=mechanic).exclude(status='completed')


    orders = Order.objects.filter(mechanic=mechanic)

    return render(request, 'main/profile.html', {
        'user': request.user,
        'services': services,
        'mechanic': mechanic,
        'completed_orders': completed_orders,
        'new_orders': new_orders,
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
