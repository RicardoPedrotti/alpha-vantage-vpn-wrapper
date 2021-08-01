import json
import logging
import concurrent.futures
from io import StringIO
from itertools import repeat
from typing import List
from time import sleep

import yaml
import requests
import pandas as pd
import random


class AlphaData:
    def __init__(
        self, config_file_path="fenix_alpha_vantage/config.yml", log_level="INFO"
    ):
        self.alpha_api_url = "https://www.alphavantage.co/query?"
        try:
            self.configs = config = yaml.safe_load(open(config_file_path))
        except FileNotFoundError:
            self.configs = config = yaml.safe_load(open(f"../{config_file_path}"))
        self.api_keys = config.get("alpha_vantage_api_key_list")
        self.proxies = config.get("vpn_proxies")
        self.class_logger = logging.getLogger(self.__class__.__name__)
        self.class_logger.setLevel(level=log_level)

    def get_random_api_key(self):
        api_key = self.api_keys[random.randrange(len(self.api_keys))]
        self.class_logger.debug(f"Using API Key {api_key}")
        return api_key

    def get_call_api(
        self, url, use_vpn=False, tries=10, delay=3, max_delay=20, backoff=2
    ):
        """
        Calls a simple get api using proxies when applied with some retries
        """
        current_try = 0
        while current_try < tries:
            self.class_logger.info(f'Try number {str(current_try+1)} on call {url}')
            if use_vpn is True:
                response = requests.request("GET", url, proxies=self.proxies)
            else:
                response = requests.request("GET", url)
            if response.status_code == 200 and "Invalid API call." not in response.text:
                return response
            else:
                self.class_logger.error(
                    f"ERROR! Status code for the error: {str(response.status_code)}"
                    f"\nMessage from Alpha Vantage: {str(response.text)}"
                )
                current_retry_delay = (
                    max_delay
                    if delay + (backoff * current_try) > max_delay
                    else delay + (backoff * current_try)
                )
                self.class_logger.info(f'Waiting {str(current_retry_delay)} seconds to make a new request.')
                sleep(current_retry_delay)
                current_try += 1

    def futures_api_calls(self, request_list: List[str], use_vpn: bool):
        """
        Receives a list of API calls to request simultaneously using the number of cores in the computer minus one
        and returns the api's responses
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            responses = executor.map(self.get_call_api, request_list, repeat(use_vpn))
        return responses

    def response_csv_to_pandas_handling(self, response, converters, column_renaming_map=None):
        if response.status_code == 200:
            pandas_df = pd.read_csv(
                filepath_or_buffer=StringIO(response.text), converters=converters
            )
            if pandas_df.size > 3:
                if column_renaming_map:
                    pandas_df = pandas_df.rename(
                        mapper=column_renaming_map, axis="columns"
                    )
                return pandas_df
            else:
                self.class_logger.error(
                    f"Well, apparently the call {response.url} returned an empty Dataframe"
                )
                self.class_logger.error(
                    f"Could be a bug, but first please check your arguments and try again. "
                    f"If exceeded the number of API calls, try using VPN."
                    f" Below is the returned information from Alpha vantage: "
                )
                self.class_logger.error(response.text)

    def logging_info_start(
        self,
        endpoint: str,
        use_vpn: bool = False,
        intervals: List = None,
        additional_logging_on_start: str = "",
    ):
        self.class_logger.debug(f"Starting API Interface with Endpoint: {endpoint}")
        if use_vpn is True:
            self.class_logger.debug(
                "Using VPN to call Alpha Vantage! Be aware that this is a 3rd party service which"
                " can malfunction sometimes due to connection timeout. If it does, try your command again."
            )
        else:
            self.class_logger.debug(
                "Beware! Not using VPN to call Alpha Vantage! This way, even when using different API keys"
                " they know who is sending the request! ;D"
            )
        if intervals is not None:
            self.class_logger.debug(
                f"Optional intervals between the Data Points for this API are: {str(intervals)}."
                f" If not set, uses standard value."
            )
        if additional_logging_on_start != "":
            self.class_logger.debug(additional_logging_on_start)

    def search_endpoint(
        self, what_to_search: str, use_vpn: bool = False
    ) -> pd.DataFrame:
        endpoint = "SYMBOL_SEARCH"
        self.logging_info_start(endpoint=endpoint)
        call = (
            f"{self.alpha_api_url}"
            f"function={endpoint}"
            f"&keywords={what_to_search.lower()}"
            f"&datatype=csv&apikey={self.get_random_api_key()}"
        )
        search_return_df = self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn), converters=None
        )
        print(f"{search_return_df.shape[0]} Results returned.")
        return search_return_df

    # @staticmethod
    # def decimal_from_value(value):
    #     # https://beepscore.com/website/2018/10/12/using-pandas-with-python-decimal.html
    #     return Decimal(value)
