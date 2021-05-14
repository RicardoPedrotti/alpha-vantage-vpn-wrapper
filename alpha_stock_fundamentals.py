import logging
import pandas as pd
from alpha_data import AlphaData


class AlphaStockFundamentals(AlphaData):
    logger = logging.getLogger()
    logger.setLevel("INFO")

    def __init__(self):
        super().__init__()
        self.api_mock_call = (
            self.alpha_api_url + "function={endpoint}&symbol={ticker}&apikey={api_key}"
        )

    @staticmethod
    def fundamentals_response_json_to_pandas_handling(api_response):
        if api_response.status_code == 200:
            pandas_df = pd.DataFrame.from_dict(api_response.json(), orient="index")
            return pandas_df
        else:
            logging.error(api_response.text)
            raise ValueError

    def fundamentals_api_call_general_flow(
        self, endpoint: str, ticker: str, use_vpn: bool, print_return: bool
    ) -> pd.DataFrame:
        self.logging_info_start(endpoint=endpoint)
        call = self.api_mock_call.format(
            endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
        )
        response_dataframe = self.fundamentals_response_json_to_pandas_handling(
            self.get_call_api(call, use_vpn=use_vpn)
        )
        if print_return is True:
            print(response_dataframe)
        return response_dataframe

    def df_overview(
        self, ticker: str, use_vpn: bool = False, print_return: bool = False
    ) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="OVERVIEW",
            ticker=ticker,
            use_vpn=use_vpn,
            print_return=print_return,
        )

    def df_earnings(
        self, ticker: str, use_vpn: bool = False, print_return: bool = False
    ) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="EARNINGS",
            ticker=ticker,
            use_vpn=use_vpn,
            print_return=print_return,
        )

    def df_income_statement(
        self, ticker: str, use_vpn: bool = False, print_return: bool = False
    ) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="INCOME_STATEMENT",
            ticker=ticker,
            use_vpn=use_vpn,
            print_return=print_return,
        )

    def df_balance_sheet(
        self, ticker: str, use_vpn: bool = False, print_return: bool = False
    ) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="BALANCE_SHEET",
            ticker=ticker,
            use_vpn=use_vpn,
            print_return=print_return,
        )

    def df_cash_flow(
        self, ticker: str, use_vpn: bool = False, print_return: bool = False
    ) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="CASH_FLOW",
            ticker=ticker,
            use_vpn=use_vpn,
            print_return=print_return,
        )
