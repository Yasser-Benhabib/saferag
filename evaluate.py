from detector import is_attack
from data import load_dataset

def evaluate(rows):
    tp =tn = fp = fn = 0

    for text, label in rows :
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
    return tp,fp,tn,fn, rappel , precision

def show(name,rows) :
    tp,fp,tn,fn,rappel,precision= evaluate(rows)
    print(name,":",len(rows),"textes")
    print("TP:", tp, "FP:", fp, "TN:", tn, "FN:", fn)
    print("Rappel =", round(rappel, 2))
    print("Précision =", round(precision, 2))

if __name__=="__main__" :
    show("Mon jeu de données",load_dataset("dataset.csv"))