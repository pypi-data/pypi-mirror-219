from typing import List
from .request import sec_request

# a file maintained by the sec that holds all ticker symbols and their corresponding cik
SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"


def ticker_to_cik(ticker_symbol: str) -> str:
    """
    takes a ticker symbol as input and returns the corresponding cik.

    :param ticker_symbol: the ticker symbol of the company
    :return: the cik of the company
    :raises ValueError: if the ticker symbol is not found
    """
    ticker = ticker_symbol.upper()
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data.values():
        if entry['ticker'] == ticker:
            return str(entry['cik_str'])
    raise ValueError(f'ticker symbol {ticker} not found')


def is_registered(ticker_symbol: str) -> bool:
    """
    takes a ticker symbol as input and returns True if the ticker symbol is registered at the sec.
    Otherwise, it returns False.

    :param ticker_symbol: the ticker symbol of the company
    :return: True if the ticker symbol is registered at the sec, otherwise False
    :raises ValueError: if the ticker symbol is not found
    """
    ticker = ticker_symbol.upper()
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data.values():
        if entry['ticker'] == ticker:
            return True
    else:
        return False


def filter_tickers_registered(tickers: List[str]) -> List[str]:
    """
    takes a list of tickers as input and returns a filtered list
    that only contains tickers that are found to be registered at the sec.
    """
    tickers = [ticker.upper() for ticker in tickers]
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    tickers_registered = [entry["ticker"] for entry in data.values()]

    return [ticker for ticker in tickers if ticker in tickers_registered]


def get_registered_tickers() -> List[str]:
    """
    Returns a list of all the tickers of all issuers that are registered at the sec.
    """
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    return [entry["ticker"] for entry in data.values()]


def get_registered_ciks() -> List[str]:
    """
    Returns a list of all the ciks of all issuers that are registered at the sec.
    """
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    return [str(entry["cik_str"]) for entry in data.values()]