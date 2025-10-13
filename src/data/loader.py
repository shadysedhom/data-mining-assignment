import os
from pathlib import Path
from typing import List, Tuple

DATA_ROOT = Path("Data")

# Candidate source directories (some may not exist on disk)
SOURCE_DIRS = [
	DATA_ROOT / "positive_polarity" / "deceptive_from_MTurk",
	DATA_ROOT / "positive_polarity" / "truthful_from_TripAdvisor",
	DATA_ROOT / "negative_polarity" / "deceptive_from_MTurk",
	DATA_ROOT / "negative_polarity" / "truthful_from_TripAdvisor",
]


def read_fold_texts(fold_dir: Path) -> Tuple[List[str], List[int], List[str]]:
	texts: List[str] = []
	labels: List[int] = []  # 1 = deceptive (fake), 0 = truthful (genuine)
	paths: List[str] = []
	is_deceptive = "deceptive_from_MTurk" in str(fold_dir)
	label_value = 1 if is_deceptive else 0
	for txt_path in sorted(fold_dir.glob("*.txt")):
		with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
			texts.append(f.read())
		labels.append(label_value)
		paths.append(str(txt_path))
	return texts, labels, paths


def load_folds(folds: List[int]) -> Tuple[List[str], List[int], List[str]]:
	all_texts: List[str] = []
	all_labels: List[int] = []
	all_paths: List[str] = []
	for base in SOURCE_DIRS:
		if not base.exists():
			continue
		for fold in folds:
			fold_dir = base / f"fold{fold}"
			if not fold_dir.exists():
				continue
			texts, labels, paths = read_fold_texts(fold_dir)
			all_texts.extend(texts)
			all_labels.extend(labels)
			all_paths.extend(paths)
	return all_texts, all_labels, all_paths


def load_train_test() -> Tuple[Tuple[List[str], List[int]], Tuple[List[str], List[int]]]:
	"""Return (train_texts, train_labels), (test_texts, test_labels) using folds 1–4 for train and 5 for test."""
	train_texts, train_labels, _ = load_folds([1, 2, 3, 4])
	test_texts, test_labels, _ = load_folds([5])
	return (train_texts, train_labels), (test_texts, test_labels)
