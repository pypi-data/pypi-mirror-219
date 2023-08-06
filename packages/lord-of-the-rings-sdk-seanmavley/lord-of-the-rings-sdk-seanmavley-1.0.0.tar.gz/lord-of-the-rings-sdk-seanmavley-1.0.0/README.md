# Lord of the Rings SDK

The Lord of the Rings SDK provides a convenient way to access the Lord of the Rings API endpoints for movies and quotes. This SDK allows developers to retrieve information about movies and quotes from the Lord of the Rings series.

## Installation

You can install the Lord of the Rings SDK using `pip`. Open a terminal and run the following command:

```shell
pip install lord-of-the-rings-sdk
```

### Usage

To use the Lord of the Rings SDK in your Python project, follow these steps:

1. Import the necessary classes from the SDK:

```python
from lord_of_the_rings_sdk import LordOfTheRingsSDK
```

2. Initialize the LordOfTheRingsSDK class with your API key:

```python
api_key = 'your-api-key'
sdk = LordOfTheRingsSDK(api_key)
```

3. Use the `movie` and `quote` methods of the SDK to access the respective endpoints:

```python
# Get a list of movies
movies = sdk.movie().by_list()

# Get movie by ID
movie_id = '5cd95395de30eff6ebccde56'
movie = sdk.movie().by_id(movie_id)

# Get quotes by random
quotes = sdk.quote().by_random()

# Get quote by ID
quote_id = '5cd95395de30eff6ebccde56'
quote = sdk.quote().by_id(quote_id)
```

### Testing

The Lord of the Rings SDK includes a set of unit tests to ensure its functionality. To run the tests, follow these steps:

1. Install the testing dependencies by running the following command in your terminal:

```shell
pip install -r requirements.txt
```

2. Run the tests using the following command:

```shell
python -m unittest test_lord_of_the_rings_sdk.py
```

The test suite will execute and display the results in the terminal.

Feel free to modify and extend the SDK according to your specific use cases and requirements.

If you encounter any issues or have questions, please contact the SDK maintainers.
