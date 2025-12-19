import shap, pickle, pandas as pd

def explain(model_path, df):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)

    shap.summary_plot(shap_values, df)