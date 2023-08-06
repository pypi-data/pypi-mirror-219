import pandas as pd
from anyjson2csv.flatten_json import flatten


def convert_json_to_csv(json_data, csv_filename):
    try:
        flattened_data = flatten(json_data)

    except Exception as e:
        print("Error occurred while flattening JSON:", str(e))

    try:
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_filename, index=False, encoding="utf-8")

    except:
        print("Error occurred while writing CSV file.")
