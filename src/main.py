import argparse
import requests
import os
from dotenv import load_dotenv

def get_api_key(provided_key):
    if provided_key:
        return provided_key
    
    load_dotenv()
    env_key = os.getenv("API_KEY")
    
    if not env_key:
        raise ValueError("No API key provided. Use --key or add API_KEY to .env file")
    
    return env_key


def convert_currency(api_key, amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Error fetching data from API")
    
    data = response.json()
    
    if to_currency not in data["conversion_rates"]:
        raise ValueError("Invalid target currency")
    
    rate = data["conversion_rates"][to_currency]
    converted_amount = amount * rate
    
    return converted_amount


def main():
    parser = argparse.ArgumentParser(description="Currency Converter CLI")

    parser.add_argument("--key", help="API key for exchangerate-api")
    parser.add_argument("--amount", type=float, required=True, help="Amount to convert")
    parser.add_argument("--from_currency", required=True, help="Currency to convert from (e.g. USD)")
    parser.add_argument("--to_currency", required=True, help="Currency to convert to (e.g. EUR)")

    args = parser.parse_args()

    api_key = get_api_key(args.key)

    result = convert_currency(api_key, args.amount, args.from_currency.upper(), args.to_currency.upper())

    print(f"{args.amount} {args.from_currency.upper()} = {result:.2f} {args.to_currency.upper()}")


if __name__ == "__main__":
    main()