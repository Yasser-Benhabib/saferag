from datasets import load_dataset as hf_load

ds = hf_load("deepset/prompt-injections")
print(ds)

ds["train"].to_csv("public_train.csv",index=False)
ds["test"].to_csv("public_test.csv",index= False)
print("Fichiers enregistés : public_train.csv et public_test.csv")