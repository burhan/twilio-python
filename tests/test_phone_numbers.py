from __future__ import with_statement
import unittest

from mock import patch, Mock
from tests.tools import create_mock_json
from twilio.rest.http import HttpClient

from twilio.rest.resources import PhoneNumbers
from twilio.rest.resources import PhoneNumber


class PhoneNumberTest(unittest.TestCase):

    def setUp(self):
        self.client = HttpClient()
        self.parent = Mock()
        self.parent.client = self.client
        self.base_uri = 'http://api.twilio.com/Accounts/ac1'
        self.auth = ("AC123", "token")
        self.sid = 'phone_sid'

        self.list = PhoneNumbers(self.client, self.base_uri, self.auth)
        self.instance = PhoneNumber(self.list, self.sid)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_update_rename_status_callback_url(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        self.instance.update(
            status_callback_url="http://www.example.com").execute()

        uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, self.sid)

        data = {
            'StatusCallback': 'http://www.example.com'
        }
        mock.assert_called_with("POST",
                                uri,
                                data=data,
                                auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_application_sid(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        self.list.update(self.sid, application_sid="foo").execute()

        uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, self.sid)
        data = {
            "VoiceApplicationSid": "foo",
            "SmsApplicationSid": "foo"
        }
        mock.assert_called_with("POST", uri, data=data, auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_update_with_multiple_params(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        self.list.update(self.sid,
                         voice_application_sid="a",
                         sms_application_sid="b",
                         status_callback="c").execute()

        uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, self.sid)
        data = {
            "VoiceApplicationSid": "a",
            "SmsApplicationSid": "b",
            "StatusCallback": "c"
        }
        mock.assert_called_with("POST", uri, data=data, auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_list_transfer(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        self.list.transfer(self.sid, 'other_account').execute()

        uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, self.sid)
        data = {
            "AccountSid": "other_account"
        }
        mock.assert_called_with("POST", uri, data=data, auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_instance_transfer(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        self.instance.transfer('other_account').execute()

        uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, self.sid)
        data = {
            "AccountSid": "other_account"
        }
        mock.assert_called_with("POST", uri, data=data, auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_purchase_type(self, mock):
        resp = create_mock_json('tests/resources/'
                                'incoming_phone_numbers_instance.json')
        resp.status_code = 201
        mock.return_value = resp

        types = {'local': 'Local', 'mobile': 'Mobile', 'tollfree': 'TollFree'}
        for type in ('local', 'mobile', 'tollfree'):

            self.list.purchase(type=type, phone_number='888').execute()
            uri = '%s/IncomingPhoneNumbers/%s' % (self.base_uri, types[type])
            data = {
                'PhoneNumber': '888'
            }
            mock.assert_called_with("POST", uri, data=data, auth=self.auth,
                                    use_json_extension=True,
                                    client=self.client)


class IncomingPhoneNumbersTest(unittest.TestCase):

    def setUp(self):
        self.client = HttpClient()
        self.auth = ("user", "pass")
        self.resource = PhoneNumbers(
            self.client, "http://api.twilio.com", self.auth
        )

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_mobile(self, mock):
        response = create_mock_json('tests/resources/'
                                    'incoming_phone_numbers_list.json')
        response.status_code = 200
        mock.return_value = response

        self.resource.list(type='mobile').execute()

        uri = "http://api.twilio.com/IncomingPhoneNumbers/Mobile"
        mock.assert_called_with("GET", uri,
                                auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_local(self, mock):
        response = create_mock_json('tests/resources/'
                                    'incoming_phone_numbers_list.json')
        response.status_code = 200
        mock.return_value = response

        self.resource.list(type='local').execute()

        uri = "http://api.twilio.com/IncomingPhoneNumbers/Local"
        mock.assert_called_with("GET", uri,
                                auth=self.auth,
                                use_json_extension=True,
                                client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_toll_free(self, mock):
        response = create_mock_json('tests/resources/'
                                    'incoming_phone_numbers_list.json')
        response.status_code = 200
        mock.return_value = response

        self.resource.list(type='tollfree').execute()

        uri = "http://api.twilio.com/IncomingPhoneNumbers/TollFree"
        mock.assert_called_with("GET", uri,
                                auth=self.auth,
                                use_json_extension=True,
                                client=self.client)
