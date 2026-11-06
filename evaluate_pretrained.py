import time

from sklearn.metrics import confusion_matrix, precision_score, recall_score
from transformers import pipeline

from data import load_dataset


MODELE= "meta-llama/Llama-Prompt-Guard-2-86M"
classifier = pipeline("text-classification",model=MODELE,truncation=True,max_length=512)
LABEL_ATTAQUE =classifier.model.config.id2label[1]
print("Modèle : ",MODELE)
print("Label d attaque :",LABEL_ATTAQUE)

def predire(textes):
    res = classifier(textes)
    return [1 if i["label"]== LABEL_ATTAQUE else 0 for i in res]

def afficher(nom,rows) : 
    textes = [i for i,j in rows]
    vraies =[j for i,j in rows]
    d = time.time()
    pred = predire(textes) #les predictions
    durée = time.time() - d
    tn,fp,fn,tp = confusion_matrix(vraies,pred).ravel()
    print(nom," :",len(rows), "textes ,en",round(durée,1),"secondes .")
    print("TP:", tp, "FP:", fp, "TN:", tn, "FN:", fn)
    print("Rappel :",round(recall_score(vraies,pred),2))
    print("Precision :",round(precision_score(vraies,pred,zero_division=0),2))
    return textes,vraies,pred

afficher("Test public",load_dataset("public_test.csv"))
textes , vraies,pred = afficher("Mes documents",load_dataset("dataset.csv"))

print("\nErreurs sur mes docs")
for txt,label,pred in zip(textes,vraies,pred)  :
    if label==1 and pred == 0 :
        print("Attaque ratée :",txt)
    elif label ==0 and pred == 1 : 
        print("Fausse alerte :",txt)