import argparse
import json
from pathlib import Path

import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from src.data.loader import load_train_test
from src.features.vectorizers import make_unigram_vectorizer, make_unigram_bigram_vectorizer


DEFAULT_CONFIG = Path("configs/base.yaml")


def load_config(path: Path) -> dict:
	if path.exists():
		with open(path, "r", encoding="utf-8") as f:
			return yaml.safe_load(f)
	return {}


def main():
	parser = argparse.ArgumentParser(description="Train and eval baseline model")
	parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG))
	parser.add_argument("--features", type=str, default="unigram", choices=["unigram", "unigram_bigram"]) 
	args = parser.parse_args()

	cfg = load_config(Path(args.config))
	vec_cfg = cfg.get("vectorizer", {})
	variant = args.features or vec_cfg.get("variant", "unigram")
	lowercase = bool(vec_cfg.get("lowercase", True))
	stop_words = vec_cfg.get("stop_words", "english")
	min_df = vec_cfg.get("min_df", 2)
	max_features = vec_cfg.get("max_features", None)

	(train_texts, y_train), (test_texts, y_test) = load_train_test()

	if variant == "unigram_bigram":
		vectorizer = make_unigram_bigram_vectorizer(min_occurrences=min_df, max_features=max_features, stop_words=stop_words, lowercase=lowercase)
	else:
		vectorizer = make_unigram_vectorizer(min_occurrences=min_df, max_features=max_features, stop_words=stop_words, lowercase=lowercase)

	X_train = vectorizer.fit_transform(train_texts)
	X_test = vectorizer.transform(test_texts)

	model_cfg = cfg.get("models", {}).get("logistic_l1", {})
	C = float(model_cfg.get("C", [1.0])[0] if isinstance(model_cfg.get("C", 1.0), list) else model_cfg.get("C", 1.0))
	solver = model_cfg.get("solver", "liblinear")
	max_iter = int(model_cfg.get("max_iter", 1000))

	clf = LogisticRegression(penalty="l1", C=C, solver=solver, max_iter=max_iter)
	clf.fit(X_train, y_train)
	y_pred = clf.predict(X_test)

	acc = accuracy_score(y_test, y_pred)
	prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)

	metrics = {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}
	print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
	main()
