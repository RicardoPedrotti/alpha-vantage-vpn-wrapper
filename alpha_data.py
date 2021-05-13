import logging
import concurrent.futures
from io import StringIO
from itertools import repeat
from typing import List

import yaml
import requests
import pandas as pd
import random


class AlphaData:
    def __init__(self, config_file_path="config.yml"):
        self.configs = config = yaml.safe_load(open(config_file_path))
        self.api_keys = config.get("alpha_vantage_api_key_list")
        self.proxies = config.get("vpn_proxies")

    def get_random_api_key(self):
        api_key = self.api_keys[random.randrange(len(self.api_keys))]
        logging.info(f'Using API Key {api_key}')
        return api_key

    def get_call_api(self, url, use_vpn=False):
        """
        Calls a simple get api using proxies when applied
        :param url: api url to call
        :param use_vpn: Define whether the call should use the VPN or not
        :return: api response
        """
        if use_vpn is True:
            response = requests.request("GET", url, proxies=self.proxies)
        else:
            response = requests.request("GET", url)

        if response.status_code == 200:
            return response
        else:
            logging.error(
                f"ERROR! Status code for the error: {str(response.status_code)}"
                f"/n Message from Alpha Vantage: /n{str(response.text)}"
            )

    def futures_api_calls(self, request_list: List, use_vpn: bool):
        """
        Receives a list of API calls to request simultaneously using the number of cores in the computer minus one
        and returns the api's responses
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            responses = executor.map(self.get_call_api, request_list, repeat(use_vpn))
        return responses

    @staticmethod
    def response_csv_to_pandas_handling(response):
        if response.status_code == 200:
            pandas_df = pd.read_csv(StringIO(response.text))
            if pandas_df.size > 3:
                return pandas_df
            else:
                logging.error(
                    f"Well, apparently the call {response.url} returned an empty Dataframe"
                )
                logging.error(
                    f"Could be a bug, but first please check your arguments and try again. If exceeded the number of API calls, try using VPN."
                    f" Below is the returned information from Alpha vantage: "
                )
                logging.error(response.text)
                raise ValueError
