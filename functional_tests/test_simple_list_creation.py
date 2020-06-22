#from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

    
class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        #Edith has heard about a cool new online to-do app. She goes to checkout its homepage
        assert 1 == 1
        #print(self.live_server_url)
        self.browser.get(self.live_server_url)

        #She Notices the page title and headr mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        
        #She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
        
        
        #She typse "Buy peacock feathers: into a text box("Edith's hobby is tying fly-fishing lures)

        inputbox.send_keys('Buy peacock feathers')
        #when she hits enter, the page updates and how the page lists
        #"1: Buy peacock feathers" as an item in a to-do list

        inputbox.send_keys(Keys.ENTER)

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')

        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #self.fail('Finish the test!')
        #There is still a text box inviting her to add another item.She enters "User peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        
        #The page updates again and now shows both iterms on her list.

        #Edith wonders wherte the site will remember her list. Then she sees that the site has generated a unique URL for her -- There is some explanatory text to that effect.

        #She visits that URL - her to do list is still there.

        #Satisfied She goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Now a new user Francis comes along to the site.
        ## We use a new browser session to make sure that no information of Edith's is coming through from cookies etc.
        self.browser.quit()
        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options = options)

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis starts a new list by entering a new item. Ie is less interesting than Edith.
            
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Francis gets his own url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #Again there is no trace of Edith's list
            
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #satisfied both go to sleep
