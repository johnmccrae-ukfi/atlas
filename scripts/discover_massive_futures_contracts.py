from __future__ import annotations

import os
import sys

import requests
from dotenv import load_dotenv
from datetime import date


API_URL = "https://api.massive.com/futures/v1/contracts"


def main() -> int:
    load_dotenv()

    api_key = os.getenv("MASSIVE_API_KEY")

    if not api_key or api_key == "your_massive_api_key_here":
        print("Error: MASSIVE_API_KEY is missing or still contains the placeholder value.")
        return 1

    params = {
        "product_code": "MES",
        "date": date.today().isoformat(),
        "active": "true",
        "type": "single",
        "limit": 100,
        "sort": "ticker.asc",
        "apiKey": api_key,
    }

    print("Requesting active MES futures contracts from Massive...")

    try:
        response = requests.get(API_URL, params=params, timeout=30)

        if not response.ok:
            print(f"Massive API request failed with status {response.status_code}.")
            print(f"Response body: {response.text}")
            return 1

    except requests.RequestException as exc:
        print(f"Massive API request failed: {exc}")
        return 1

    payload = response.json()
    raw_results = payload.get("results", [])

    today = date.today().isoformat()

    filtered_results = [
        contract
        for contract in raw_results
        if contract.get("ticker")
        and contract.get("last_trade_date")
        and contract["last_trade_date"] >= today
    ]

    contracts_by_ticker = {
        contract["ticker"]: contract
        for contract in filtered_results
    }

    results = sorted(
        contracts_by_ticker.values(),
        key=lambda contract: contract["last_trade_date"],
    )

    print(f"Raw records returned: {len(raw_results)}")
    print(f"Unique contracts returned: {len(results)}")

    # print(f"Contracts returned: {len(results)}")

    if not results:
        print("No active MES contracts were returned.")
        print(payload)
        return 1

    for contract in results:
        print("-" * 70)
        print(f"Ticker:           {contract.get('ticker')}")
        print(f"Name:             {contract.get('name')}")
        print(f"Product code:     {contract.get('product_code')}")
        print(f"Trading venue:    {contract.get('trading_venue')}")
        print(f"First trade date: {contract.get('first_trade_date')}")
        print(f"Last trade date:  {contract.get('last_trade_date')}")
        print(f"Days to maturity: {contract.get('days_to_maturity')}")
        print(f"Active:           {contract.get('active')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())