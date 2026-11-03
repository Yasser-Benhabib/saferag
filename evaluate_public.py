from langdetect import detect, DetectorFactory
from data import load_dataset
from detector import is_attack
from evaluate import show

DetectorFactory.seed = 0

test = load_dataset("public_test.csv")
show("Jeu public, tout le test",test)

anglais = [(text,label) for text,label in test if detect(text) =="en"]
show("Jeu public : textes anglais",anglais)
ratées = [text for text,label in anglais if not is_attack(text) and label==1]
print("\n---5 attaques anglais ratées---")

for i in ratées[:5] :
    print('-', i[:120])