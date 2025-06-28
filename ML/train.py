import os
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import joblib

def main():
    TRAIN_CSV = os.path.join("data", "train", "train.csv")
    MODEL_DIR = "ML"
    MODEL_PATH = os.path.join(MODEL_DIR, "sgd_logistic.pkl")
    os.makedirs(MODEL_DIR, exist_ok=True)

    le = LabelEncoder().fit(["halt", "nonhalt"])
    clf = SGDClassifier(
        loss="log_loss",
        max_iter=1,
        tol=None,
        learning_rate="optimal",
        random_state=0,
        warm_start=True
    )

    CHUNK_SIZE = 10_000
    TOTAL_ROWS = 120_000_000
    total_chunks = TOTAL_ROWS // CHUNK_SIZE

    first = True
    for chunk in tqdm(
        pd.read_csv(TRAIN_CSV, chunksize=CHUNK_SIZE),
        total=total_chunks,
        unit="chunk",
        desc="Training"
    ):
        X = chunk.drop(columns="status").astype(int).values
        y = le.transform(chunk["status"].values)
        if first:
            clf.partial_fit(X, y, classes=le.transform(["halt", "nonhalt"]))
            first = False
        else:
            clf.partial_fit(X, y)

    joblib.dump({"model": clf, "labels": le}, MODEL_PATH)

if __name__ == "__main__":
    main()