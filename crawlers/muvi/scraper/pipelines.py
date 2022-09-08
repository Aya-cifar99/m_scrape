import csv
import datetime
import json
import logging
import os
import sys
from functools import reduce
import boto3


class JsonWriterPipeline:
    s3 = None
    directory_name = None
    result = []
    result_dict = {}
    today = datetime.date.today().strftime("%Y-%m-%d")
    first_item = True
    response_keys_path = [
        "cinemas_locations.0.city",
        "cinemas_attributes.0.name",
    ]


    def open_spider(self, spider):
        logging.error(f"Starting a new scraper at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")


    def close_spider(self, spider):
        logging.error(f"Ending the scraper at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    def process_item(self, movies):
        try:
            self.validate_movies(movies)
        except Exception as err:
            message = f'Error while validating movie: ' \
                      f'\nMovie name: {movies.get("movie_name")}' \
                      f'\nMovie id: {movies.get("movie_id")}' \
                      f'\n ERROR : {err}'
            logging.error(message)
        if movies.get('last_movie'):
            if 'results' in self.result_dict:
                try:
                    sorted_result = sorted(self.result_dict['results'], key=lambda k: k['city'])
                    logging.info(f'Total showtimes: {len(self.result_dict["results"])} showtime')
                    keys = sorted_result[0].keys()
                    with open(os.getcwd() + fr'/muvi_{datetime.date.today().strftime("%Y-%m-%d")}.csv', 'a', newline='') as output_file:
                        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                        dict_writer.writeheader()
                        dict_writer.writerows(sorted_result)
                    logging.info(f'Saving csv file: {os.getcwd()}' +'/muvi_'+ fr"{datetime.date.today().strftime('%Y-%m-%d')}")
                except Exception as err:
                    message = f'Error while saving csv file, \n ERROR : {err}'
                    logging.error(message)
            else:
                message = f'No available movies for today to save, ' \
                          f'Please validate the query parameters again ... '
                logging.error(message)
        return movies

    def save_routes_into_s3(self, movies):
        file_name = f'{self.directory_name}/muvi_{datetime.date.today().strftime("%Y-%m-%d")}.json'
        file_content = bytes(json.dumps(movies, indent=4, ensure_ascii=False).encode("utf8"))
        self.s3.put_object(Body=file_content, Bucket=BUCKET_NAME, Key=file_name)

    def validate_movies(self, results):
        if not results:
            return

        if self.first_item:
            self.validate_response_attribuites(results)
            self.first_item = False

        for exp in results.get('sessionsbyexperience'):
            sessions = exp.get('experiences').get('sessions')
            for item in sessions:
                resource = {
                    'city': results.get('cinemas_locations')[0].get('city'),
                    'movie_name': results.get('movie_name'),
                    'cinema_name': results.get('cinemas_attributes')[0].get('name'),
                    'experience': exp.get('experiences').get('experienceid').get('name'),
                    'show_time': item.get('showtime'),
                }

                if 'results' not in self.result_dict:
                    self.result_dict['results'] = []
                self.result_dict['results'].append(resource)
                self.result.append(resource)

    def remove_duplicates(self, list_of_dicts):
        filtered_set = set()
        new_list_of_dicts = []
        for d in list_of_dicts:
            t = tuple(d.items())
            if t not in filtered_set:
                filtered_set.add(t)
                new_list_of_dicts.append(d)
        return new_list_of_dicts

    def _haskey(self, dict, path):
        """ checks if the specified path exists in a dictionary """
        try:
            reduce(lambda curr_object, key: curr_object[int(key)] if key.isdigit() and isinstance(curr_object, list) else curr_object[key] , path.split("."), dict)
            return True
        except KeyError:
            return False

    def validate_response_attribuites(self, data):
        """validate the keys of passed dict """
        for path in self.response_keys_path:
            if not self._haskey(data, path):
                logging.error(f"unable to find attribute path : {path} in data")
            else:
                logging.debug(f"{path} does exist")
