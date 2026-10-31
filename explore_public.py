from data import load_dataset


train = load_dataset("public_train.csv")
test= load_dataset("public_test.csv")
for nom , rows in [("Entrainement",train),("Test",test)] : 
    attaques = sum(label for text,label in rows)
    print(nom,":",len(rows),"textes dont",attaques,"attaques")

attaques= [text for text,label in train if label ==1]
normaux = [text for text,label in train if label == 0]

print("\n---5 attaques ---")
for text in attaques[:5] :
    print("-", text[:120])
print("\n---5 textes normaux ---")
for text in normaux[:5] :
    print("-", text[:120])
