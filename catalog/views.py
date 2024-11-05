from typing import Any
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Cart, CartItem,Inventory
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
# For Graph
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import io
import base64
from django.contrib.auth.models import User

@login_required
@require_POST
def add_to_cart(request, isbn):
    try:
        data = json.loads(request.body)  # Parse the JSON request body
        quantity = data.get('quantity', 1)
        book = get_object_or_404(Book, isbn=isbn)

        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add item to cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        cart_item.quantity += quantity
        cart_item.save()
        
        return JsonResponse({'success': True, 'message': 'Book added to cart successfully!'})
    except Exception as e:
        # Ensure that all exceptions also return a JSON response
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    total_price = sum(item.book.price * item.quantity for item in cart_items)

    return render(request, 'catalog/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})


# Create your views here.

def index(request):
    """View function for home page of site."""
    num_books= Book.objects.all().count()
    num_instances= BookInstance.objects.all().count()

    num_instances_available= BookInstance.objects.filter(status__exact='a').count()

    num_authors=Author.objects.count()

    num_genres=Genre.objects.filter(name__contains='F').count()

    num_books_contain_cabin=Book.objects.filter(title__contains='Cabin').count()
    context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_contain_cabin': num_books_contain_cabin,
    }

    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    template_name='books/BookListView.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        
        context= super(BookListView,self).get_context_data(**kwargs)

        context['some data']='This is some data'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model= Author

class AuthorDetailView(generic.DetailView):
    model= Author



def books_per_author(request):
    # Get the count of books per author
    authors = Author.objects.annotate(num_books=Count('book')).order_by('last_name')
    
    # Prepare data for the graph
    author_names = [f"{author.first_name} {author.last_name}" for author in authors]
    num_books = [author.num_books for author in authors]
    
    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.bar(author_names, num_books, color='skyblue')
    plt.xlabel('Authors')
    plt.ylabel('Number of Books')
    plt.title('Number of Books per Author')
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Encode the image to display in the template
    image_png = buf.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')  # Encode to base64

    return render(request, 'books_per_author.html', {'graph': graph})

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-books'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

from django.contrib.auth.mixins import PermissionRequiredMixin

class view_loaned_book_librarian(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to librarian."""

    permission_required='catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.all()
            .filter(status__exact='o')
            .order_by('due_back')
        )


def update_inventory(book_isbn, quantity_change):
    """Update inventory for a specific book based on ISBN."""
    # Get the book instance using the ISBN
    book = get_object_or_404(Book, isbn=book_isbn)
    
    # Get the associated inventory item
    inventory = get_object_or_404(Inventory, book=book)
    
    # Calculate the new quantity available
    new_quantity = inventory.quantity_available + quantity_change
    
    # Check if new quantity is sufficient
    if new_quantity < 0:
        return JsonResponse({'success': False, 'error': 'Insufficient inventory.'})

    # Update the inventory quantity
    inventory.quantity_available = new_quantity
    inventory.save()
    
    return JsonResponse({'success': True, 'quantity_available': inventory.quantity_available})

@login_required
@require_POST
def checkout(request):
    try:
        data = json.loads(request.body)
        items = data.get('items', [])

        # Process each cart item using the book's ISBN
        for item in items:
            book_isbn = item['book_isbn']  # Change this to book_isbn
            quantity = int(item['quantity'])  # Ensure quantity is an integer

            # Get the cart item using the book's ISBN
            cart_item = get_object_or_404(CartItem, book__isbn=book_isbn)
            
            # Update inventory: decrease available quantity
            update_inventory(book_isbn, -quantity)

        return JsonResponse({'success': True, 'message': 'Checkout completed successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


    

@login_required
def checkout_success(request):
    return render(request, 'catalog/checkout_success.html')

from decimal import Decimal

@login_required
@require_POST
def update_cart_item_quantity(request):
    try:
        data = json.loads(request.body)  # Parse the JSON request body
        book_isbn = data.get('book_isbn')
        quantity = int(data.get('quantity', 1))  # Convert quantity to an integer

        # Get the cart item by book ISBN
        cart_item = get_object_or_404(CartItem, book__isbn=book_isbn, cart__user=request.user)
        
        # Update the quantity
        cart_item.quantity = quantity
        cart_item.save()

        # Calculate new total price for this item
        # Ensure that the price is treated as a Decimal
        total_price = cart_item.book.price * Decimal(cart_item.quantity)

        return JsonResponse({'success': True, 'total_price': total_price.quantize(Decimal('0.01'))})  # Format to 2 decimal places
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
from .forms import UserRegistrationForm
from django.contrib.auth import login
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect(reverse('books'))  # Redirect to a desired page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'catalog/register.html', {'form': form})