from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your views here.

def home_page(request):
    return render(request,'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    error = None
    if request.method == 'POST':
        item = Item(text = request.POST['item_text'], list = list_)
        try:
            item.full_clean()
            item.save()
            return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')
        except ValidationError:
            error  = "You can't have an empty list item"
    return render(request, 'list.html', {'list': list_, 'error':error})

def new_list(request):
   new_item_text = request.POST['item_text']
   list_ = List.objects.create()
   item = Item(text = new_item_text, list = list_)
   try:
       item.full_clean()
       item.save()
   except ValidationError:
       list_.delete()
       return render(request, 'home.html', {'error':"You can't have an empty list item"})
   
   return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')

#def add_item(request, list_id):
#    list_ = List.objects.get(id=list_id)
#    new_item_text = request.POST['item_text']
#    Item.objects.create(text = new_item_text, list = list_)
#    return redirect(f'{settings.BASE_URL}/lists/{list_.id}/')

