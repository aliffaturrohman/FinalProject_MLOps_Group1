import pandas as pd

def json_to_csv(json_file, csv_file):
    df = pd.read_json(json_file, lines=True)
    df.to_csv(csv_file, index=False)
    print(f"The CSV file has been successfully saved as {csv_file}")

path_json = r"dataset/News_Category_Dataset.json"
path_to_csv = r"dataset/news_dataset.csv"

json_to_csv(path_json, path_to_csv)
