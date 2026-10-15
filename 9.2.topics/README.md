# 9.2 Topics from news headlines

Discover groups of related headlines without topic labels, then interpret and
name the groups yourself. Use the course stack: Python, Jupyter, NumPy, and
scikit-learn. Allow about 45–60 minutes. The supplied dataset contains 64 original,
synthetic English news-style headlines, including a few mixed-subject examples;
it is intentionally small and simplified. See `data/README.md` for provenance.

## Setup

Use **Python 3.14** and a virtual environment exclusive to this activity.
From `9.2.topics`, run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate with `.venv\Scripts\activate`. Choose this environment's
kernel and open `notebooks/topics.ipynb`. The CSV is included; no download needed.
Add your own code cells after each prompt and before its assertions. Preserve
all supplied cells, IDs, assertions, and the order of headlines.

## Required work — 100 points

1. **Vectorize (20).** Create `vectorizer = CountVectorizer(stop_words="english")`
   and fit it on `headlines`, saving its count matrix as `counts`. Save
   `terms = vectorizer.get_feature_names_out()`. Create `tfidf = TfidfTransformer()`
   and save `X = tfidf.fit_transform(counts)`. Use TF-IDF for clustering and raw
   counts for the most common words. Keep other vectorizer settings at defaults.
2. **Cluster (30).** Create `kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)`
   and save `kmeans_labels = kmeans.fit_predict(X)`. Create
   `meanshift = MeanShift(bandwidth=bandwidth)` using a positive `bandwidth` of
   your choice (start at `1.1`); save `meanshift_labels` from `fit_predict(X.toarray())`.
   MeanShift needs a dense array here; conversion is only practical because this
   dataset is tiny. Save both label arrays in `labels_by_method`, with keys
   `"kmeans"` and `"meanshift"`. Print the number of groups and size of each group
   for each method. K-means takes the desired number of clusters; MeanShift
   discovers a number that depends on bandwidth and the data. Any number of
   MeanShift groups, including one, is acceptable. Do not substitute KNN.
3. **Describe groups (25).** Create `cluster_summaries`, a dictionary keyed by
   method name and then integer cluster ID. For every group, store a dictionary
   with `size` (number of headlines), `top_words` (the five most frequent words,
   or all words if fewer than five), and `examples` (the first three original
   headlines in that group, or all if smaller). Sum `counts` over the group's
   rows, discard zero counts, and sort by descending frequency; break ties
   alphabetically. Print each group's ID, size, top words, and examples.
   Do not call TF-IDF weights word frequencies.
4. **Interpret (25).** Create `topic_names`, keyed by method name and then integer
   cluster ID, with your own short topic name for every group. Use `"mixed"` or
   `"unclear"` when appropriate. Create `reflection`, a paragraph of at least
   80 words comparing the two results: support proposed names with words and
   sample headlines, identify at least one ambiguous or mixed headline, and
   explain the effect of choosing a number of clusters versus a bandwidth.
   Print the names and reflection. Spanish or English is acceptable. Names and
   reasoning are reviewed manually; there is no single correct topic list.
   Interpretation points: complete names (5), evidence from words and headlines
   (10), an ambiguous headline (5), and comparison of cluster count versus
   bandwidth (5).

This is qualitative exploration of the supplied corpus: use all 64 headlines.
No train/test split, accuracy, silhouette score, external labels, parameter
search, or minimum clustering quality is required. A mixed group is a finding
to discuss. Execution assertions check implementation, not the quality of topics.

## Run and validate

Run the complete notebook from top to bottom. Its printed summaries are the
example output to inspect; there is no separate application.
From the activity directory:

```bash
python -m pytest --nbmake notebooks/topics.ipynb
python -m nbstripout --keep-id notebooks/topics.ipynb
python -m nbstripout --verify --keep-id notebooks/topics.ipynb
```

From your submissions repository root, canonical validation is:

```bash
sync-assign check 9.2
```

The starter intentionally fails until you add your implementation cells.
There is no Python library or separate pytest suite; each scored section has
notebook assertions. Interpretation assertions check completeness only; the
teacher reviews the actual names and explanation.

## Submission and scoring

| Component | Points |
|---|---:|
| Counts and TF-IDF vectors | 20 |
| K-means and MeanShift, group counts and sizes | 30 |
| Common words and sample headlines for every group | 25 |
| Manual topic names and evidence-based comparison | 25 |
| **Total** | **100** |

Submit the completed notebook with outputs cleared, keeping your code cells,
topic names, and reflection in the notebook. Preserve the dataset and teacher
assertions. Do not submit the virtual environment or installed dependencies.
Follow course Jupyter conventions; failure to follow them halves the total score.

## References

- [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [MeanShift](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MeanShift.html)
- [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)
