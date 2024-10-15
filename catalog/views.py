from typing import Any
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


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