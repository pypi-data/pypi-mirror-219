# secapi
This module provides a set of functions that can be used to query 
company submissions from the sec. 
As well as some utility functions that can be used to get sec related 
information about companies.

## Technical information
The module was developed with python 2.7.18 and only uses build-in python packages as well
as the packages typing, requests, ratelimiter and [OpenDateRange](https://github.com/tlie03/OpenDateRange).

## Installation
``$ pip install secapi-tl``

## core functions

### sec_request
The sec_request method is used to make requests to the sec.
It has a rate limit mechanism implemented that ensures that the amount of 
requests stays in the boundaries set by the sec. 
All methods from this module
use this method internally for their requests. Thereby your own requests to
the sec will be compatible if you use this method. Furthermore, the sec_request method will automatically
create a header with a valid User-Agent. You can also pass your own header to the method.
If this header does not contain a User-Agent, the method will add a valid User-Agent to the header.


```python
from secapi_tl import sec_request

raw_data = sec_request(url="https://www.sec.gov/Archives/edgar/data/320193/000032019323000070/xslF345X04/wf-form4_168444912415136.xml")
```

### get_submissions
The get_submissions function queries company submissions via the 
data.sec.gov/submissions/ endpoint as recommended [here](https://www.sec.gov/edgar/sec-api-documentation).
The method takes parameters that can be used to filter the queried submissions.
A query accepts the following parameters:
- ticker_symbol_or_cik: The ticker symbol or cik of the company you want to query submissions for.
Takes lowercase and uppercase letters for ticker symbols. 
Ciks must be passed as strings but leading zeros are not required.
- start_date: Only submissions that have been published at or after this date will be queried.
The date must be passed as a string of format YYYY-MM-DD.
- end_date: Only submissions that have been published at or before this date will be queried.
The date must be passed as a string of format YYYY-MM-DD.
- form_type: Only submissions that have one of the specified form types will be queried.
You can pass a form type as a string or a list of form types as a list of strings.

The method returns a list of Submission objects. Each submission object holds
the data for one submission. The data can be accessed via properties of the object.


```python
from secapi_tl import get_submissions

# query form 4 submissions for apple in january 2021
submissions = get_submissions(
    ticker_symbol_or_cik="AAPL",
    start_date="2021-01-01",
    end_date="2021-01-31",
    form_type="4"
)
```

!!! WARNING !!! Since the data.sec.gov/submissions/ endpoint is constantly under a
high load, it can happen that a TooManyRequestsError is raised. Since the method
does use the sec_request method there is no violation of the rate limit. Requests
to other endpoints will therefore still work. The occurrence of this error is
highly dependent on the usage of this method. So you might need to implement
a mechanism that handles this error depending on your use case. The TooManyRequests
error is part of this module and can be imported from the module.
```python
from secapi_tl import TooManyRequestsError
```

## utility functions
Most of the utility functions are based on the [company tickers file](https://www.sec.gov/files/company_tickers.json).
They use this file for transitions between cik and ticker symbol or to
proof if a ticker symbol is registered at the sec or not.

### is_registered
This method takes a ticker symbol and returns True if the ticker symbol is registered
at the sec and False if it is not registered. If the method returns True the ticker symbol
can be used with all other methods of this module. The ticker symbol can be uppercase and
lowercase. The method will automatically convert the ticker symbol to uppercase letters.
```python
from secapi_tl import is_registered

is_registered("AAPL") # True
is_registered("aapl") # True
is_registered("AAP") # False
```

### ticker_to_cik
This method takes a ticker symbol and returns the cik of the company to which the ticker symbol belongs.
If the ticker symbol is not found a ValueError is raised.
The ticker symbol can be uppercase and lowercase. The method will automatically convert the ticker symbol to uppercase letters.
```python   
from secapi_tl import ticker_to_cik

ticker_to_cik("AAPL") # "320193"
```

### filter_tickers_registered
Takes a list of ticker symbols and returns a list of those ticker symbols that
are found to be registered at the sec. The ticker symbols can be uppercase and lowercase.
The returned ticker symbols are uppercase.
```python
from secapi_tl import filter_tickers_registered

filter_tickers_registered(["AAPL", "TSLA", "AAP"]) # ["AAPL", "TSLA"]
```
This method is useful if you want to query submissions for a list of companies
and you dont know if all of the companies are registered at the sec.
All the returned ticker symbols will work with the get_submissions method.

### get_registered_tickers
Returns a list of all ticker symbols that are found in the [company tickers file](https://www.sec.gov/files/company_tickers.json).

### get_registered_ciks
Returns a list of all ciks that are found in the [company tickers file](https://www.sec.gov/files/company_tickers.json).
