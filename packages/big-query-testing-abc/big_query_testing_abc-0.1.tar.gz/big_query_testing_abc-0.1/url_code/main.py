import pandas as pd
import requests

url = 'https://us-central1-taxfiling-aggregation.cloudfunctions.net/filings-summary?parm_name=tab_2019_N1'

response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)


def get_first_row_state(state_code):
    """
    This function will return the first row of the filtered dataframe with the desired state.
    """
    df_filtered = df[(df['STATE'] == state_code)]
    return df_filtered.iloc[0]
