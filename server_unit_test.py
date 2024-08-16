import unittest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
import server
from datetime import datetime

class TestMQTTServer(unittest.TestCase):

    @patch('server.MongoClient')
    def test_callback(self, mock_mongo_client):
        # Mock MongoDB connection and collection
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value.mqtt_database = mock_db
        mock_db.mqtt_messages = mock_collection

        # Mock the message and delivery tag
        mock_ch = MagicMock()
        mock_method = MagicMock()
        mock_body = b'{"status": 3}'
        mock_properties = MagicMock()

        # Run the callback function
        with patch('server.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 8, 14, 10, 0, 0)
            server.callback(mock_ch, mock_method, mock_properties, mock_body)

            # Check that the message is stored in MongoDB with a timestamp
            mock_collection.insert_one.assert_called_with({
                'status': 3,
                'timestamp': datetime(2024, 8, 14, 10, 0, 0)
            })

            # Ensure the message was acknowledged
            mock_ch.basic_ack.assert_called_with(delivery_tag=mock_method.delivery_tag)

if __name__ == "__main__":
    unittest.main()
