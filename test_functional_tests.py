from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith has heard about a cool new online to-do app. She goes to checkout its homepage
        self.browser.get('http://localhost:8000')

        #She Notices the page title and headr mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        #She is invited to enter a to-do item straight away

        #She typse "Buy peacock feathers: into a text box("Edith's hobby is tying fly-fishing lures)

        #when she hits enter, the page updates and how the page lists
        #"1: Buy peacock feathers" as an item in a to-do list

        #There is still a text box inviting her to add another item.She enters "User peacock feathers to make a fly" (Edith is very methodical)

        #The page updates again and now shows both iterms on her list.

        #Edith wonders wherte the site will remember her list. Then she sees that the site has generated a unique URL for her -- There is some explanatory text to that effect.

        #She visits that URL - her to do list is still there.

        #Satisfied She goes back to sleep.

if __name__ == '__main__':
    unittest.main()
