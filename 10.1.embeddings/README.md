# 10.1 Semantic meaning with embeddings

Explore how pretrained embeddings capture semantic relationships. Retrieve word
vectors using GloVe and Word2Vec, encode complete short documents with Sentence
Transformers, compare cosine similarities, and interpret supplied PCA and
clustering visualizations. Work in `notebooks/embeddings.ipynb`.

## Setup

Use Python **3.14** in this activity's own virtual environment. From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

**Compatibility limitation:** Gensim 4.4.0 currently fails to compile on this Mac
with Python 3.14 (its generated C references removed CPython internals).
Python 3.14 remains the course target; local execution was verified with
Python 3.13 as a compatibility fallback using the same requirements.

On Windows, activate `.venv\Scripts\activate`. Select the environment's kernel.
The first notebook cell configures all model downloads under
`Path(gettempdir()) / "compint" / "10.1.embeddings"`; do not substitute a fixed
machine-specific path. Gensim is configured before its downloader is imported;
SentenceTransformer receives an explicit cache folder. Restart the kernel if
these libraries were already imported. Temporary caches can be cleared by the
operating system. Internet is required on the first run, with no paid API or
private account. Later runs reuse cached models.

Google News Word2Vec-300 downloads about **1.74 GB compressed** and requires
several GB of RAM; GloVe-100 downloads about **134 MB compressed**. Finish each
word model's operations, retain only the requested small arrays/results, delete
the model, and call `gc.collect()` before loading the next. SentenceTransformer
runs on CPU. Never commit downloaded models, caches, or your environment.

## Student instructions

Add new code and markdown cells after the prompts, before their assertions.
Preserve all supplied cells and IDs. The supplied 24 synthetic English documents
are local inputs, with provenance in `data/README.md`; preserve their order and
IDs. No separate corpus is required.

1. **Word embeddings (30 code points).** Load both pretrained models sequentially.
   Loading, dimensions, a complete labeled vector, and selected vectors are worth
   10 points; the four word comparisons and five neighbors of `student` are worth
   10; the two analogies with five candidates each are worth 10. Create
   `word_vectors`, `word_scores`, `word_neighbors`, and `word_analogies` with the
   keys described in the notebook. Use its case-sensitive model tokens. Evaluate
   `king - man + woman` and `Paris - France + Japan`, not `king + woman` alone.
2. **Word PCA.** Run the supplied helper separately for each word model and interpret
   the plots. Its implementation is provided and unscored.
3. **Document embeddings (10 code points).** Use
   `sentence-transformers/all-MiniLM-L6-v2` with the specified cache folder and CPU.
   Create `document_embeddings`; display shape and a complete row with its text.
   Keep natural text rather than applying count-vectorization preprocessing.
4. **Document cosine similarity (10 code points).** Use
   `from sentence_transformers import util` and `util.cos_sim` on the original
   embeddings. Save `document_similarities` and its CPU NumPy `similarity_array`.
   Display the labeled matrix and four specified pairs. Create
   `nearest_document_ids` containing three row indices nearest row 0, excluding
   itself, sorted by unrounded scores (stable input order for ties). Display
   their IDs, texts, and scores.
5. **Document PCA.** Run the supplied plot and compare it with original-space scores.
6. **Clustering experiments.** Call the supplied `compare_clusters` helper in your
   own cell with at least three distinct integer `k` values, from 2 to 23.
   `(2, 4, 6)` is a suggested starting point. Keep the corpus and PCA coordinates
   fixed. Compare all KMeans results with MeanShift, which estimates bandwidth
   when none is specified rather than accepting a requested cluster count.
   Optionally explore a positive explicit bandwidth. The helper displays cluster
   counts, sizes, complete memberships, and plots on shared axes. No clustering
   or plotting implementation is required or scored.

## Interpretation and scoring

Answer every question in a new markdown cell immediately after its section.
Spanish or English is acceptable. Cite observed words, scores, document IDs,
and memberships; expectations alone are insufficient.

| Criterion | Points |
|---|---:|
| Word loading and vector inspection | 10 |
| Word similarities and neighbors | 10 |
| Word analogies | 10 |
| Document embeddings and inspection | 10 |
| Document cosine matrix, comparisons, and retrieval | 10 |
| **Code subtotal** | **50** |
| Q1 — semantic evidence, dimensions, analogies, and static-vector limitations | 10 |
| Q2 — word plots and projection limitations | 5 |
| Q3 — document representation, context, and input limits | 10 |
| Q4 — document similarities, paraphrases, ambiguity, and negation | 10 |
| Q5 — document plot versus original similarities | 5 |
| Q6 — different k values, MeanShift comparison, evidence, and limitations | 10 |
| **Interpretation subtotal** | **50** |
| **Total** | **100** |

For Q6, comparing KMeans splits/merges is worth 3 points; explaining MeanShift's
cluster count and bandwidth is worth 3; naming groups with membership evidence
is worth 2; judging usefulness and limitations is worth 2. Compare the actual
results without assuming that cluster IDs/colors correspond across runs.

All points are assigned manually. Assertions verify required objects and basic
numerical properties; passing does not determine the grade. No exact nearest
word, analogy rank, semantic score, cluster count, or membership is required.
Unexpected similarities, mixed groups, and a single MeanShift cluster are valid
observations when explained using evidence. No training, custom corpus, numerical
clustering metrics, parameter search, or algorithm implementation is required.

Embedding coordinates are learned features, not named vocabulary columns.
Different models' vector spaces cannot be compared coordinate by coordinate.
Analogies are approximate and can reflect training-data biases. Cosine similarity
is not a probability or proof of agreement. The document model produces 384
features and truncates beyond 256 wordpieces by default. PCA discards information;
all clustering here is deliberately illustrative and uses the 2D coordinates.
MeanShift does not require k, but is not parameter-free.

## Run, validate, and submit

After completing the notebook, restart its kernel and run every cell. From the
activity directory:

```bash
python -m pytest --nbmake --nbmake-timeout=3600 notebooks/embeddings.ipynb
python -m nbstripout --keep-id notebooks/embeddings.ipynb
python -m nbstripout --verify --keep-id notebooks/embeddings.ipynb
```

Allow time for the initial downloads. From the submissions repository root:

```bash
sync-assign check 10.1
```

The untouched template stops at its first student completion assertion. There
is no separate Python test suite because student work stays in notebook cells.
Submit with outputs cleared and all code and interpretation answers preserved.
The teacher reruns it for review. Follow course Jupyter conventions; failure to
follow them halves the total score, consistent with activity 9.2.

## References

- [Gensim pretrained model catalog](https://github.com/piskvorky/gensim-data/blob/master/list.json)
- [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [SentenceTransformers similarity utilities](https://sbert.net/docs/package_reference/util.html)
- [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), and [MeanShift](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MeanShift.html)
