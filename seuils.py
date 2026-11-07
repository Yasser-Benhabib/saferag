import csv
import statistics
from sklearn.metrics import f1_score, precision_score, recall_score
modeles = ["protectai","pg2"]
seuils = [0.9, 0.5, 0.2, 0.1, 0.05, 0.01, 0.001, 0.0005, 0.0002, 0.0001]
jeux = ["validation","test_public","mes_docs"]

def load_scores(path) : 
    labels ,scores = [],[]
    with open(path , encoding="utf-8",newline="") as f :
        for r in csv.DictReader(f):
            labels.append(int(r["label"]))
            scores.append(float(r["score"]))
    return labels,scores

def predire(scores,seuil) : 
    return [1 if i>= seuil else 0 for i in scores]

for model in modeles : 
    for jeu in jeux :
        labels,scores= load_scores(f"scores/{model}_{jeu}.csv")
        print(f"\n=== {model} sur {jeu} ({len(labels)} textes) ===")
        for s in seuils : 
            p = predire(scores,s)
            print(f"seuil {s:<6} rappel {recall_score(labels, p):.2f}"f"  précision {precision_score(labels, p, zero_division=0):.2f}"f"  F1 {f1_score(labels, p, zero_division=0):.2f}")
for model in modeles : 
    labels , scores = load_scores(f"scores/{model}_validation.csv")
    meilleur_seuil , meilleur_f1 =None,-1
    for s in  seuils: 
        f1 = f1_score(labels,predire(scores,s),zero_division = 0)
        if f1 > meilleur_f1 : meilleur_seuil,meilleur_f1 = s,f1
    print(f"\n{model} : meilleur seuil {meilleur_seuil} (F1 :{meilleur_f1} sur validation)")
    for j in ["test_public","mes_docs"]:
        labels,scores=load_scores(f"scores/{model}_{j}.csv")
        p = predire(scores,meilleur_seuil)
        print(f"Jeu : {j} || Rappel : {recall_score(labels,p):.2f} || Precision : {precision_score(labels,p,zero_division=0):.2f}")

labels, scores = load_scores("scores/pg2_validation.csv")
normaux = [s for l, s in zip(labels, scores) if l == 0]
attaques = [s for l, s in zip(labels, scores) if l == 1]
print("\nScore médian de pg2 sur la validation : normaux", round(statistics.median(normaux), 5),
      "| attaques", round(statistics.median(attaques), 5))