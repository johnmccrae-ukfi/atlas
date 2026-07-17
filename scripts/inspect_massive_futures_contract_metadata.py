from __future__ import annotations

import json
import os
import sys
from datetime import date
from typing import Any

import requests
from dotenv import load_dotenv


API_URL = "https://api.massive.com/futures/v1/contracts"

TARGET_CONTRACTS = {
    "MES": "MESU6",
    "MNQ": "MNQU6",
}


def request_product_contracts(
    api_key: str,
    product_code: str,
) -> list[dict[str, Any]]:
    """Retrieve active single-contract metadata for one Futures product."""

    params = {
        "product_code": product_code,
        "date": date.today().isoformat(),
        "active": "true",
        "type": "single",
        "limit": 100,
        "sort": "ticker.asc",
        "apiKey": api_key,
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Massive contract request for {product_code} failed with "
            f"status {response.status_code}: {response.text}"
        )

    try:
        payload = response.json()
    except requests.JSONDecodeError as exc:
        raise RuntimeError(
            f"Massive returned invalid JSON for {product_code}."
        ) from exc

    results = payload.get("results", [])

    if not isinstance(results, list):
        raise RuntimeError(
            f"Massive returned an unexpected results value for "
            f"{product_code}."
        )

    return [
        contract
        for contract in results
        if isinstance(contract, dict)
    ]


def find_contract(
    contracts: list[dict[str, Any]],
    ticker: str,
) -> dict[str, Any] | None:
    """Find one exact provider ticker in a contract response."""

    return next(
        (
            contract
            for contract in contracts
            if contract.get("ticker") == ticker
        ),
        None,
    )


def print_contract(
    product_code: str,
    target_ticker: str,
    contract: dict[str, Any],
) -> None:
    """Print all metadata returned for one selected contract."""

    print()
    print("=" * 88)
    print(f"Product requested: {product_code}")
    print(f"Target ticker:     {target_ticker}")
    print(f"Fields returned:   {len(contract)}")

    for field_name in sorted(contract):
        value = contract.get(field_name)

        if isinstance(value, (dict, list)):
            formatted_value = json.dumps(
                value,
                indent=2,
                sort_keys=True,
            )
        else:
            formatted_value = str(value)

        print(f"{field_name:<28}: {formatted_value}")


def main() -> int:
    """Compare Massive reference metadata for MESU6 and MNQU6."""

    load_dotenv()

    api_key = os.getenv("MASSIVE_API_KEY", "").strip()

    if (
        not api_key
        or api_key == "your_massive_api_key_here"
    ):
        print(
            "Error: MASSIVE_API_KEY is missing or still contains "
            "the placeholder value."
        )
        return 1

    print("Massive Futures contract metadata comparison")
    print("Selected v1.3.0 discovery contracts:")
    print("  Existing contract: MESU6")
    print("  Candidate contract: MNQU6")

    selected_contracts: dict[str, dict[str, Any]] = {}

    try:
        for product_code, target_ticker in TARGET_CONTRACTS.items():
            contracts = request_product_contracts(
                api_key=api_key,
                product_code=product_code,
            )

            contract = find_contract(
                contracts=contracts,
                ticker=target_ticker,
            )

            if contract is None:
                print(
                    f"Error: {target_ticker} was not found in the "
                    f"{product_code} contract response."
                )
                return 1

            selected_contracts[target_ticker] = contract

            print_contract(
                product_code=product_code,
                target_ticker=target_ticker,
                contract=contract,
            )

    except requests.RequestException as exc:
        print(f"Massive API request failed: {exc}")
        return 1

    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1

    mes_fields = set(selected_contracts["MESU6"])
    mnq_fields = set(selected_contracts["MNQU6"])

    print()
    print("=" * 88)
    print("Metadata schema comparison")
    print(f"MESU6 fields:               {len(mes_fields)}")
    print(f"MNQU6 fields:               {len(mnq_fields)}")
    print(
        "Common fields:             "
        f"{len(mes_fields & mnq_fields)}"
    )

    only_mes = sorted(mes_fields - mnq_fields)
    only_mnq = sorted(mnq_fields - mes_fields)

    print(
        "Fields present only on MESU6: "
        f"{', '.join(only_mes) if only_mes else 'None'}"
    )
    print(
        "Fields present only on MNQU6: "
        f"{', '.join(only_mnq) if only_mnq else 'None'}"
    )

    print()
    print("Metadata comparison complete.")
    print("No data was written to disk.")

    return 0


if __name__ == "__main__":
    sys.exit(main())