import requests

class LordOfTheRingsSDK:
    """
    LordOfTheRingsSDK class provides access to the Lord of the Rings API endpoints for movies and quotes.
    """

    def __init__(self, api_key):
        """
        Initialize the LordOfTheRingsSDK with the provided API key.

        Args:
            api_key (str): The API key for authentication.
        """
        self.api_key = api_key
        self.base_url = 'https://the-one-api.dev/v2'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def movie(self):
        """
        Get an instance of the MovieEndpoint class.

        Returns:
            MovieEndpoint: An instance of the MovieEndpoint class.
        """
        return MovieEndpoint(self.api_key, self.base_url, self.headers)

    def quote(self):
        """
        Get an instance of the QuoteEndpoint class.

        Returns:
            QuoteEndpoint: An instance of the QuoteEndpoint class.
        """
        return QuoteEndpoint(self.api_key, self.base_url, self.headers)


class MovieEndpoint:
    """
    MovieEndpoint class provides methods to interact with the movie endpoint of the Lord of the Rings API.
    """

    def __init__(self, api_key, base_url, headers):
        """
        Initialize the MovieEndpoint with the provided API key, base URL, and headers.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL of the API.
            headers (dict): The headers for the API requests.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = headers

    def by_list(self):
        """
        Get a list of movies.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = 'movie'
        return self._make_request(endpoint)

    def by_id(self, movie_id):
        """
        Get a specific movie by its ID.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = f'movie/{movie_id}'
        return self._make_request(endpoint)
    
    def by_id_quote(self, movie_id):
        """
        Get quotes for a specific movie by its ID.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = f'movie/{movie_id}/quote'
        return self._make_request(endpoint)

    def _make_request(self, endpoint):
        """
        Make an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to make the request to.

        Returns:
            dict: A dictionary containing the response from the API.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
        """
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class QuoteEndpoint:
    """
    QuoteEndpoint class provides methods to interact with the quote endpoint of the Lord of the Rings API.
    """

    def __init__(self, api_key, base_url, headers):
        """
        Initialize the QuoteEndpoint with the provided API key, base URL, and headers.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL of the API.
            headers (dict): The headers for the API requests.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = headers

    def by_random(self):
        """
        Get random quotes.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = 'quote'
        return self._make_request(endpoint)

    def by_id(self, quote_id):
        """
        Get a specific quote by its ID.

        Args:
            quote_id (str): The ID of the quote.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = f'quote/{quote_id}'
        return self._make_request(endpoint)

    def _make_request(self, endpoint):
        """
        Make an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to make the request to.

        Returns:
            dict: A dictionary containing the response from the API.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
        """
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
