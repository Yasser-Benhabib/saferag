import ollama 
from recherche import charger_morceaux,chercher,indexer
import time

MODELE_LLM = "llama3.2:3b"
seuil = 0.4

CONSIGNES = """Tu es l'assistant du service client de Zentra, une boutique en ligne.
Réponds en français, en deux ou trois phrases.
Réponds seulement à partir des extraits ci-dessous.
Si la réponse n'est pas dans les extraits, dis que tu ne sais pas."""

def repondre(quest, morceaux,vecteurs) : 
    list_proches = chercher(quest,morceaux,vecteurs,k=3) 
    new_l = [p for p in list_proches if p[0] >=0.4] #laisser seuelement ceux qui ont au dessus de seuil 
    
    if not new_l : 
        return "Je ne trouve pas cette information dans nos documents.", []
    extraits = ""
    for score,nom,morceau in new_l  :
        extraits +=f"[{nom}] {morceau}\n"
    reponse = ollama.chat(
        model = MODELE_LLM,
        messages=[{"role" : "system" , "content" : CONSIGNES + "\n\nExtraits :\n" + extraits},
                {"role" : "user","content" :quest},],
    )                            
    sources = sorted(set([nom for sc,nom,morc in new_l]))
    return reponse.message.content,sources



if __name__ == "__main__":
    morceaux = charger_morceaux("base")
    vecteurs = indexer(morceaux)
    questions = [
        "Combien de jours ai-je pour être remboursé ?",
        "Is shipping free?",
        "Vendez-vous des téléphones pliables ?",
    ]
    for question in questions:
        texte, sources = repondre(question, morceaux, vecteurs)
        print(f"\nQuestion : {question}")
        print(f"Réponse : {texte}")
        print(f"Sources : {sources}")