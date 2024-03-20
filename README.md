# Yelp Scraper Project

This project contains a Scrapy spider for scraping business information from Yelp based on user-specified criteria such as location and category. It's designed to help gather data about businesses for analysis or personal use, adhering to Yelp's API rate limits (500 API calls per day) and terms of use.

## Features

- Scrapes business details from Yelp, including name, rating, and Yelp URL.
- Retrieves the first 5 reviews for each business, including the review text, date, and rating.
- Allows customization of the scraping process through command-line arguments, including location, category name, and maximum number of items to scrape.

**Note:** The spider doesn't extract the business website or reviewer's personal name due to limitations in the Yelp API. Due to the limit of 500 API calls per day, not all results may be available in `results.jsonl`.

## Prerequisites

Before running this spider, you need to have Python 3.6+ and Scrapy installed on your system. Additionally, you'll need a Yelp API key set in your environment variables.

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
4. Create a `.env` file in the root of your project directory (same place as your `scrapy.cfg` file) and add your Yelp API key:

    ```plaintext
    AUTH_KEY=YOUR_API_KEY
    ```

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start scraping Yelp for business information, use the following command:

```bash
scrapy crawl yelp -a location="Your Location" -a category_name="Your Category" -a max_items=Your Max Items
