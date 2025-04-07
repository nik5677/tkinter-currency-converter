import csv

import requests


class CurrencyExchange:
    """A class to provide a Polish złoty (PLN) foreign currency exchange rates.

    Attributes:
        exchange_rates: a list that contains each currency data in tuple: name, ISO 4217 code, average exchange rate
    """

    def __init__(self) -> None:
        """Initialize ExchangeRates object with an empty exchange rates list"""
        self.exchange_rates = list()

    def read_from_api(self) -> None:
        """Read current foreign exchange rates from National Bank of Poland website"""
        url = 'https://api.nbp.pl/api/exchangerates/tables/A'
        response = requests.get(url)
        data = response.json()

        rates = data[0]['rates']
        for rate in rates:
            rate_tuple = (rate['currency'], rate['code'], rate['mid'])
            self.exchange_rates.append(rate_tuple)
        pln = ('złoty polski', 'PLN', '1')
        if pln not in self.exchange_rates:
            self.exchange_rates.append(pln)

    def save_to_csv(self, file_path: str) -> None:
        """Save the exchange rates to a csv file"""
        if not self.exchange_rates:
            raise ValueError('Exchange rates list is empty!')

        fieldnames = ['currency', 'code', 'mid']
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for currency_tuple in self.exchange_rates:
                writer.writerow({'currency': currency_tuple[0], 'code': currency_tuple[1], 'mid': currency_tuple[2]})

    def read_from_csv(self, file_path: str) -> None:
        """Read foreign exchange rate from previously saved csv file"""
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.exchange_rates = []
            for row in reader:
                self.exchange_rates.append((row['currency'], row['code'], row['mid']))
            pln = ('złoty polski', 'PLN', '1')
            if pln not in self.exchange_rates:
                self.exchange_rates.append(pln)

    def get_currency_data(self, name: str) -> tuple:
        """Return a tuple containing an exchange rate data relative to its name"""
        for exchange_rate in self.exchange_rates:
            if name in exchange_rate:
                return exchange_rate
        raise ValueError('Invalid currency name!')

    def get_available_currencies(self) -> list:
        """Return a list of available currencies"""
        available_currencies = []
        for exchange_rate in self.exchange_rates:
            available_currencies.append(exchange_rate[0])
        return available_currencies

    def convert(self, value: float or int, convert_from: str, convert_to: str) -> float:
        """Return converted currency value"""
        initial_currency = self.get_currency_data(convert_from)[2]
        final_currency = self.get_currency_data(convert_to)[2]
        return round((float(final_currency) * value) / float(initial_currency), 2)

    def get_currency_code(self, name: str) -> str:
        for exchange_rate in self.exchange_rates:
            if name in exchange_rate:
                return exchange_rate[1]
        raise ValueError('Invalid currency name!')
