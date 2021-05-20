import json
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
    def __init__(self, config_file_path="fenix_alpha_vantage_interface/config.yml"):
        self.alpha_api_url = "https://www.alphavantage.co/query?"
        try:
            self.configs = config = yaml.safe_load(open(config_file_path))
        except FileNotFoundError:
            self.configs = config = yaml.safe_load(open(f"../{config_file_path}"))
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

    @staticmethod
    def logging_info_start(
            endpoint: str,
            use_vpn: bool = False,
            intervals: List = None,
            additional_logging_on_start: str = "",
    ):
        logging.info(f"Starting API Interface with Endpoint: {endpoint}")
        if use_vpn is True:
            logging.info(
                "Using VPN to call Alpha Vantage! Be aware that this is a 3rd party service which"
                " can malfunction sometimes due to connection timeout. If it does, try your command again."
            )
        else:
            logging.info(
                "Beware! Not using VPN to call Alpha Vantage! This way, even when using different API keys"
                " they know who is sending the request! ;D"
            )
        if intervals is not None:
            logging.info(
                f"Optional intervals between the Data Points for this API are: {str(intervals)}."
                f" If not set, uses standard value."
            )
        if additional_logging_on_start is not "":
            logging.info(additional_logging_on_start)

    def search_endpoint(self, what_to_search: str, use_vpn: bool = False):
        endpoint = "SYMBOL_SEARCH"
        self.logging_info_start(endpoint=endpoint)
        call = f"{self.alpha_api_url}" \
               f"function={endpoint}" \
               f"&keywords={what_to_search.lower()}" \
               f"&datatype=csv&apikey={self.get_random_api_key()}"
        search_return_df = self.response_csv_to_pandas_handling(self.get_call_api(call, use_vpn=use_vpn))
        print(f"{search_return_df.shape[0]} Results returned. Showing first records.")
        print(search_return_df.head(10))



