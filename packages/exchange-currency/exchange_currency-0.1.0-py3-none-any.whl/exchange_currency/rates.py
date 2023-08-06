import requests


def get_rates(appID, base, target):
    url = f"https://openexchangerates.org/api/latest.json?app_id={appID}&base={base}"
    response = requests.get(url)
    print(f"Base {response.json()['base']}")
    print(f"ExchangeRate {base}:{target}|1:{response.json()['rates'][target]}")
