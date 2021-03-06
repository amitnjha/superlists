from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http  import HttpRequest
from lists.models import Item, List
from django.conf import settings
from django.utils.html import escape
from lists.forms import ItemForm, ITEM_EMPTY_ERROR, ExistingListItemForm
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve(f'{settings.BASE_URL}/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        
        response = self.client.get(f'{settings.BASE_URL}/')
        html = response.content.decode('utf8')
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>\n'))

        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response =  self.client.get(f'{settings.BASE_URL}/')
        self.assertIsInstance(response.context['form'], ItemForm)

        
class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'{settings.BASE_URL}/lists/{list_.id}/',
            data = {'text' : ''}
        )
    
    def test_display_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='item 1', list = list_)
        Item.objects.create(text='item 2', list = list_)

        other_list = List.objects.create()
        Item.objects.create(text='item 11', list = other_list)
        Item.objects.create(text='item 22', list = other_list)

        response = self.client.get(f'{settings.BASE_URL}/lists/{list_.id}/')
        
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 11')
        self.assertNotContains(response, 'item 22')
        
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'{settings.BASE_URL}/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'{settings.BASE_URL}/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'{settings.BASE_URL}/lists/{correct_list.id}/', data = {'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response  = self.client.post(f'{settings.BASE_URL}/lists/{correct_list.id}/', data = {'text': 'A new item for an existing list'})

        self.assertRedirects(response, f'{settings.BASE_URL}/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        #expected_error = escape("You can't have an empty list item")
        self.assertContains(response, ITEM_EMPTY_ERROR)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'{settings.BASE_URL}/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        response = self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertContains(response, ITEM_EMPTY_ERROR)
        
        
class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':'A new list item'})
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertRedirects(response, f'{settings.BASE_URL}/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':''})
        self.assertContains(response, ITEM_EMPTY_ERROR)

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email = 'a@b.com')
        self.client.force_login(user)
        self.client.post(f'{settings.BASE_URL}/lists/new', data = {'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)
        
        

class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get(f'{settings.BASE_URL}/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        wrong_user = User.objects.create(email = 'wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
    
