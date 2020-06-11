from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/superlists/accounts/send_login_email', data = {
            'email': 'edith@example.com'
            })
        self.assertRedirects(response, '/superlists/')

    @patch('accounts.views.send_mail')
    def test_sends_email_to_address_from_post(self, mock_send_mail):
        self.client.post('/superlists/accounts/send_login_email', data={
            'email': 'edith@example.com'
            })
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])


    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post('/superlists/accounts/send_login_email',
                                    data={
            'email': 'edith@example.com'
            })
        expected = "Check your email, we have sent you a link you can use to log in"
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected),
            )

    def test_creates_token_associated_with_email(self):
        self.client.post('/superlists/accounts/send_login_email', data={
            'email': 'edith@example.com'
            })
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')    
    def test_sends_links_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/superlists/accounts/send_login_email', data={
            'email': 'edith@example.com'
            })
        token = Token.objects.first()
        expected_url = f'http://testserver/superlists/accounts/login?token={token.uid}'
        #print('expected_url',expected_url)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
        
    
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/superlists/accounts/login?token=abc123')
        self.assertRedirects(response, '/superlists/')
        
