import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from lord_of_the_rings_sdk.lord_of_the_rings_sdk import LordOfTheRingsSDK

class LordOfTheRingsSDKTest(unittest.TestCase):
    def setUp(self):
        self.api_key = 'DngPTqueCyI1fk6do2so'
        self.sdk = LordOfTheRingsSDK(self.api_key)

    @patch('lord_of_the_rings_sdk.lord_of_the_rings_sdk.requests.get')
    def test_get_movie_by_id(self, mock_get):
        expected_response = {
            'docs': [{
                '_id': '5cd95395de30eff6ebccde56',
            }]
        }
        mock_get.return_value.json.return_value = expected_response
        movie_id = '5cd95395de30eff6ebccde56'

        movie_endpoint = self.sdk.movie()
        movie = movie_endpoint.by_id(movie_id)

        mock_get.assert_called_once_with(f'https://the-one-api.dev/v2/movie/{movie_id}', headers={'Authorization': f'Bearer {self.api_key}'})
        self.assertEqual(movie['docs'][0]['_id'], expected_response['docs'][0]['_id'])

    @patch('lord_of_the_rings_sdk.lord_of_the_rings_sdk.requests.get')
    def test_get_quote_by_random(self, mock_get):
        expected_response = {
            'docs': [],
            'total': 2384,
            'limit': 1000,
            'offset': 0,
            'page': 1,
            'pages': 3
        }
        mock_get.return_value.json.return_value = expected_response

        quote_endpoint = self.sdk.quote()
        quotes = quote_endpoint.by_random()

        mock_get.assert_called_once_with('https://the-one-api.dev/v2/quote', headers={'Authorization': f'Bearer {self.api_key}'})
        self.assertEqual(quotes, expected_response)

    @patch('lord_of_the_rings_sdk.lord_of_the_rings_sdk.requests.get')
    def test_get_quote_by_id(self, mock_get):
        expected_response = {
            'docs': [{
                '_id': '5cd96e05de30eff6ebccebd0',
            }]
        }
        mock_get.return_value.json.return_value = expected_response
        quote_id = '5cd96e05de30eff6ebccebd0'

        quote_endpoint = self.sdk.quote()
        quote = quote_endpoint.by_id(quote_id)

        mock_get.assert_called_once_with(f'https://the-one-api.dev/v2/quote/{quote_id}', headers={'Authorization': f'Bearer {self.api_key}'})
        self.assertEqual(quote['docs'][0]['_id'], expected_response['docs'][0]['_id'])

    @patch('lord_of_the_rings_sdk.lord_of_the_rings_sdk.requests.get')
    def test_get_movie_list(self, mock_get):
        expected_response = {
            'docs': [],
            'total': 8
        }
        mock_get.return_value.json.return_value = expected_response

        movie_endpoint = self.sdk.movie()
        movies = movie_endpoint.by_list()

        mock_get.assert_called_once_with('https://the-one-api.dev/v2/movie', headers={'Authorization': f'Bearer {self.api_key}'})
        self.assertEqual(movies, expected_response)

    @patch('lord_of_the_rings_sdk.lord_of_the_rings_sdk.requests.get')
    def test_get_movie_id_quote(self, mock_get):
        expected_response = {
            'docs': [{
                '_id': '5cd96e05de30eff6ebccebd0',
                'movie': '5cd95395de30eff6ebccde5b',
            }]
        }
        mock_get.return_value.json.return_value = expected_response
        movie_id = '5cd95395de30eff6ebccde5b'

        movie_endpoint = self.sdk.movie()
        quotes = movie_endpoint.by_id_quote(movie_id)

        mock_get.assert_called_once_with(f'https://the-one-api.dev/v2/movie/{movie_id}/quote', headers={'Authorization': f'Bearer {self.api_key}'})
        self.assertEqual(quotes, expected_response)

if __name__ == '__main__':
    unittest.main()
