import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

import src.internet_connection as internet_connection
from src.currency_exchange import CurrencyExchange


class ConverterApp:
    """A class to provide a simple currency converter app"""
    def __init__(self):
        """Initialize an app window and text resources"""
        self.root = tk.Tk()
        self.root.title('Przelicznik walut')
        self.root.resizable(False, False)
        ttk.Style(self.root)

        self.local_save_path = Path('../data/exchange_rates.csv')

        self.text_combobox_convert_from = tk.StringVar()
        self.text_combobox_convert_to = tk.StringVar()
        self.text_entry_convert_to = tk.StringVar()
        self.text_label_final_currency = tk.StringVar()
        self.text_label_init_currency = tk.StringVar()
        self.text_label_info = tk.StringVar()

        self.available_currencies = []
        self.current_exchanges = CurrencyExchange()

    def get_data(self):
        """Check if connected to internet, and then get online/offline data or inform that it is not possible"""
        if internet_connection.is_connected():
            self.current_exchanges.read_from_api()
            self.current_exchanges.save_to_csv(self.local_save_path)
            self.text_label_info.set("Połączono z internetem: kursy pobrano ze strony NBP.")
        else:
            try:
                self.current_exchanges.read_from_csv(self.local_save_path)
                local_save_time = datetime.fromtimestamp(self.local_save_path.lstat().st_mtime)
                local_save_date = str(local_save_time.strftime("%d-%m-%Y %H:%M"))
                self.text_label_info.set(f"Brak internetu: kursy pobrano z lokalnego zapisu"
                                         f"\n(ostatnio zaaktualizowany: {local_save_date}).")
            except FileNotFoundError:
                self.text_label_info.set("Brak internetu: nie znaleziono żadnych kursów (lokalny zapis nie istnieje)."
                                         "\nPołącz z internetem i zrestartuj program aby pobrać kursy.")
                messagebox.showerror(title="Błąd", message="Brak połączenia z internetem.\nKursy nie zostały pobrane")

        self.available_currencies = self.current_exchanges.get_available_currencies()

    def show_window(self):
        """Start GUI"""
        def click_button():
            """To execute if button is clicked"""
            try:
                init_currency = combobox_convert_to.get()
                final_currency = combobox_convert_from.get()
                init_value = float(entry_convert_from.get().replace(',', '.', 1))
                final_value = self.current_exchanges.convert(init_value, init_currency, final_currency)
                self.text_entry_convert_to.set(final_value)
                self.text_label_final_currency.set(self.current_exchanges.get_currency_code(combobox_convert_to.get()))
            except ValueError:
                messagebox.showerror(title="Błąd", message="Upewnij się, czy wszystkie dane zostały wprowadzone poprawnie")

        def update_label_from(event):
            """Update the initial currency code label (the one next to the text box)"""
            self.text_label_init_currency.set(self.current_exchanges.get_currency_code(combobox_convert_from.get()))

        frame0 = ttk.Frame(self.root)
        frame0.grid(padx=10, pady=10)
        label_convert_from = ttk.Label(frame0, text='Przelicz z')
        label_convert_from.grid(column=0, row=0, padx=5, pady=5)
        combobox_convert_from = ttk.Combobox(frame0, state='readonly', values=self.available_currencies,
                                             textvariable=self.text_combobox_convert_from)
        combobox_convert_from.grid(column=1, row=0, padx=5, pady=5)
        combobox_convert_from.bind('<<ComboboxSelected>>', update_label_from)
        label_convert_to = ttk.Label(frame0, text='na')
        label_convert_to.grid(column=2, row=0, padx=5, pady=5)
        combobox_convert_to = ttk.Combobox(frame0, state='readonly', values=self.available_currencies,
                                           textvariable=self.text_combobox_convert_to)
        combobox_convert_to.grid(column=3, row=0, padx=5, pady=5)

        frame1 = ttk.Frame(self.root)
        frame1.grid(padx=10, pady=10)
        entry_convert_from = ttk.Entry(frame1)
        entry_convert_from.grid(column=1, row=1, padx=5, pady=5)
        self.text_label_final_currency.set("---")
        label_init_currency = ttk.Label(frame1, textvariable=self.text_label_init_currency)
        label_init_currency.grid(column=2, row=1, padx=5, pady=5)
        label_arrow = ttk.Label(frame1, text='to w przeliczeniu')
        label_arrow.grid(column=3, row=1, padx=5, pady=5)
        entry_convert_to = ttk.Entry(frame1, state='readonly', textvariable=self.text_entry_convert_to)
        entry_convert_to.grid(column=4, row=1, padx=5, pady=5)
        self.text_label_init_currency.set("---")
        label_final_currency = ttk.Label(frame1, textvariable=self.text_label_final_currency)
        label_final_currency.grid(column=5, row=1, padx=5, pady=5)

        frame2 = ttk.Frame(self.root)
        frame2.grid(padx=10, pady=10)
        button_start = ttk.Button(frame2, text='Przelicz', default="active", command=click_button)
        button_start.grid(column=1, row=2, padx=5, pady=5)
        button_close = ttk.Button(frame2, text='Zamknij', default="normal", command=self.root.destroy)
        button_close.grid(column=2, row=2, padx=5, pady=5)

        frame3 = ttk.Frame(self.root)
        frame3.grid(padx=10, pady=10)
        label_info = ttk.Label(frame3, textvariable=self.text_label_info, justify="center")
        label_info.grid(column=0, row=3)


def main():
    app = ConverterApp()
    app.get_data()
    app.show_window()
    app.root.mainloop()


if __name__ == "__main__":
    main()
