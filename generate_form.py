import pandas as pd

country_code_dict = {'WO': 'World', 'BR': 'Brazil', 'CN': 'China, P.R.: Mainland',
                     'EZ': 'Euro Area', 'GB': 'United Kingdom', 'IN': 'India',
                     'JP': 'Japan', 'MX': 'Mexico', 'RU': 'Russia', 'US': 'United States', 'ZA': 'South Africa'}


def get_index_as_list(df, inflation):
    if inflation:

        countries = []

        for code in df:
            country_code = country_code_dict.get(code[-2:])
            countries.append(country_code)

    else:
        countries = df.index.to_list()
    return countries



#%%

def get_selected_dataframes(selected_data, gpmn_dict_of_dfs):
    selected_data_df = pd.DataFrame()

    for data in selected_data:

        # Get headline cpi by country
        data_df = gpmn_dict_of_dfs.get(data)
        data_df.columns = get_index_as_list(data_df, True)

        # Get concatenated dataframe
        data_df.columns = data_df.loc['Comments ->']
        data_df = data_df.drop(index=['Comments ->', '1999Q1', '1999Q2', '1999Q3', '1999Q4'])
        selected_data_df = pd.concat([selected_data_df, data_df], axis=1)
    return selected_data_df
