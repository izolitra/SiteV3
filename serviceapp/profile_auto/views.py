from django.shortcuts import render

def profile_auto_home(request):
    return render(request, 'profile_auto/order_tracking.html')

def profile_auto_payment(request):
    return render(request, 'profile_auto/payment.html')