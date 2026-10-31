import csv
def load_dataset(path) : 
    rows = []
    with open(path,encoding="utf-8") as f :
        for row in csv.DictReader(f) :
            rows.append((row["text"],int(row["label"])))
    return rows