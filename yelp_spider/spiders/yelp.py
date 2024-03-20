import os
import json
from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from dotenv import load_dotenv

from yelp_spider.items import BusinessItem

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)


class YelpSpider(scrapy.Spider):
    name = 'yelp'
    handle_httpstatus_list = [400, 401, 429]

    def __init__(self, location: str, category_name: str, max_items=1000, **kwargs) -> None:
        super().__init__(**kwargs)

        if not location or not category_name:
            raise ValueError('"location" and "category_name" arguments are required')

        self.location = location
        self.category = category_name
        self.base_url = 'https://api.yelp.com/v3'
        self.limit = 50
        self.offset = 0
        self.headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
        }

        # default value for the official YELP API is 1000 https://docs.developer.yelp.com/docs/fusion-faq
        self.max_items = max_items

    @staticmethod
    def check_status_code(status_code: int):
        if status_code == 401:
            raise CloseSpider('Unauthorized access, check your API key')
        if status_code == 429:
            raise CloseSpider('API rate limit exceeded, retry after 24 hours (500 calls per day)')

    def start_requests(self) -> Iterable[Request]:
        query_str = 'location={self.location}&categories={self.category}&limit={self.limit}&offset={self.offset}'
        url = f'{self.base_url}/businesses/search?{query_str}'
        yield Request(url, headers=self.headers)

    def parse(self, response: Response, **kwargs: Any):
        self.check_status_code(response.status)
        data = json.loads(response.text)
        businesses = data.get('businesses', [])
        total = data.get('total', 0)

        for business in businesses:
            item = BusinessItem()
            item['name'] = business.get('name')
            item['rating'] = business.get('rating')
            item['business_yelp_url'] = business.get('url')
            reviews_url = f'{self.base_url}/businesses/{business.get("id")}/reviews'
            yield Request(reviews_url, callback=self.parse_reviews, headers=self.headers, meta={'item': item})

        self.offset += self.limit
        if self.offset <= total and self.offset <= self.max_items:
            query_str = 'location={self.location}&categories={self.category}&limit={self.limit}&offset={self.offset}'
            next_page = f'{self.base_url}/businesses/search?{query_str}'
            yield response.follow(next_page, callback=self.parse, headers=self.headers)

    def parse_reviews(self, response: Response):
        self.check_status_code(response.status)
        data = json.loads(response.text)
        item = response.meta.get('item')
        reviews = data.get('reviews', [])
        item['reviews'] = [
            {
                'reviewer_name': review.get('user', {}).get('name'),
                'text': review.get('text'),
                'review_date': review.get('time_created'),
                'rating': review.get('rating')
            } for review in reviews[:5]
        ]
        yield item
