from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import json

from .models import *


# Create your views here.


def home(request):
	return render(request, template_name='index.html')


def book(request, pk):
	book = Book.objects.get(id=pk)
	genre = Genre.objects.filter(genres=book)
	genre_ids = genre.values_list('id', flat=True)
	similars = Book.objects.filter(genre__in=genre_ids).exclude(id=pk).order_by('?').distinct()[:4]
	if request.user.is_authenticated:
		customer = request.user.person
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items': 0}
	context = {'book': book, 'genres': genre, 'similars': similars, 'items': items, 'order': order}
	return render(request, template_name='book.html', context=context)


def new_books(request):
	book_list = Book.objects.all().order_by('-added')
	genres_list = Genre.objects.all()
	if request.user.is_authenticated:
		customer = request.user.person
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items': 0}
	context = {'new_books': book_list, 'genres': genres_list, 'items': items, 'order': order}
	return render(request, template_name='index.html', context=context)


def books_page(request):
	book_list = Book.objects.all().order_by('-id')
	genres_list = Genre.objects.all()
	if request.user.is_authenticated:
		customer = request.user.person
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items': 0}
	context = {'books': book_list, 'genres': genres_list, 'items': items, 'order': order}
	return render(request, template_name='books.html', context=context)


class AuthorsView(TemplateView):
	template_name = 'authors.html'
	author_list = Author.objects.all().order_by('name')
	genres_list = Genre.objects.all()
	paginator = Paginator(author_list, 5)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page_number = self.request.GET.get('page')
		page_object = self.paginator.get_page(page_number)
		context['authors'] = page_object
		context['genres'] = self.genres_list
		return context


def cart(request):
	return render(request, template_name='cart.html')


def order_done(request):
	customer = request.user.person
	order, created = Order.objects.get_or_create(user=customer, complete=False)
	order.complete = True
	order.save()

	return render(request, template_name='order_done.html')


# class AddToCartForm(forms.Form):
# 	book = forms.ModelChoiceField(queryset=Book.objects.all())


# def add_to_cart(request):
# 	if request.method == 'POST':
# 		form = AddToCartForm(request.POST)
# 		if form.is_valid():
# 			product = form.cleaned_data['product']
#
# 			return redirect('cart')
# 	else:
# 		form = AddToCartForm()
# 	return render(request, 'cart.html', {'form': form})


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.person
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items': 0}
	context = {'items': items, 'order': order}
	return render(request, 'cart.html', context)


def update_item(request):
	data = json.loads(request.body)
	book_id = data['bookId']
	action = data['action']

	customer = request.user.person
	book = Book.objects.get(id=book_id)
	print(book)
	print(action)
	order, created = Order.objects.get_or_create(user=customer, complete=False)

	order_item, created = OrderItem.objects.get_or_create(cart=order, book=book)

	print(book.amount)
	if book.amount > 0:
		order_item.save()
		book.amount -= 1
		book.save()
	if action == 'remove':
		order_item.delete()
		book.amount +=1
		book.save()
	if action == 'reserve':
		book, created = Reserved.objects.get_or_create(id_user=customer, id_book=book)

	return JsonResponse('Item was added', safe=False)
