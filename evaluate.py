import pandas as pd
from collections import Counter

def load_labels(path="eval_labels.csv"):
    return pd.read_csv(path)

def load_hits(path="eval_hits.csv"):
    return pd.read_csv(path)

def compute_metrics(labels_df, hits_df):
    """
    Compute precision, recall, accuracy per PII type.
    Matching is done on exact (pii_type, original) pairs.
    """
    # Convert to sets of tuples for easy comparison
    label_pairs = set(zip(labels_df["pii_type"], labels_df["original"]))
    hit_pairs = set(zip(hits_df["pii_type"], hits_df["original"]))

    # True positives: correctly detected labeled items
    tp_pairs = label_pairs & hit_pairs

    # False positives: detected but not labeled as PII
    fp_pairs = hit_pairs - label_pairs

    # False negatives: labeled but not detected
    fn_pairs = label_pairs - hit_pairs

    # Break down counts per type
    tp_counts = Counter(p[0] for p in tp_pairs)
    fp_counts = Counter(p[0] for p in fp_pairs)
    fn_counts = Counter(p[0] for p in fn_pairs)

    all_types = sorted(set(labels_df["pii_type"]) | set(hits_df["pii_type"]))
    results = []

    for t in all_types:
        tp = tp_counts[t]
        fp = fp_counts[t]
        fn = fn_counts[t]
        # Accuracy here defined per type over labeled+detected for that type
        total = tp + fp + fn
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        accuracy = tp / total if total > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        results.append({
            "pii_type": t,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "accuracy": round(accuracy, 3),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
        })

    return pd.DataFrame(results)

def main():
    labels_df = load_labels("eval_labels.csv")
    hits_df = load_hits("eval_hits.csv")

    metrics_df = compute_metrics(labels_df, hits_df)
    print(metrics_df.to_string(index=False))

    # Optionally save to CSV for your report
    metrics_df.to_csv("evaluation_results.csv", index=False)

if __name__ == "__main__":
    main()