from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from data import load_dataset

rows = load_dataset("dataset.csv")
texts = [i for i,j in rows]
labels = [j for i,j in rows]

X_train, X_test, y_train , y_test = train_test_split(
    texts,labels, test_size=0.3, random_state=42, stratify=labels
)

print("Entrainement :",len(X_train),"exemples")
print("Test :", len(X_test),"exemples")

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Taille de vocabulaire :",len(vectorizer.vocabulary_))
print("Forme de X_train_vec :",X_train_vec.shape)

mots= vectorizer.get_feature_names_out()
poids = X_train_vec[0].toarray()[0]
print("Texte :", X_train[0])

for mot,p in zip(mots,poids) : 
    if p > 0 :
        print("  ",mot,round(p,2))

model = LogisticRegression()
model.fit(X_train_vec,y_train)
predictions = model.predict(X_test_vec)

for text,label,pred in zip(X_test,y_test,predictions) :
    print(label,pred,"->",text)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
vide = vectorizer.transform([""])
print("Texte vide ->",model.predict(vide)[0],
      "proba attaque :", round(model.predict_proba(vide)[0][1],2))
print(sum(y_train))
print(len(y_train))

probas = model.predict_proba(X_test_vec)[:,1]
for text,p in zip(X_test,probas) :
    print(round(p,2),"->",text)

coefs = sorted(zip(model.coef_[0], vectorizer.get_feature_names_out()))
print("Mots vers 'normal' :",[mot for c,mot in coefs[:8]])
print("Mots vers 'attaque' :",[mot for c,mot in coefs[-8:]])
