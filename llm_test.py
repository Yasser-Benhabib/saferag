import time 
import ollama
MODELE_LLM = "llama3.2:3b"
questions = [
    "Explique en deux phrases ce qu'est un chatbot RAG.",
    "Combien de jours ai-je pour être remboursé chez Zentra ?",
]
for ques in questions : 
    d= time.time()
    reponse = ollama.chat(
        model = MODELE_LLM,
        messages = [{"role" : "user" , "content" : ques}],
    )
    duree = time.time() -d 
    print(f"\nQuestion : {ques}")
    print(f"Réponse ({duree:.1f} s) : {reponse.message.content}")
