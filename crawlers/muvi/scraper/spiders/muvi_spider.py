import json
import logging
import scrapy
import datetime
from inline_requests import inline_requests
from scrapy.http import FormRequest

from crawlers.muvi.scraper.configs import MuviConfigs


class MuviSpider(MuviConfigs, scrapy.Spider):
    start_urls = ['http://httpbin.org/ip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = ''
        self.movie_id = ''
        self.movie_name = ''
        self.params = ''
        logging.getLogger("scrapy").setLevel(logging.WARNING)

    def parse(self, response):
        yield FormRequest(
            url='https://apiprod.muvicinemas.com/user/v1/token',
            callback=self.fetch_movies,
            meta={'handle_httpstatus_all': True},
            method='POST',
            body=json.dumps({
                "accessTokenExpiry": "3000",
                "dataversion": "en-US",
                "getUserInfo": 'false',
                "keepMeSignedIn": 'true'
            }),
            headers={
                'authorization': 'Basic bXV2aS5pb3NAaW5qaW4uY29tOmRLOHdqX1ludU4kRSFLNEs='},
            dont_filter=True,
        )

    def fetch_movies(self, response):
        try:
            self.token = json.loads(response.body).get('accessToken')
            if self.token:
                yield FormRequest(
                    url='https://apiprod.muvicinemas.com/cms/v1/films',
                    meta={'handle_httpstatus_all': True},
                    method='GET',
                    callback=self.fetch_id,
                    headers={'appversion': '3.1.6',
                             'dataversion': 'en-US',
                             'content-type': 'application/json',
                             'appplatform': 'ANDROID',
                             'authorization': 'Bearer ' + self.token},
                    dont_filter=True,
                )

        except Exception as error:
            message = f"an error occurred while fetching the access token\n" \
                      f"{response}" \
                      f"\nError: {error}"
            logging.error(message)

    @inline_requests
    def fetch_id(self, response):
        data = json.loads(response.body).get('data', [])
        current_index = 0
        available_movies = []
        try:
            for movie in data:
                self.movie_id = movie.get('id')
                self.movie_name = movie.get('title')
                logging.info(
                    f'\nCrawling the movie:'
                    f'\nMovie id: {self.movie_id}\n'
                    f'Movie name: {self.movie_name}\n'
                    f'index : {current_index}\n')
                response = yield FormRequest(
                    url=f'https://apiprod.muvicinemas.com/cms/v1/films/{self.movie_id}/sessionsbyexperience?showdate={datetime.date.today().strftime("%m-%d-%Y")}',
                    meta={'handle_httpstatus_all': True},
                    method='GET',
                    headers={'appversion': '3.1.6',
                             'dataversion': 'en-US',
                             'content-type': 'application/json',
                             'appplatform': 'ANDROID',
                             'authorization': 'Bearer ' + self.token},
                    dont_filter=True,
                )

                movie_details = json.loads(response.body).get('data', [])
                if movie_details:
                    available_movies.append({f'{self.movie_name}': movie_details})
                current_index += 1
            available_index = 0
            logging.info(f'Total valid movies: {len(available_movies)}')
            for movie in available_movies:
                available_index += 1
                location_index = 0
                locations = movie[list(movie.keys())[0]]
                for location in locations:
                    if location_index == len(locations) - 1 and available_index == len(available_movies):
                        location['last_movie'] = True
                    location_index += 1
                    location['movie_name'] = list(movie.keys())[0]
                    location['movie_id'] = self.movie_id
                    yield location

        except Exception as error:
            message = f"an error occurred while fetching movie details for:" \
                      f"\nMovie id: {self.movie_id}" \
                      f"\nMovie name: {self.movie_name}" \
                      f"\nError: {error}"
            logging.error(message)
