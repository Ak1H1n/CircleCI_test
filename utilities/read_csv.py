import csv

def read_csv_data(csv_path):
    rows = []
    with open(str(csv_path), encoding="utf-8") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)
        print(rows)
        return rows