import pandas as pd
import xlrd
import openpyxl

country_code_dict = {'WO': 'World', 'BR': 'Brazil', 'CN': 'China, P.R.: Mainland',
                     'EZ': 'Euro Area', 'GB': 'United Kingdom', 'IN': 'India',
                     'JP': 'Japan', 'MX': 'Mexico', 'RU': 'Russia', 'US': 'United States', 'ZA': 'South Africa'}

exchange_rates = {'2000': 4.071662, '2001': 4.20319, '2002': 4.744882, '2003': 4.76, '2004': 4.519921, '2005': 4.485712,
                  '2006': 4.457282, '2007': 4.112041, '2008': 3.582559, '2009': 3.902731, '2010': 3.734313,
                  '2011': 3.577075, '2012': 3.855556, '2013': 3.609841, '2014': 3.576907, '2015': 3.885835,
                  '2016': 3.839699, '2017': 3.597737, '2018': 3.595276, '2019': 3.562846}


def get_excel_as_df(path):
    return pd.read_excel(path, index_col=0)


def get_year_weight(inflation_df, import_df, rows_in_df, year):
    year_weight_list = []

    # Get countries as lists
    inflation_countries = inflation_df.columns.to_list()
    import_countries = import_df.columns.to_list()
    import_df.index = list(inflation_df.index)[5:-23]
    # print(list(inflation_df.index)[5:-23])
    # Iterate over each country
    for country in inflation_countries:
        if country in import_countries:

            # If data does not exists => assign 2019 data
            try:
                import_value = float(import_df.loc[year][country])

            except:
                import_value = float(import_df.loc['2019Q1'][country])

            # Get exchange rate and if data does not exists => assign 2019 data
            exchange_rate = exchange_rates.get(year)

            if exchange_rate is None:
                exchange_rate = exchange_rates.get('2019')

            # Multiply base by exchange rate in base year
            inflation_value_base = float(inflation_df.loc['1999Q1'][country]) * 4.15

            # Multiply exchange rate by usd to ils exchange rate in current year
            inflation_value = float(inflation_df.loc[year][country]) * exchange_rate / inflation_value_base

            if pd.notna(import_value) and pd.notna(inflation_value):  # Check that values are not null
                # Format data to 3 decimal points
                inflation_pow_import_share = float("{:.3f}".format(inflation_value ** import_value))

                # Avoiding powering by zero
                if inflation_pow_import_share != 0 and pd.notna(inflation_pow_import_share):  # Check that powered value is valid
                    year_weight_list.append({country: inflation_pow_import_share})

    return year_weight_list


def get_trade_weight_list(inflation_df, import_df, year_start, year_end):
    trade_weight_list = []

    # Iterate over years
    for year in range(year_start, year_end + 1):  # Iterate over years
        for quarter in range(1, 5):
            rows_in_df = inflation_df.loc[str(year) + 'Q' + str(quarter)].shape[0]  # Number of Rows in DF

            # Append TWI attribution to dictionary
            year_weight_list = get_year_weight(inflation_df, import_df, rows_in_df, str(year) + 'Q' + str(quarter))
            trade_weight_list.append({str(year) + 'Q' + str(quarter): year_weight_list})

    return trade_weight_list


def get_twi_by_year(inflation_df, import_df, year_start, year_end):
    trade_weight_list = get_trade_weight_list(inflation_df, import_df, year_start, year_end)
    twi_by_year = {}

    # For each year calculate TWI
    for year in trade_weight_list:
        twi = 1
        for value in year.values():
            for country in value:
                if pd.notna(list(country.values())[0]):  # and list(country.values())[0] != 0:
                    twi *= list(country.values())[0]
            curr_year = str(list(year.keys())[0])

            twi_by_year[curr_year] = twi

    return twi_by_year
