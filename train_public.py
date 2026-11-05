from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score

from data import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer

train = load_dataset("public_train.csv")
test = load_dataset("public_test.csv")
X_train = [i for i,j in train ]
y_train = [j for i,j in train]

X_test=[i for i,j in test]
y_test = [j for i,j in test]

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec,y_train)
predictions =model.predict(X_test_vec)

tn,fp,fn,tp = confusion_matrix(y_test,predictions).ravel()
print("TP:", tp, "FP:", fp, "TN:", tn, "FN:", fn)
print("Rappel : ",round(recall_score(y_test,predictions),2))
print("Précision : ", round(precision_score(y_test, predictions), 2))

vide = vectorizer.transform([""])
print("Texte vide ->",model.predict(vide)[0])

coefs = sorted(zip(model.coef_[0],vectorizer.get_feature_names_out()))
print("Mots vers 'attaque' :",[mot for c,mot, in coefs[-15:]])
print("Mots vers 'normal' :", [mot for c, mot in coefs[:10]])

####################################################
mes_docs = load_dataset("dataset.csv")
X_mes = [i for i,j in mes_docs]
y_mes = [j for i,j in mes_docs]

predictions_mes = model.predict(vectorizer.transform(X_mes))
tn,fp,fn,tp = confusion_matrix(y_mes,predictions_mes).ravel()
print("\n--- Evaluation sur mes 57 documents ---")
print("TP:", tp, "FP:", fp, "TN:", tn, "FN:", fn)
print("Rappel : ",round(recall_score(y_mes,predictions_mes),2))
print("Précision : ", round(precision_score(y_mes, predictions_mes), 2))

print("\n---Les erreurs---")
for text,label,pred in zip(X_mes,y_mes,predictions_mes) : 
    if label == 1 and pred ==0 : 
        print("Attaque raté:",text)
    elif label == 0 and pred == 1 :
        print("Fausse alerte:",text)