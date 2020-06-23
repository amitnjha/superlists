from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email = email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        ## to set a cookie we need to first visit the domain.
        ## 404 page loads the quickest.

        self.browser.get(self.live_server_url + '/superlists' + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name = settings.SESSION_COOKIE_NAME,
            value = session.session_key,
            path = '/'
            ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

        self.add_list_item('Immanetize eschaton')
        self.add_list_item('Reticulate splines')
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My Lists').click()

        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Immanetize eschaton')
        )
        self.browser.find_element_by_link_text('Immanetize eschaton').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        #She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under My lists her new list appears
        self.browser.find_element_by_link_text('My Lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My Lists'),
            []
        ))
            
