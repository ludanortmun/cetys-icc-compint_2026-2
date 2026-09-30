# 7.1 Vectorization

## Introduction

Turn preprocessed reviews into numeric vectors by implementing three small classes in a notebook: `Vocabulary` (20 points), `BagOfWordsVectorizer` (30 points), and `TFIDFVectorizer` (50 points). 

The supplied spaCy pipeline and review loader are complete and outside the scope of the activity. The pipeline uses spaCy's English tokenizer, keeps alphabetic tokens, and lowercases them. It preserves stopwords and does not lemmatize; no language-model download is needed. Its output is `list[str]`, not a custom token class.

This activity introduces the [Stanford Large Movie Review Dataset](https://ai.stanford.edu/~amaas/data/sentiment/) (Maas et al., 2011). Both vectorizers learn from a balanced subset of 5,000 training reviews and demonstrate their representations on a review from that same subset. Sentiment labels are used only to balance the sample, not as vector features.

## Setup

Use Python 3.11 or 3.12. From this activity directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Open `notebooks/vectorization.ipynb` using the environment's Python kernel. All implementation belongs in new code cells immediately after the three marked instruction cells. Keep supplied cells intact. There is no `src/` package or separate Python implementation to edit.

### Download the movie reviews manually

1. Open the dataset page linked above and download `aclImdb_v1.tar.gz`.
2. Extract the archive into this activity's `data/` directory, preserving its `aclImdb/` folder.
3. Check that files exist under `data/aclImdb/train/pos/` and `data/aclImdb/train/neg/`. This activity uses only the training set.

Use the raw `.txt` reviews only. The download and extracted data are ignored by Git and should not be submitted. Download before class: the notebook initializes the dataset at the start, before any implementation. The class assertions use a tiny built-in corpus, while each supplied demonstration uses the downloaded reviews.

The supplied loader sorts training `.txt` paths by filename, samples 2,500 from `pos` and then 2,500 from `neg` using one local `random.Random(42)` instance, and shuffles the combined paths with that same instance. This fixes both membership and document order for reproducible vocabulary indexes and weights. The demonstrations use the first review in this sampled corpus. The pipeline removes HTML tags, then tokenizes and lowercases alphabetic tokens. Vectorization preserves the learned vocabulary and IDF. To keep memory use small, the demonstration creates only individual dense vectors, not a dense matrix for all 5,000 documents.

## Student instructions

### Vocabulary — 20 points

Create `Vocabulary()` with these methods:

- `add(token: str) -> int`: assign a new token the next consecutive index starting at zero, in first-appearance order. Return the existing index for duplicates.
- `token_to_idx(token: str) -> int | None`: return its index, or `None` when absent, without adding anything.
- `idx_to_token(index: int) -> str`: return the token, raising `IndexError` for a negative or out-of-range index.
- `__len__() -> int`: return the number of distinct tokens.

Use strings and ordinary Python containers. This object is the only source of truth for vector positions; neither vectorizer should maintain a separate token-to-index mapping.

### BagOfWordsVectorizer — 30 points

Create `BagOfWordsVectorizer()` with an initially empty `.vocabulary` (a `Vocabulary` instance) and these methods:

- `learn_corpus(corpus: list[list[str]]) -> None`: build its vocabulary by visiting documents and their tokens in order.
- `vectorize(document: list[str]) -> list[int]`: return token counts in vocabulary order.

For both vectorizers, each `learn_corpus` call replaces all learned state. `vectorize` ignores unknown tokens without changing the vocabulary or learned statistics. An empty document produces a zero vector with one entry per vocabulary term. Before learning, and whenever the learned vocabulary is empty, `vectorize` returns `[]`.

Bag of Words values are raw counts; do not normalize them.

### TFIDFVectorizer — 50 points

Create `TFIDFVectorizer()` with an initially empty `.vocabulary` (a `Vocabulary` instance) and these methods:

- `learn_corpus(corpus: list[list[str]]) -> None`: build its vocabulary and IDF statistics by visiting documents and their tokens in order.
- `vectorize(document: list[str]) -> list[float]`: return TF-IDF weights in vocabulary order.

Use exactly:

```text
TF(token, document) = token count / total number of document tokens
DF(token) = number of corpus documents containing the token
IDF(token) = math.log(N / DF(token))
TFIDF(token, document) = TF(token, document) * IDF(token)
```

`N` includes empty documents. Each document contributes at most one to a token's DF. The TF denominator includes all supplied tokens, including unknown ones. Use natural logarithms, no smoothing, and no additional vector normalization. A term present in all corpus documents has zero weight.

### Run each demonstration

Initialize the dataset once at the start. Then work in this order: implement Vocabulary, run its review demonstration and assertions; implement BagOfWordsVectorizer, run its review demonstration and assertions; implement TFIDFVectorizer, run its review demonstration and assertions. No changes to preprocessing, data loading, or the demonstrations are required.

## Run and validate

Restart the kernel and run all cells from top to bottom. Assertion cells test only the three scored classes, including repeated terms, unknown tokens, empty inputs, and relearning. Until you add your implementations, the starter notebook intentionally fails at the first missing class.

From this activity directory, with the environment activated:

```bash
pytest --nbmake notebooks
nbstripout notebooks/vectorization.ipynb
nbstripout --verify --keep-id notebooks/vectorization.ipynb
```

From the assignments repository root, canonical validation is:

```bash
sync-assign check 7.1
```

## Scoring

| Component | Points |
|---|---:|
| Vocabulary: stable indexes, insertion and both lookups | 20 |
| BagOfWordsVectorizer: corpus learning and count vectors | 30 |
| TFIDFVectorizer: corpus learning and TF-IDF vectors | 50 |
| **Total** | **100** |

Each criterion requires all of its notebook assertions to pass. Submit the notebook with your new implementation cells and cleared outputs. Do not modify the pipeline or supplied checks.
