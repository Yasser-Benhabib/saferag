from detector import is_attack
import csv

def load_dataset(path):
    rows=[]
    with open(path,encoding="utf-8")  as f :
        for row in csv.DictReader(f) : 
            rows.append((row["text"], int(row["label"])))
    return rows

DATASET = load_dataset("dataset.csv")
tp =tn = fp = fn = 0
for text, label in DATASET :
    prediction = is_attack(text)
    if prediction and label == 1 :
        tp+=1
    elif prediction and label == 0 : 
        fp+=1
    elif not prediction and label ==1 :
        fn +=1
    else : 
        tn+=1
rappel = tp/(tp + fn) if tp + fn > 0 else 0
precision = tp/(tp + fp) if tp + fp > 0 else 0

print("TP:", tp, "FP:", fp, "TN:", tn, "FN:", fn)
print("Rappel =", round(rappel, 2))
print("Précision =", round(precision, 2))