#from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #Edith goes to the home page and accidently tries to submit an empty list item. She hits enter on empty box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        #The browser intercepts the error and does not load the list page
        #The homepage refreshes and there is an error message saying that list items cannot be blank
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        
        # She tries again with some text for the item which now works
        # Perversely she decides to sumit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # She receives a similar warning on the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make Tea')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make Tea')
        
    def test_cannot_add_duplicate_items(self):
        #Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy Wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Wellies')

        #She accidently tries to enter a duplicate name
        self.get_item_input_box().send_keys('Buy Wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        #self.wait_for_row_in_list_table('1: Buy Wellies')

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Duplicate items not allowed"
        ))
