from django.shortcuts import render
from authorization.models import Mechanic
from authorization.models import Order
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from authorization.models import Service

def mechanic_detail(request, mechanic_id):
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    services = mechanic.services.all()
    return render(request, 'main/mechanic_detail.html', {'mechanic': mechanic, 'services': services})


def create_order(request):
    if request.method == 'POST':
        mechanic_id = request.POST.get('mechanic_id')
        service1_id = request.POST.get('service1')
        service2_id = request.POST.get('service2')
        payment_method = request.POST.get('payment_method')
        address = request.POST.get('address')

        mechanic = get_object_or_404(Mechanic, id=mechanic_id)

        service1 = get_object_or_404(Service, id=service1_id) if service1_id != '0' else None
        service2 = get_object_or_404(Service, id=service2_id) if service2_id != '0' else None

        service_description = ""
        total_price = 0

        if service1:
            service_description += f"Услуга 1: {service1.category} ({service1.price} ₽)"
            total_price += service1.price
        if service2:
            if service_description:
                service_description += ", "
            service_description += f"Услуга 2: {service2.category} ({service2.price} ₽)"
            total_price += service2.price

        # Формируем описание с оплатой и адресом
        payment_method_description = "1. Наличные" if payment_method == "1" else "2. Безналичный расчет"
        description = f"{service_description}, Оплата: {total_price} ₽, Способ оплаты: {payment_method_description}"

        order = Order.objects.create(
            mechanic=mechanic,
            customer_name=request.user.username if request.user.is_authenticated else "Гость",
            description=description,
            status='new',
        )

        return redirect('mechanic_detail', mechanic_id=mechanic.id)

    return redirect('applications_page')


def mechanics_list(request):
    mechanics = Mechanic.objects.all()
    return render(request, 'main/mechanics_list.html', {'mechanics': mechanics})

def profile_auto_payment(request):
    mechanic_id = request.GET.get('mechanic_id')  # Получаем ID механика
    mechanic = Mechanic.objects.get(id=mechanic_id)  # Получаем механика
    return render(request, 'profile_auto/payment.html', {'mechanic': mechanic})

def index(request):
    return render(request, 'main/index.html')

def applications(request):
    mechanics = Mechanic.objects.all()  # получаем всех механиков
    return render(request, 'main/applications.html', {'mechanics': mechanics})
