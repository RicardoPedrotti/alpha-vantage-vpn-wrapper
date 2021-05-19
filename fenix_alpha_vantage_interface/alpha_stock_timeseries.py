import logging
from typing import List
import pandas as pd
from fenix_alpha_vantage_interface.alpha_data import AlphaData


class AlphaStockTimeSeries(AlphaData):
    logger = logging.getLogger()
    logger.setLevel("INFO")

    def __init__(self):
        super().__init__()
        self.api_mock_call = (
            self.alpha_api_url + "function={endpoint}&symbol={ticker}&apikey={api_key}"
        )

    def df_time_series_intraday(
        self,
        ticker: str,
        interval: str = "60min",
        adjusted: str = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        endpoint = "TIME_SERIES_INTRADAY"
        possible_intervals = ["1min", "5min", "15min", "30min", "60min"]
        self.logging_info_start(endpoint=endpoint, intervals=possible_intervals)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&interval={interval}&adjusted={str(adjusted).lower()}&outputsize=full&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )

    def df_time_series_intraday_extended(
        self,
        ticker: str,
        interval: str,
        adjusted: bool = True,
        year_range: int = 2,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        endpoint = "TIME_SERIES_INTRADAY_EXTENDED"
        possible_intervals = ["1min", "5min", "15min", "30min", "60min"]
        if year_range > 2:
            logging.error(
                'By limitations of the API, the maximum value for the param "year_range" is 2'
            )
            raise ValueError
        else:
            self.logging_info_start(endpoint=endpoint, intervals=possible_intervals)
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
            api_responses = list(self.futures_api_calls(api_calls, use_vpn))
            aggregated_df = pd.concat(
                [
                    self.response_csv_to_pandas_handling(response)
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
        else:
            endpoint = "TIME_SERIES_DAILY"

        self.logging_info_start(endpoint=endpoint)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&outputsize=full&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )

    def df_time_series_weekly(
        self,
        ticker: str,
        adjusted: bool = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        if adjusted is True:
            endpoint = "TIME_SERIES_WEEKLY_ADJUSTED"
        else:
            endpoint = "TIME_SERIES_WEEKLY"

        self.logging_info_start(endpoint=endpoint)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )

    def df_time_series_monthly(
        self,
        ticker: str,
        adjusted: bool = True,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        if adjusted is True:
            endpoint = "TIME_SERIES_MONTHLY_ADJUSTED"
        else:
            endpoint = "TIME_SERIES_MONTHLY"

        self.logging_info_start(endpoint=endpoint)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )

    def df_quote_endpoint(
        self,
        ticker: str,
        use_vpn: bool = False,
    ) -> pd.DataFrame:
        endpoint = "GLOBAL_QUOTE"

        self.logging_info_start(endpoint=endpoint)
        call = (
            self.api_mock_call.format(
                endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
            )
            + f"&datatype=csv"
        )
        return self.response_csv_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )
