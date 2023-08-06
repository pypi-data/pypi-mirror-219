from typing import List, Union
from openDateRange import DateRange
import re

from .request import sec_request
from .utility_functions import ticker_to_cik
from .submission import Submission


# list of existing metadata points for a submission
FILING_INFORMATION_KEYS = ['accessionNumber',
                           'filingDate',
                           'reportDate',
                           'acceptanceDateTime',
                           'act',
                           'form',
                           'fileNumber',
                           'filmNumber',
                           'items',
                           'size',
                           'isXBRL',
                           'isInlineXBRL',
                           'primaryDocument',
                           'primaryDocDescription']

DATE_FORMAT = '%Y-%m-%d'
JSON_FILE = ".json"
BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10
CIK_REGEX = re.compile('\d{0,10}')


def get_submissions(ticker_symbol_or_cik: str,
                    date_from: str = None,
                    date_to: str = None,
                    form_types: Union[List[str], str] = None) -> List[Submission]:
    """
    Returns a list of submissions that match the given parameters.
    The parameters are used to create a query to the sec server and filter the data afterward.
    The function accesses the https://data.sec.gov/submissions/ endpoint as it recommended by the sec.

    !!!
    It can happen that a TooManyRequestsError is raised. This happens when the https://data.sec.gov/submissions/
    endpoint is overloaded. The SEC returns a 429 status code in this case. Requests to other endpoints are not blocked
    since the method uses the sec_request function and thus the allowed request limit is not exceeded. You may need to
    implement your own strategy to handle this error since this error depends strongly on the usage of this function.
    !!!

    :param ticker_symbol_or_cik: ticker symbol or cik of the company cik should be a string
    :param date_from: the date from which the submissions should be returned "YYYY-MM-DD"
    :param date_to: the date to which the submissions should be returned "YYYY-MM-DD"
    :param form_types: submission form types that should be returned. Valid form types are all form types that
                     are used by the sec for submissions.
    :return: the list of Submission instances each instance contains the data for one submission
    """

    format_before = DateRange.DATE_FORMAT
    DateRange.DATE_FORMAT = DATE_FORMAT
    search_daterange = DateRange(date_from=date_from, date_to=date_to)
    DateRange.DATE_FORMAT = format_before

    if isinstance(form_types, str):
        form_types = [form_types]
    checker = create_filing_checker(search_daterange, form_types)

    # get the main submissions file
    # the ticker symbol can also be a cik
    if CIK_REGEX.fullmatch(ticker_symbol_or_cik):
        cik = ticker_symbol_or_cik
    else:
        cik = ticker_to_cik(ticker_symbol_or_cik)
    length_diff = REQUIRED_CIK_LENGTH - len(cik)
    cik_formatted = ('0' * length_diff) + cik
    submissions_url = BASE_URL_SUBMISSIONS + CIK_STRING + cik_formatted + JSON_FILE

    response = sec_request(url=submissions_url)
    submissions_dict = response.json()

    filings = []
    # parse recent
    data = submissions_dict['filings']['recent']
    if search_daterange.intersects(date_from=data['filingDate'][-1], date_to=data['filingDate'][0]):
        filings += filter_filings(data, checker, cik, ticker_symbol_or_cik)

    # parse files
    files = submissions_dict['filings']['files']
    for file in files:
        if search_daterange.intersects(date_from=file['filingFrom'], date_to=file['filingTo']):
            url = BASE_URL_SUBMISSIONS + file['name']
            response = sec_request(url=url)
            data = response.json()
            filings += filter_filings(data, checker, cik, ticker_symbol_or_cik)

    return [Submission._from_dict(filing_dict=filing) for filing in filings]


def filter_filings(raw_filings, checker, cik, ticker_symbol):
    filings = []

    dates = raw_filings['filingDate']
    forms = raw_filings['form']
    for i, (date, form) in enumerate(zip(dates, forms)):
        if checker(date, form):
            filing = {'tickerSymbol': ticker_symbol.upper(), 'cik': cik}
            for key in FILING_INFORMATION_KEYS:
                filing[key] = raw_filings[key][i]
            filings.append(filing)
    return filings


def create_filing_checker(date_range, form_types):
    def filing_checker(filing_date, form):
        return filing_date in date_range and (form_types is None or form in form_types)

    return filing_checker
