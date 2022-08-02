from unittest import mock

import pytest

from qualitycheck.utils import send_email_message


@pytest.fixture()
def message_scaffold():
    message = 'Iodine is a chemical element with the symbol I and atomic number 53'
    incoming = {
        'message': message,
        'subject': 'Iodine',
        'email_from': 'pineapple@fruits.org',
        'email_to': 'key_lime@fruits.org',
        'smtp_server': 'smtp.fruits.org'
    }
    return incoming


@mock.patch('qualitycheck.utils.SMTP')
def test_send_email_message(smtp_mock, message_scaffold):
    send_email_message(**message_scaffold)
    smtp_mock.assert_called_with(message_scaffold['smtp_server'])
    smtp_mock.return_value.__enter__.return_value.send_message.assert_called_once()
