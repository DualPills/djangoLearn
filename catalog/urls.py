from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('cart/add/<str:isbn>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_detail, name='cart-detail'),
    path('books-per-author/', views.books_per_author, name='books_per_author'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed-books/', views.view_loaned_book_librarian.as_view(), name='borrowed-books'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/checkout/success/', views.checkout_success, name='checkout-success'),
    path('update-cart-item/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('register/', views.register, name='register'),
]
