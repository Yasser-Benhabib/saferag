import os 
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def indexer(morceaux) : 
    morceaux = [morceau for nom,morceau in morceaux]
    v_morceaux = model.encode(morceaux,normalize_embeddings = True)
    return v_morceaux



def chercher(question,morceaux,vecteurs,k=3) : 
    res = []
    v_ques = model.encode(question,normalize_embeddings= True)
    s = vecteurs @ v_ques
    pos= np.argsort(s)[::-1][:k]
    for i in pos : 
        nom,morceau = morceaux[i]
        res.append((float(s[i]),nom,morceau))
    return res

def decouper(texte) :
    l = []
    for par  in texte.split("\n\n") : 
        par = par.strip()
        if par != "" : 
            l.append(par)
    return l

def charger_morceaux(dossier) : 
    names = sorted(os.listdir(dossier))
    res  = []
    for i in names : 
        chemin = os.path.join(dossier,i)
        with open(chemin,encoding="utf-8") as f : 
            texte = f.read()
        for j in decouper(texte)  : 
            res.append((i,j))
    
    return res

if __name__ == "__main__" :
    morceaux = charger_morceaux("base") 
    vecteurs = indexer(morceaux)
    print("Nombre de morceaux :",len(morceaux)) 
    print("Forme de la base ",vecteurs.shape)
    questions =[
        "Combien de jours ai-je pour etre remboursé ?",
        "Is shipping free?",
        "Vendez-vous des téléphones pliables ?",
    ]
    for ques in questions : 
        print("\nQues :",ques)
        for score,nom,morceau in chercher(ques,morceaux,vecteurs) : 
            print(f"{score:.2f}   {nom}    {morceau[:70]} ")