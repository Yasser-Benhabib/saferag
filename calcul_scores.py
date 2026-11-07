from data import load_dataset
import os
import csv
from transformers import pipeline  as p 

modeles = {
    "protectai":"protectai/deberta-v3-base-prompt-injection-v2",
    "pg2":"meta-llama/Llama-Prompt-Guard-2-86M",
} 
jeux = {
    "validation":"public_train.csv",
    "test_public":"public_test.csv",
    "mes_docs":"dataset.csv",
}

def score(res,label) : #score d attaques d'elements de res avec label d attaque
    for i in res : 
        if i["label"] == label : 
            return i["score"]
os.makedirs("scores",exist_ok=True)
for n,m in modeles.items():
    clas = p("text-classification",model=m,truncation=True,max_length=512) #creation de classifieur de texte
    label_att = clas.model.config.id2label[1]
    for j,f in jeux.items(): 
        rows = load_dataset(f)
        textes = [t for t,l in rows]
        resultats = clas(textes,top_k=None)

        path = f"scores/{n}_{j}.csv"
        with open(path,"w",encoding="utf-8",newline="") as fichier : 
            writer = csv.writer(fichier)
            writer.writerow(["text","label","score"])
            for (text,label), resultat in zip(rows , resultats):
                writer.writerow([text,label,score(resultat,label_att)]) 
        print("Enregisté :",path,len(rows),"textes")