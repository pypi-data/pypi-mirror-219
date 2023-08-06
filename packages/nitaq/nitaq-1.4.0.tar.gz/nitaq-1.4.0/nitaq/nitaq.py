import pandas as pd
def get_lob(df):
    column_names = df.columns
    for pattern in ["lob", "market_segment", "product", "class_of_business",'type']:
        matching_columns = [col for col in column_names if pattern in col.lower()]
        if matching_columns:
            return sorted(matching_columns, key=len)[0]
    return None

def quarters(df):
    valid_cols = []
    df = df.applymap(lambda x: str(int(x)) if isinstance(x, (int, float)) and str(x) != 'nan' else str(x))
    for col in df.columns:
        # Check if all values in column are either 'nan' or numeric
        if all(df[col].apply(lambda x: str(x).isnumeric() or str(x) == 'nan')):
            # Check if column has at least one value with length of 6
            if any(df[col].apply(lambda x: len(str(x))) == 6):
                # Check if all non-zero numeric values end with '03', '06', '09', or '12'
                filtered = df[df[col] != '0']
                filtered = filtered[filtered[col].apply(lambda x: str(x).isnumeric())]
                if filtered[col].apply(lambda x: x[-2:]).isin(['03', '06', '09', '12']).all():
                    valid_cols.append(col)
    valid_cols = [elem for elem in valid_cols if "report" not in elem.lower() if "effect" not in elem.lower()]
    return valid_cols

def yearlize(df, column_list):
    df_modified = df.copy()
    names = []
    for column_name in column_list:
        column_values = df_modified[column_name].astype(str)
        last_character = column_values.str[-1]
        sliced_values = column_values
        sliced_values = sliced_values.where(~last_character.isin(['3', '6']), column_values.str[:4])
        sliced_values = sliced_values.where(~last_character.isin(['9', '2']), column_values.str[:4].astype(int) + 1)
        new_column = 'c'
        if 'accident' in column_name.lower():
            new_column = 'Accident_mapped'
        elif 'transaction' in column_name.lower():
            new_column = 'Paid_mapped'
        elif 'quarter' in column_name.lower():
            new_column = 'yearly_bracket'
        df_modified[new_column] = sliced_values
        names.append(new_column)
    return df_modified,names

def min_year(df, column_list, min_year):
    df_modified = df.copy()
    
    for column_name in column_list:
        df_modified[column_name] = pd.to_numeric(df_modified[column_name], errors='coerce')
        df_modified = df_modified[df_modified[column_name] >= min_year]
    
    return df_modified

def ener_engi(df, column_name):
    df_filtered = df[df[column_name].str.lower().str.contains('engineering|energy', case=False)]
    return df_filtered

def yearly_basis(file_name):
    try:
        df = pd.read_excel(file_name)
    except:
        df = pd.read_csv(file_name)
    # get lob
    lob = get_lob(df)
    # get quarter names
    columns = quarters(df)
    # energy and engineering only
    removed_rows = ener_engi(df,lob)
    # yearly basis
    yearly,names = yearlize(removed_rows,columns)
    # force minimum year
    filtered = min_year(yearly,names,2014)
    return filtered