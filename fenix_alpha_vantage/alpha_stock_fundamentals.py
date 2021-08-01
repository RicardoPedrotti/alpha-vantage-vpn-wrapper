import logging
import pandas as pd
from fenix_alpha_vantage.alpha_data import AlphaData


class AlphaStockFundamentals(AlphaData):
    logger = logging.getLogger()
    logger.setLevel("INFO")

    def __init__(self, config_file_path="fenix_alpha_vantage/config.yml", log_level='INFO'):
        super().__init__(config_file_path=config_file_path)
        self.api_mock_call = (
            self.alpha_api_url + "function={endpoint}&symbol={ticker}&apikey={api_key}"
        )
        self.class_logger = logging.getLogger(self.__class__.__name__)
        self.class_logger.setLevel(level=log_level)

    def annual_quarterly_fundamentals_response_json_to_pandas_handling(self, api_response, suffix):
        if api_response.status_code == 200:
            pandas_df = pd.DataFrame.from_dict(api_response.json(), orient="index")
            annual_reports_df = (
                pd.DataFrame.from_dict(
                    pandas_df.loc[f"annual{suffix}"][0][0], orient="index"
                )
            ).transpose()
            quarterly_reports_df = (
                pd.DataFrame.from_dict(
                    pandas_df.loc[f"quarterly{suffix}"][0][0], orient="index"
                )
            ).transpose()
            aggregated_df = pd.concat([annual_reports_df, quarterly_reports_df])
            return aggregated_df
        else:
            self.class_logger.error(api_response.text)
            raise ValueError

    def fundamentals_response_json_to_pandas_handling(self, api_response):
        if api_response.status_code == 200:
            pandas_df = pd.DataFrame.from_dict(api_response.json(), orient="index")
            return pandas_df
        else:
            self.class_logger.error(api_response.text)
            raise ValueError

    def fundamentals_api_call_general_flow(
        self, endpoint: str, ticker: str, use_vpn: bool, parse_annual_quarterly: bool, suffix='Reports'
    ) -> pd.DataFrame:
        self.logging_info_start(endpoint=endpoint, use_vpn=use_vpn)
        call = self.api_mock_call.format(
            endpoint=endpoint, ticker=ticker, api_key=self.get_random_api_key()
        )
        if parse_annual_quarterly:
            response_dataframe = self.annual_quarterly_fundamentals_response_json_to_pandas_handling(
                self.get_call_api(call, use_vpn=use_vpn), suffix=suffix
            )
        else:
            response_dataframe = self.fundamentals_response_json_to_pandas_handling(
                self.get_call_api(call, use_vpn=use_vpn)
            )
        return response_dataframe

    def df_overview(self, ticker: str, use_vpn: bool = False) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="OVERVIEW", ticker=ticker, use_vpn=use_vpn, parse_annual_quarterly=False
        ).transpose()

    def df_earnings(self, ticker: str, use_vpn: bool = False) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="EARNINGS", ticker=ticker, use_vpn=use_vpn, parse_annual_quarterly=True, suffix="Earnings"
        )

    def df_income_statement(self, ticker: str, use_vpn: bool = False) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="INCOME_STATEMENT", ticker=ticker, use_vpn=use_vpn, parse_annual_quarterly=True
        )

    def df_balance_sheet(self, ticker: str, use_vpn: bool = False) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="BALANCE_SHEET", ticker=ticker, use_vpn=use_vpn, parse_annual_quarterly=True
        )

    def df_cash_flow(self, ticker: str, use_vpn: bool = False) -> pd.DataFrame:
        return self.fundamentals_api_call_general_flow(
            endpoint="CASH_FLOW", ticker=ticker, use_vpn=use_vpn, parse_annual_quarterly=True
        )
