# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
import json
from main import start_pubsub_listener, send_sms
from main import SMS_API_URL

class TestStartPubsubListener(unittest.TestCase):
    @patch('main.requests.post')
    @patch('main.pubsub_v1.SubscriberClient')
    def test_start_pubsub_listener(self, MockSubscriberClient, mock_post):
        print(f"TestStartPubsubListener mock_post   : {mock_post}")
        # Arrange

        headers = {'Content-Type': 'application/json'}
        payload = {'message': 'Hello, World!', 'to': '+1234567890'}
        
        # Mock the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response

        # Mock the SubscriberClient and its methods
        mock_subscriber = MockSubscriberClient.return_value
        mock_subscription_path = 'projects/my-project/subscriptions/my-subscription'
        
        # Mock the subscription_path method to return the mock_subscription_path
        mock_subscriber.subscription_path.return_value = mock_subscription_path
        
        # Create a mock future object
        mock_future = MagicMock()
        mock_future.result.side_effect = KeyboardInterrupt  # Simulate a KeyboardInterrupt to exit the loop
        
        # Mock the subscribe method to call the callback with a fake message and return the mock future
        def mock_subscribe(subscription_path, callback):
            # Create a fake message
            fake_message = MagicMock()
            fake_message.data = b'{"message": "Hello, World!", "to": "+1234567890"}'
            fake_message.ack_id = 'test-ack-id'
            
            # Call the callback with the fake message
            callback(fake_message)
            
            return mock_future
        
        mock_subscriber.subscribe.side_effect = mock_subscribe

        # Act
        start_pubsub_listener()

        # Assert
        mock_subscriber.subscribe.assert_called_once_with(mock_subscription_path, callback=unittest.mock.ANY)
        #mock_post.assert_called_once_with(SMS_API_URL, headers=headers, data=json.dumps(payload))

class TestSendSms(unittest.TestCase):
    @patch('main.SMS_API_URL', new='https://api.example.com/send_sms')
    @patch('main.requests.post')
    def test_send_sms(self, mock_post):
        print(f"TestSendSms mock_post: {mock_post}")
        # Arrange
        headers = {'Content-Type': 'application/json'}
        payload = {'message': 'Hello, World!', 'to': '+1234567890'}
        
        # Mock the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response
        
        # Act
        response = send_sms('+1234567890', headers, payload)
        
        print(f"response: {response}")
        # Assert
        calls = [call[0][0] for call in mock_post.call_args_list]
        self.assertIn('https://api.example.com/send_sms', calls)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})


if __name__ == '__main__':
    unittest.main()