from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.conf import settings
# Create your views here.

def home_page(request):
    return render(request,'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
   new_item_text = request.POST['item_text']
   list_ = List.objects.create()
   Item.objects.create(text = new_item_text, list = list_)
   return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item_text = request.POST['item_text']
    Item.objects.create(text = new_item_text, list = list_)
    return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')

