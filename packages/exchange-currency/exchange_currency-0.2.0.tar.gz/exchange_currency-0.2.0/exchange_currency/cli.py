import argparse
from exchange_currency.rates import get_rates
from exchange_currency.config import Config


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-B", "--base", help="choose a certain base")
    argParser.add_argument("-T", "--target", help="choose a certain target currency")

    args = argParser.parse_args()
    get_rates(Config.appID, args.base, args.target)


if __name__ == "__main__":
    main()
