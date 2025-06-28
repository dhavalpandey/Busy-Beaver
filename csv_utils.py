import csv

def print_head(path, n=5):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            print(row)
            if i >= n - 1:
                break

if __name__ == "__main__":
    print_head("data/train/train.csv", 5)