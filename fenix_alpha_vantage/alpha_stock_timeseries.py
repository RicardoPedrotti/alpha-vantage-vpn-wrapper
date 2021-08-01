import concurrent
import logging
from typing import Callable, List
import pandas as pd
from fenix_alpha_vantage.alpha_data import AlphaData


class AlphaStockTimeSeries(AlphaData):
    def __init__(self, config_file_path="fenix_alpha_vantage/config.yml", log_level='INFO'):
        super().__init__(config_file_path=config_file_path, log_level=log_level)
        self.api_mock_call = (
            self.alpha_api_url + "function={endpoint}&symbol={ticker}&apikey={api_key}"
        )
        self.class_logger = logging.getLogger(self.__class__.__name__)
        self.class_logger.setLevel(level=log_level)

    def df_time_series_intraday(
        self,
        ticker: str,
        interval: str = "60min",
        adjusted: str = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        # Endpoint Configs
        endpoint = "TIME_SERIES_INTRADAY"
        possible_intervals = ["1min", "5min", "15min", "30min", "60min"]
        converters = {
            "timestamp": pd.to_datetime,
            "open": pd.to_numeric,
            "high": pd.to_numeric,
            "low": pd.to_numeric,
            "close": pd.to_numeric,
        }
        column_renaming_map = {'timestamp': 'date'}
        # Endpoint Configs #
        self.logging_info_start(
            endpoint=endpoint, intervals=possible_intervals, use_vpn=use_vpn
        )
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&interval={interval}&adjusted={str(adjusted).lower()}&outputsize=full&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            response=self.get_call_api(call, use_vpn=use_vpn), converters=converters, column_renaming_map=column_renaming_map
        )

    def df_time_series_intraday_extended(
        self,
        ticker: str,
        interval: str = "60min",
        adjusted: bool = True,
        year_range: int = 2,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        # Endpoint Configs
        endpoint = "TIME_SERIES_INTRADAY_EXTENDED"
        possible_intervals = ["1min", "5min", "15min", "30min", "60min"]
        converters = {
            "time": pd.to_datetime,
            "open": pd.to_numeric,
            "high": pd.to_numeric,
            "low": pd.to_numeric,
            "close": pd.to_numeric,
        }
        column_renaming_map = {'time': 'date'}
        # Endpoint Configs #
        if year_range > 2:
            self.class_logger.error(
                'By limitations of the API, the maximum value for the param "year_range" is 2'
            )
            raise ValueError
        else:
            self.logging_info_start(
                endpoint=endpoint, intervals=possible_intervals, use_vpn=use_vpn
            )
            api_calls = [
                self.api_mock_call.format(
                    endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
                )
                + f"&interval={interval}"
                f"&adjusted={str(adjusted).lower()}"
                f"&outputsize=full"
                f'&slice={f"year{year + 1}month{month + 1}"}'
                for month in range(12)
                for year in range(year_range)
            ]
            api_responses = list(self.futures_api_calls(request_list=api_calls, use_vpn=use_vpn))
            aggregated_df = pd.concat(
                [
                    self.response_csv_to_pandas_handling(response=response, converters=converters, column_renaming_map=column_renaming_map)
                    for response in api_responses
                ]
            )
            return aggregated_df

    def df_time_series_daily(
        self,
        ticker: str,
        adjusted: bool = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        if adjusted is True:
            endpoint = "TIME_SERIES_DAILY_ADJUSTED"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric,
                "adjusted_close": pd.to_numeric,
                "dividend_amount": pd.to_numeric,
                "split_coefficient": pd.to_numeric
            }
        else:
            endpoint = "TIME_SERIES_DAILY"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric
            }
        column_renaming_map = {'timestamp': 'date'}
        self.logging_info_start(endpoint=endpoint, use_vpn=use_vpn)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&outputsize=full&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn), converters=converters,column_renaming_map=column_renaming_map
        )

    def df_time_series_weekly(
        self,
        ticker: str,
        adjusted: bool = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        if adjusted is True:
            endpoint = "TIME_SERIES_WEEKLY_ADJUSTED"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric,
                "adjusted close": pd.to_numeric,
                "dividend amount": pd.to_numeric
            }
        else:
            endpoint = "TIME_SERIES_WEEKLY"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric,
            }
        column_renaming_map = {'timestamp': 'date', 'adjusted close': 'adjusted_close', 'dividend amount': 'dividend_amount'}

        self.logging_info_start(endpoint=endpoint, use_vpn=use_vpn)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn), converters=converters, column_renaming_map=column_renaming_map
        )

    def df_time_series_monthly(
        self,
        ticker: str,
        adjusted: bool = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        if adjusted is True:
            endpoint = "TIME_SERIES_MONTHLY_ADJUSTED"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric,
                "adjusted close": pd.to_numeric,
                "dividend amount": pd.to_numeric
            }
        else:
            endpoint = "TIME_SERIES_MONTHLY"
            converters = {
                "timestamp": pd.to_datetime,
                "open": pd.to_numeric,
                "high": pd.to_numeric,
                "low": pd.to_numeric,
                "close": pd.to_numeric
            }
        column_renaming_map = {'timestamp': 'date', 'adjusted close': 'adjusted_close',
                               'dividend amount': 'dividend_amount'}


        self.logging_info_start(endpoint=endpoint, use_vpn=use_vpn)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn), converters=converters, column_renaming_map=column_renaming_map
        )

    def df_quote_endpoint(
        self,
        ticker: str,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        endpoint = "GLOBAL_QUOTE"

        self.logging_info_start(endpoint=endpoint, use_vpn=use_vpn)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn), converters=None
        )

    # def process_multiple_tickers(self, endpoint_method: Callable, tickers_list: list, *args):
    #     def futures_api_calls(self, request_list: List[str], use_vpn: bool):
    #         with concurrent.futures.ProcessPoolExecutor() as executor:
    #             responses = executor.map(endpoint_method, tickers_list,     repeat(use_vpn))
    #         return responses