"""
Stream raw BB5 CSV → numeric train/test CSVs.

Usage:
  python create_data.py \
    --input data/raw/BB5_verified_enumeration.csv \
    --train data/train/train.csv \
    --test  data/test/test.csv \
    --split 0.8
"""

import csv, os, sys, random, argparse
from time import time
from ML.turing_machine import Machine

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input",  required=True, help="raw BB5 CSV")
    p.add_argument("--train",  required=True, help="output train CSV")
    p.add_argument("--test",   required=True, help="output test CSV")
    p.add_argument("--split",  type=float, default=0.8,
                   help="fraction for training set")
    p.add_argument("--seed",   type=int,   default=42,
                   help="random seed for reproducibility")
    args = p.parse_args()

    random.seed(args.seed)
    # ensure output dirs exist
    os.makedirs(os.path.dirname(args.train), exist_ok=True)
    os.makedirs(os.path.dirname(args.test),  exist_ok=True)

    # open files
    rf = open(args.input, newline='')
    tf = open(args.train, "w", newline='')
    vf = open(args.test,  "w", newline='')
    rdr = csv.reader(rf)
    wtr = csv.writer(tf)
    wvr = csv.writer(vf)

    header = [f"f{i}" for i in range(30)] + ["status"]
    wtr.writerow(header)
    wvr.writerow(header)

    next(rdr) 

    count = 0
    t0 = time()
    for row in rdr:
        code, status, *_ = row
        if status not in ("halt","nonhalt"):
            continue
        feats = Machine(code).parse()
        out = feats + [status]
        if random.random() < args.split:
            wtr.writerow(out)
        else:
            wvr.writerow(out)

        count += 1
        if count % 1_000_000 == 0:
            elapsed = time() - t0
            rate = count / elapsed
            sys.stdout.write(f"\rProcessed {count:,} rows ({rate:,.0f}/s) ")
            sys.stdout.flush()

    sys.stdout.write(f"\nDone. Total rows: {count:,}\n")
    rf.close(); tf.close(); vf.close()

if __name__ == "__main__":
    main()