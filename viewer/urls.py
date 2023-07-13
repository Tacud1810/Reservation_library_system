from django.urls import path
from .views import *

urlpatterns = [
	path("", new_books, name='home'),
	path("index/", new_books, name='home'),

	path("book/<pk>/", book, name='book'),
	path("books_page/", books_page, name='books_page'),
	path("authors/", AuthorsView.as_view(), name='authors'),

	path("cart/", cart, name='cart'),
	path("order_done/", order_done, name='order_done'),
	path("update_item/", update_item, name='update_item'),

]
