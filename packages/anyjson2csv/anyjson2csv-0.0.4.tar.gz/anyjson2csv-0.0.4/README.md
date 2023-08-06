See the source for this project here: https://github.com/mehdiabidi/json2csv"

(Example)

from anyjson2csv.json_to_csv import convert_json_to_csv
import json

with open("listing_data_sampled.json", "r") as f:
    json_data = json.load(f)

convert_json_to_csv(json_data, "test.csv")
