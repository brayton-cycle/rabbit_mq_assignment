import unittest
from unittest.mock import patch, MagicMock
import client
import json

class TestMQTTClient(unittest.TestCase):

    @patch('client.pika.BlockingConnection')
    @patch('client.time.sleep', return_value=None)
    def test_mqtt_producer(self, mock_sleep, mock_blocking_connection):
        # Mock the channel and connection
        mock_channel = MagicMock()
        mock_connection = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Run the client code
        with patch('client.random.randint', return_value=3):
            with patch('builtins.print') as mocked_print:
                client.mqtt_producer()

                # Check that the correct message is sent
                expected_message = json.dumps({'status': 3})
                mock_channel.basic_publish.assert_called_with(
                    exchange='',
                    routing_key='mqtt_queue',
                    body=expected_message,
                    properties=mock_channel.basic_publish.call_args[1]['properties']
                )

                # Check if the message is printed
                mocked_print.assert_called_with(f"Sent: {{'status': 3}}")

if __name__ == "__main__":
    unittest.main()
