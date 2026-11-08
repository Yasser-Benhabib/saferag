import csv 
S_BLOQUER = 0.5 # seuil
S_VERIFIER = 0.001 

def verdict(score): 
    if score >= S_BLOQUER :
        return "BLOQUER"
    elif score >= S_VERIFIER : 
        return "VERIFIER"
    return "AUTORISER"

for j in ["test_public","mes_docs"] : 
    d = {}
    with open(f"scores/pg2_{j}.csv",encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f) :
            cle = (verdict(float(r["score"])),"attaque" if r["label"] == "1" else "normal")
            d[cle] = d.get(cle,0)+1
        print(f"\n--- {j} ---")
        for i in ["BLOQUER","VERIFIER","AUTORISER"] :
            print(
                f"{i} attaques : {d.get((i,'attaque'),0)} || normaux : {d.get((i,'normal'))}"
            )