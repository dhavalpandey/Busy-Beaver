import os
import joblib
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import metrics

def main():
    model_path = os.path.join("ML", "logistic_model.pkl")
    test_csv   = os.path.join("data", "test", "test.csv")
    out_dir    = os.path.join("ML", "outcomes")
    os.makedirs(out_dir, exist_ok=True)

    print("Loading model…")
    bundle = joblib.load(model_path)
    # if you pickled a dict, unpack
    if isinstance(bundle, dict):
        clf = bundle.get("model") or bundle.get("clf")
        le  = bundle.get("le", None)
    else:
        clf = bundle
        le  = None

    if clf is None:
        raise RuntimeError("No classifier found inside the pickle.")

    all_true = []
    all_pred = []

    print(f"Streaming test data from `{test_csv}`…")
    reader = pd.read_csv(test_csv, chunksize=10_000)
    for df in tqdm(reader, desc="Testing"):
        raw = df["status"].values
        if le:
            y = le.transform(raw)
        else:
            y = (raw == "halt").astype(np.int8)

        X = df.drop(columns=["status"]).values.astype(np.int8)
        preds = clf.predict(X)

        all_true.append(y)
        all_pred.append(preds)

    y_true = np.concatenate(all_true)
    y_pred = np.concatenate(all_pred)

    acc  = metrics.accuracy_score(y_true, y_pred)
    prec = metrics.precision_score(y_true, y_pred, zero_division=0)
    rec  = metrics.recall_score(y_true, y_pred, zero_division=0)
    f1   = metrics.f1_score(y_true, y_pred, zero_division=0)
    cm   = metrics.confusion_matrix(y_true, y_pred).tolist()

    report = {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": cm,
        "support": {
            "halt": int((y_true == 1).sum()),
            "nonhalt": int((y_true == 0).sum())
        }
    }

    with open(os.path.join(out_dir, "metrics.json"), "w") as jf:
        json.dump(report, jf, indent=2)
    with open(os.path.join(out_dir, "metrics.txt"), "w") as tf:
        tf.write("Test set evaluation:\n")
        tf.write(f"  Accuracy : {acc:.6f}\n")
        tf.write(f"  Precision: {prec:.6f}\n")
        tf.write(f"  Recall   : {rec:.6f}\n")
        tf.write(f"  F1 score : {f1:.6f}\n")
        tf.write("  Confusion matrix (rows=true, cols=pred):\n")
        for row in cm:
            tf.write(f"    {row}\n")
        tf.write(f"\nSupport: {report['support']}\n")

    print("Done. Metrics written to:", out_dir)


if __name__ == "__main__":
    main()
