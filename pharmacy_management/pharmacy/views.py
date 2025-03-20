from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import Medicine, Billing
from .forms import UserRegisterForm



def home(request):
    return render(request, 'pharmacy/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserRegisterForm()

    return render(request, 'pharmacy/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                
                
                next_url = request.GET.get('next', 'medicine_list')
                return redirect(next_url)  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')

    else:
        form = AuthenticationForm()

    return render(request, 'pharmacy/login.html', {'form': form})



def custom_logout(request):
    logout(request)
    
    
    
    return redirect('home')



@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/medicine_list.html', {'medicines': medicines})



@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'pharmacy/medicine_detail.html', {'medicine': medicine})



@login_required
@transaction.atomic  
def billing(request):
    medicines = Medicine.objects.all()

    if request.method == "POST":
        customer = request.POST.get('customer')
        medicine_id = request.POST.get('medicine')
        quantity_str = request.POST.get('quantity')

        
        if not quantity_str.isdigit():
            messages.error(request, "Invalid quantity. Please enter a valid number.")
            return redirect('billing')

        quantity = int(quantity_str)

        
        medicine = get_object_or_404(Medicine, id=medicine_id)

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('billing')

        if medicine.quantity < quantity:
            messages.error(request, "Not enough stock available.")
            return redirect('billing')

        
        total_price = medicine.price * quantity

        
        medicine.quantity -= quantity
        medicine.save()

        
        bill = Billing.objects.create(
            customer=customer,
            medicine=medicine,
            quantity=quantity,
            total_price=total_price,
            date=now()
        )

        messages.success(request, "Bill generated successfully!")

        
        return redirect('bill_detail_view', pk=bill.pk)

    return render(request, 'pharmacy/billing.html', {'medicines': medicines})



@login_required
def bill_detail(request):
    bills = Billing.objects.all().order_by('-date')
    return render(request, 'pharmacy/bill_detail.html', {'bills': bills})


# ✅ Bill Detail View (requires login)
@login_required
def bill_detail_view(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    return render(request, 'pharmacy/bill_detail_view.html', {'bill': bill})
