import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def train_rf(input_csv="data/processed/dataset_clean.csv"):
    df = pd.read_csv(input_csv)
    X = df.drop("label", axis=1)
    y = df["label"]

    model = RandomForestClassifier(n_estimators=300)
    model.fit(X, y)

    with open("models/rf_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Random Forest trained and saved!")
