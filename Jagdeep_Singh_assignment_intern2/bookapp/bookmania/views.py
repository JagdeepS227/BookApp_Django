from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from django.contrib.sessions.models import Session;
Session.objects.all().delete()
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name= form.cleaned_data.get('name')
            phone=form.cleaned_data.get('phone')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            account_type = form.cleaned_data.get('account_type')
            group = Group.objects.get(name=account_type)
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            if account_type == "seller":
                Seller.objects.create(name=name,phone=phone,email=email)
            if account_type=="customer":
                Customer.objects.create(name=name,phone=phone,email=email)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            login(request, user)

            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):
	context = {}
	return render(request, 'user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def home(request):
    #orders = Order.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    sellers=Seller.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    orders=Order.objects.all().order_by('-date_created')[:5][::-1]
    context = {'orders':orders, 'customers':customers,'sellers':sellers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator','seller','customer'])
def books(request):
    books = Books.objects.all()
    return render(request, 'books.html', {'books':books})


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator','seller'])
def books_of_seller(request):
    seller = Seller.objects.get(email=request.user.email)
    books = Books.objects.filter(seller=seller)
    return render(request, 'books.html', {'books':books})




@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders=orders.count()
    order_count = orders.count()
    context = {'customer':customer,'total_orders':total_orders, 'orders':orders, 'order_count':order_count}
    return render(request, 'customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def seller(request,pk_test):
    seller = Seller.objects.get(id=pk_test)
    books = Books.objects.filter(seller=seller)
    total_books=books.count()
    context = {'seller':seller,'books':books,'total_books':total_books}
    return render(request, 'seller.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator','customer'])
def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('book',), extra=4 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = {'form':formset}
	return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def addBook(request,pk):
    OrderFormSet = inlineformset_factory(Seller, Books, fields=('name', 'author','price','num_copies','tags'), extra=4 )
    seller = Seller.objects.get(email=request.user.email)
    formset = OrderFormSet(queryset=Books.objects.none(),instance=seller)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=seller)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'form':formset}
    return render(request, 'add_books.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def updateBook(request, pk):
    book = Books.objects.get(id=pk)
    seller=Seller.objects.filter(email=request.user.email)
    form = BookForm(instance=book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            books2=Books.objects.filter(seller=seller[0])
            total_books=books2.count()
            return redirect('/')
            #return render(request,'seller.html',{'seller':seller,'total_books':total_books,'books':books2})
    context = {'form':form}
    return render(request, 'add_books.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def deleteBook(request, pk):
    book = Books.objects.get(id=pk)
    seller=Seller.objects.filter(email=request.user.email)
    if request.method == "POST":
        book.delete()
        return redirect('/')
    context = {'item':book}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'delete.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def deleteSeller(request):
    seller = Seller.objects.get(email=request.user.email)
    print(seller)
    if request.method == "POST":
        seller.delete()
        user=User.objects.filter(username=seller.name)
        user.delete()
        return redirect('logout')
    context = {'item':seller}
    return render(request, 'delete_seller.html', context)    


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteCustomer(request):
    customer = Customer.objects.get(email=request.user.email)
    print(customer,"TTTTTTTTTTTTTt")
    if request.method == "POST":
        customer.delete()
        user=User.objects.filter(username=customer.name)
        user.delete()
        return redirect('logout')
    context = {'item':customer}
    return render(request, 'delete_customer.html', context)    