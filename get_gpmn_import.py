import pandas as pd
import re


def clean_cell(cell):
    if type(cell) == str:
        cell = cell.replace('r', '')
        cell = cell.replace(',', '')
        return float(cell)


def get_percent_df(df, divider):
    percentage_df = df.div(divider, axis=0)
    percentage_df.drop(columns='World', axis=0)

    return percentage_df


def get_import_df(path, yearly):
    import_df = pd.read_excel(path, index_col=0)
    for col in import_df:
        if re.search('Q[1-4]$', col) and col != 'Country' and yearly:
            import_df = import_df.drop(columns=[col], axis=1)

        else:
            # Clean Cell Data
            for code in import_df:
                for i in import_df[code]:
                    i = clean_cell(i)

    import_df = import_df.transpose()

    import_df = get_percent_df(import_df, import_df.World)

    return import_df


def get_year_index_list(df):
    year_lst = df.index.tolist()
    for year in range(len(year_lst)):
        year_lst[year] = year_lst[year][:-1]
    return year_lst


def change_year_index(gpmn_df, dict_of_dfs):
    year_lst = get_year_index_list(gpmn_df)

    for df in list(dict_of_dfs.values()):
        df.index = year_lst

    return dict_of_dfs


def get_gpmn_dfs(path_to_gpmn, yearly):
    gpmn_df = pd.read_csv(path_to_gpmn, index_col=0)
    # Get headline cpi code
    headline_cpi_codes = []
    core_cpi_codes = []
    nominal_interest_codes = []
    real_output_change_codes = []
    real_interest_codes = []
    interest_lcy_codes = []

    for code in gpmn_df:

        if code.find('DOT4_CPI_') != -1:
            headline_cpi_codes.append(code)

        elif code.find('NC_RS_') != -1:
            nominal_interest_codes.append(code)

        elif re.search('D4L_GDP_..$', code):
            real_output_change_codes.append(code)

        elif code.find('DOT4_CPIXFE_') != -1:
            core_cpi_codes.append(code)

        elif re.search('RR_..$', code):
            real_interest_codes.append(code)

        elif re.search('^S_[A-Z][A-Z]$', code):
            if code not in interest_lcy_codes:
                interest_lcy_codes.append(code)

    # Create Dataframes by codes
    headline_cpi_df = gpmn_df[headline_cpi_codes]
    nominal_interest_df = gpmn_df[nominal_interest_codes]
    real_output_change_df = gpmn_df[real_output_change_codes]
    core_cpi_df = gpmn_df[core_cpi_codes]
    real_interest_df = gpmn_df[real_interest_codes]
    interest_lcy_df = gpmn_df[interest_lcy_codes]
    # Create dictionary made of dataframes:
    dict_of_df = {'headline_cpi': headline_cpi_df, 'nominal_interest': nominal_interest_df,
                  'real_interest': real_interest_df, 'core_cpi': core_cpi_df,
                  'real_output': real_output_change_df, 'interest_lcy': interest_lcy_df}

    if yearly:
        # Remove Y from end of year
        dict_of_df = change_year_index(gpmn_df, dict_of_df)
    else:
        pass

    return dict_of_df

