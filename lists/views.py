from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.conf import settings
from django.core.exceptions import ValidationError
from lists.forms import ItemForm, ITEM_EMPTY_ERROR

# Create your views here.

def home_page(request):
    return render(request,'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    error = None
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data = request.POST)
        if form.is_valid():
            item = Item(text = request.POST['text'], list = list_)
            item.save()
            return redirect(f'{settings.BASE_URL}/lists/{list_.id}/', {'form': form})
    return render(request, 'list.html', {'list': list_, 'error':error, 'form': form})

def new_list(request):
   #print(request.POST) 
   form = ItemForm(data = request.POST)
   if form.is_valid():
       list_ = List.objects.create()
       Item.objects.create(text = request.POST['text'], list = list_)
       return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')
   else:
       return render(request, 'home.html', {"form" : form, 'error': ITEM_EMPTY_ERROR})
#def add_item(request, list_id):
#    list_ = List.objects.get(id=list_id)
#    new_item_text = request.POST['item_text']
#    Item.objects.create(text = new_item_text, list = list_)
#    return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')

