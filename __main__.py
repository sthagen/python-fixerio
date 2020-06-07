#! /usr/bin/env python
# encoding: utf-8
"""Retrieve latest exchange rates from free fixer.io API endpoint with TOKEN."""

import os
import sys
import requests

TOKEN_NAME = "FIXERIO_TOKEN"
ACCESS_TOKEN = os.getenv(TOKEN_NAME)
if not ACCESS_TOKEN:
    raise ValueError(f"no token value or undefined {TOKEN_NAME}")

PROTOCOL = "http"  # free access only via HTTP
API_ROOT = f"{PROTOCOL}://data.fixer.io/api/"
BASE_CURRENCY = "CHF"  # free access only with base EUR
RATES_IN = ["CHF", "EUR", "USD", "DKK", "BTC", "HUF", "ISK"]
QUERY_OPTIONS = f"access_key={ACCESS_TOKEN}&symbols={','.join(RATES_IN)}"
QUERY_LATEST_ENDPOINT = f"{API_ROOT}latest?{QUERY_OPTIONS}"


def get_exchange_report():
    """Return JSON response or empty dict print JSON response if error."""
    try:
        response = requests.get(QUERY_LATEST_ENDPOINT)
        if response.status_code != 200:
            print("ERROR:", response.json())
        else:
            return response.json()
    except requests.ConnectionError as error:
        print("ERROR:", error)
    return {}


def main():
    """Retrieve latest report and rebase on BASE_CURRENCY."""
    report = get_exchange_report()
    if not report:
        sys.exit(1)
    print("Raw:", report)
    rates = report["rates"]
    rescale = 1.0 / rates[BASE_CURRENCY]
    rates_rescaled = {k: v * rescale for k, v in rates.items()}
    rates_rounded = {
        k: f"{round(v, 6):.6f}" if v > 0.1 else f"{round(v, 9):.9f}"
        for k, v in rates_rescaled.items()
    }
    print("Rescaled:", rates_rounded)


main()
