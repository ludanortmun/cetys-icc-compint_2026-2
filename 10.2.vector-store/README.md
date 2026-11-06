# 10.2 Build a vector store

Build a small Python library for semantic document retrieval. You may use SentenceTransformers
similarity helpers such as `sentence_transformers.util.cos_sim`; implementing
cosine arithmetic yourself is not required. Implement storage, filtering, and
ranking using your own code and NumPy.

## Setup

Use Python **3.14** and a dedicated environment. From this activity directory:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The package is installed in editable mode. Implement `src/vector_store/store.py`;
keep its public names and signatures. Every student method initially raises
`NotImplementedError`. The supplied encoder protocol, package exports, CLI, and
notebook are demonstration infrastructure and are not scored.

## Contract and student work

Metadata is an optional **set of arbitrary string tags**, not a key/value mapping.
Tags are case-sensitive and compared exactly (including spaces). Do not embed
metadata or preprocess text. Inputs follow the annotated types; type validation
is not required. Return scores without rounding.

| Criterion / test file | Points |
|---|---:|
| `Document.__init__` — `test_document.py` | 15 |
| `VectorStore.__init__` and `add` — `test_add.py` | 25 |
| `VectorStore.search`: cosine, ranking and edge cases — `test_search.py` | 40 |
| `VectorStore.search`: metadata filtering — `test_filter.py` | 20 |
| **Base total** | **100** |
| `VectorStore.save` and `load` together — `test_extra_credit_persistence_extra_credit.py` | **+10** |

1. **Document (15).** `Document(text, metadata=None)` exposes `.text` and
   `.metadata`. Preserve text verbatim; copy tags into a set. Omitted/None tags
   become an independent empty set for each document. No custom equality is needed.
2. **Store and insertion (25).** `VectorStore(model)` starts empty and retains
   the supplied encoder. `add(documents)` appends every document, including
   duplicates, in input order. Call
   `model.encode(texts, convert_to_numpy=True, normalize_embeddings=False)`
   on a list of new document texts; store the resulting NumPy rows aligned with
   their documents. Do not re-encode old documents. Adding `[]` does nothing
   and must not call the encoder. Stores must be independent. Callers will not
   mutate inserted documents. Arrays are finite, two-dimensional, and have a
   consistent positive embedding dimension.
3. **Cosine retrieval (40).** `search(query, k=3, metadata=None)` embeds `[query]`
   using the same encoder arguments and returns a list of `(Document, float)`
   pairs. You may use `from sentence_transformers import util` and
   `util.cos_sim(query_embedding, document_embeddings)` to compare the query
   against stored embeddings. This helper returns a tensor of pairwise scores;
   convert the query row to NumPy for ranking. The similarity is defined as
   `cosine(q, d) = dot(q, d) / (norm(q) * norm(d))`. Define the score as 0 when
   either norm is zero. Return at most `k` entries, sorted by descending full
   precision score; exact ties retain insertion order. Include negative scores.
   An empty store or no eligible documents returns `[]`; `k` larger than the
   candidate count returns all candidates. Integer `k <= 0` raises `ValueError`,
   even for an empty store. Never re-embed stored documents during search.
4. **Metadata filtering (20).** A document qualifies only if it contains **all**
   query tags. Apply filtering before selecting the top `k`. `None` and `set()`
   disable filtering; untagged documents qualify only when no tags are required.
   Do not mutate the supplied filter. For example, filter `{"python", "tutorial"}`
   matches tags `{"python", "tutorial", "beginner"}`, but not `{"python"}`.
5. **Persistence (+10, optional).** Implement `save(path)` and classmethod
   `VectorStore.load(path, model)`. Both require a file path (`str` or `Path`);
   no default path, interactive prompt, or implicit extension. Save document text,
   tags, insertion order, and numerical embeddings; overwrite an existing file.
   Loading returns an independent store and restores embeddings without encoding
   documents. The supplied model must use the same configuration as the original.
   Do not serialize or download model weights. Support empty stores and continued
   insertion/search/save after loading. Missing files raise `FileNotFoundError`.
   Choose your own format; parents already exist. Corrupt-file recovery and model
   compatibility detection are outside scope. The 10 points cover the working
   save/load round trip together.

Internal attribute names and storage format are your choice. You may add private
helpers. Tests use a deterministic encoder with non-unit vectors to check exact
numerical behavior without model downloads. Real model results need not have any
particular score or semantic ordering. Tests cannot establish every implementation
constraint: the teacher also checks storage, filtering, ranking, and embedding
caching by reading the code. Using SentenceTransformers similarity helpers does
not reduce the score.

## Run and validate

From the submissions repository root, run the canonical check:

```bash
sync-assign check 10.2
```

From this activity directory, run the base or complete suite:

```bash
python -m pytest tests --ignore=tests/test_extra_credit_persistence_extra_credit.py
python -m pytest tests
```

The untouched template intentionally fails with `NotImplementedError`. Extra
credit tests also fail until persistence is implemented. Only `Document` and
`VectorStore` are graded. There are no notebook, CLI, or interpretation points.

## Interactive demonstration (supplied, optional)

```bash
python -m jupyterlab
```

Open `notebooks/vector-store.ipynb`, select this environment's kernel, and run all
cells after completing the base library. The notebook uses an in-memory store
and needs no persistence. Its small synthetic English examples are supplied;
no dataset download is required. MiniLM runs on CPU; its initial model download
requires internet, with no API key or paid service. Both demonstrations cache
models under `Path(gettempdir()) / "compint" / "10.2.vector-store"`.

Optional notebook validation and output cleanup:

```bash
python -m pytest --nbmake --nbmake-timeout=600 notebooks/vector-store.ipynb
python -m nbstripout --keep-id notebooks/vector-store.ipynb
```

## CLI demonstration (supplied, requires persistence)

Run these as separate processes from this activity directory after completing
the extra credit. Repeat `--tag` to specify multiple tags. `add` creates a new
file when needed and otherwise appends to the loaded store; `search` requires
an existing file. Both use the same MiniLM model.

```bash
python -m vector_store add --path demo.store --text "Python is a programming language." --tag programming --tag python
python -m vector_store add --path demo.store --text "Cats sleep for many hours." --tag animals
python -m vector_store search --path demo.store --query "learning to code" --k 2
python -m vector_store search --path demo.store --query "learning to code" --tag programming --tag python
```

Submit library source with supplied tests and demonstrations preserved. Do not
commit virtual environments, model caches, store files, or notebook outputs.

## Reference

[SentenceTransformer.encode documentation](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html)
describes embedding generation. The
[similarity utilities](https://www.sbert.net/docs/package_reference/util.html)
include `util.cos_sim`, which you may use for cosine scores. Implement the
remaining retrieval logic yourself.
