from django.contrib import admin
from django import forms

from .models import *


# Register your models here.


class AuthorForm(forms.ModelForm):
	birth_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'), required=False)

	class Meta:
		model = Author
		fields = '__all__'
	# widgets = {
	# 	'birth_date': forms.DateInput(format='%d.%m.%Y'),
	# }


class AuthorModelAdmin(admin.ModelAdmin):
	form = AuthorForm


class BookAdmin(admin.ModelAdmin):
	class Meta:
		model: Book
		exclude = ["added"]


class OrderItemInLine(admin.TabularInline):
	model = OrderItem
	extra = 0


class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at')
	inlines = [OrderItemInLine]


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Rented)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Person)
admin.site.register(Order, CartAdmin)
admin.site.register(OrderItem)
admin.site.register(Author, AuthorModelAdmin)
admin.site.register(Reserved)
