from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Book, CartItem, Order, OrderItem
from .forms import UserUpdateForm


def book_list(request):
    books = Book.objects.all()
    return render(request, 'echo/book_list.html', {'books': books})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'echo/book_form.html', {'form': form})


@staff_member_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'echo/book_form.html', {'form': form})


@staff_member_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'echo/book_confirm_delete.html', {'book': book})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'echo/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'echo/register.html', {'form': form})


@login_required
def account_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'echo/account.html', {'form': form})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'echo/cart.html', {'items': items, 'total': total})

@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart_view')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
    cart_items.delete()
    return redirect('order_success')  # перенаправляем на страницу успеха


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'echo/orders.html', {'orders': orders})


@login_required
def profile_view(request):
    return render(request, 'echo/profile.html', {'user': request.user})



def order_success(request):
    return render(request, 'echo/order_success.html')

def cart_detail(request):
    # твоя логика вывода корзины
    return render(request, 'echo/cart_detail.html', {'cart': ...})

def logout_view(request):
    logout(request)
    return redirect('login')
