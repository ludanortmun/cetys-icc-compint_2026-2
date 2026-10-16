# 9.2 Topic modeling: discover and interpret themes

Use Latent Dirichlet Allocation (LDA) to explore themes in a text collection.
The focus is **interpreting evidence**, not implementing an algorithm. Work in
one notebook, `notebooks/topics.ipynb`, with two parts:

1. **Reference example:** complete, runnable code using 64 supplied synthetic
   news headlines. Read its explanations and discuss the reference reflection question.
2. **Your dataset:** find a different text dataset, reuse the reference code,
   and answer Q2–Q5. Answer Q1 in the reference part as well. Any language or
   subject is welcome.

## Setup

Use **Python 3.14** and an environment exclusive to this activity. From
`9.2.topics`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate with `.venv\Scripts\activate`. Choose this environment's
kernel. All reference data and dependencies are provided; the reference needs
no download. See `data/README.md` for its synthetic-data provenance.

## Part 1 — Read and run the reference

Run the first part from top to bottom. It explicitly creates document–term
**counts**, fits scikit-learn's `LatentDirichletAllocation`, and directly displays
the raw array returned by `fit_transform`. It explains the document rows and
topic columns, inspects individual document mixtures, normalizes `components_`
to rank words per topic, and selects representative documents by sorting columns
of the document-topic array. Only after these steps does it introduce reusable
helpers. It repeats the model with a different topic count and supports a
qualitative comparison. Answer Reflection Q1 (10 points) by proposing topic
names using the displayed words and documents. The supplied reference code
is not scored.

The supplied `analyze_topics` and `show_topics` helpers are complete and reusable.
No library implementation, custom algorithm, or additional Python package is
required. LDA takes counts here, not TF-IDF. A topic's high-weight words are model
estimates, not simply its most frequent words. A document can mix multiple topics;
its largest topic weight is only a convenient summary. Topic IDs have no fixed
meaning and do not correspond between different model runs.

## Part 2 — Choose data and interpret it

Add your own code and markdown cells after each prompt. Preserve all supplied
cells, IDs, and assertions. You may copy and adapt the reference code directly.

- **Choose, load, and document your corpus — code: 10 points.** Find a dataset other than the supplied
  reference data. Explain its source, language, document unit, selection, size,
  preprocessing, and your exploration question. A document might be an article,
  summary, review, or discussion post. Prefer varied, substantive texts; very
  short headlines can provide little word co-occurrence evidence. Around
  100–1,000 documents is a useful starting point, not a graded minimum. If you
  sample a larger dataset, describe the selection and keep it reproducible.
- **Make the analysis reproducible.** Store a small redistributable input in
  `data/`, or provide an accessible download link and exact loading/preparation
  instructions. Include the exact analyzed subset when permitted. Exclude raw
  data from Git if it is large; do not submit credentials or installed packages.
  Keep loading paths relative to the activity. Explain how the teacher can
  obtain the same documents without a private account. Convert your texts to a
  list of nonempty strings called `student_documents`.
- **Run LDA — code: 25 points.** Choose at least two topics and save `student_results` using
  `analyze_topics(student_documents, n_topics=..., stop_words=...)`. The default
  English stopword list is only suitable for English; use your own list or
  `None` for another language and explain the choice. Display results with
  `show_topics(student_results, student_documents)`. You may adapt the helper,
  preserving its result keys. Inspect full documents when printed excerpts are
  insufficient. Record the settings you used.
- **Compare one other topic count — code: 15 points.** On the same documents with the same
  preprocessing and random seed, create `alternative_results` with a different
  topic count and display it. There is no need for a parameter search or a
  numerical claim about the best count.
- **Answer Q2–Q5** in new markdown cells, as well as Q1 in Part 1. Each
  question is worth 10 points. Name the reference and student-corpus topics,
  describe your dataset, compare the two student analyses, and draw conclusions.
  Spanish or English is acceptable. Mixed or unclear topics are valid findings
  when explained thoughtfully.

## Reflection questions — 10 points each

1. **Reference topics (Part 1):** Based on the top words and documents for each
   topic, which name would you assign to each topic?
2. **Dataset and purpose (Part 2):** Where did the texts come from, what does each
   document represent, and what did you hope to discover? Why is this collection
   suitable? Describe selection, language, preprocessing, size, and access for
   reproduction.
3. **Your topics (Part 2):** What name would you give each topic in your primary
   model?
4. **Alternate topic count (Part 2):** What changed? Which result is more useful
   for your exploration question, and why?
5. **Conclusions (Part 2):** What did you learn about this corpus? How might
   preprocessing, document length, dataset selection, and the model's word-count
   representation affect your conclusions? Distinguish observations supported
   by these texts from claims about the wider world.

## Scoring — 50 points for code and 50 for questions

| Criterion | Points |
|---|---:|
| Load the student corpus reproducibly as `student_documents` | 10 |
| First analysis: LDA, topic words, representative documents, and a document's topic mixture | 25 |
| Alternate topic count on the same corpus, with displayed results | 15 |
| **Code subtotal** | **50** |
| Q1 — name the reference topics | 10 |
| Q2 — describe the chosen dataset and purpose | 10 |
| Q3 — name the student-corpus topics | 10 |
| Q4 — compare the topic counts and explain usefulness | 10 |
| Q5 — conclusions and limitations | 10 |
| **Questions subtotal** | **50** |
| **Total** | **100** |

All points are assigned manually by the teacher. Notebook assertions only check
that your documents, model results, topic mixtures, and summaries were created;
passing them does **not** determine your grade. Answers and modeling choices are
reviewed manually. No expected topics, exact model parameters, implementation
style, or model-quality thresholds are tested. No accuracy, coherence,
perplexity, train/test split, or LSI comparison is required for this exploration.

## Run, validate, and submit

Run Part 1 on its own to inspect the reference. After completing Part 2, restart
the kernel and run the entire notebook. From the activity directory:

```bash
python -m pytest --nbmake notebooks/topics.ipynb
python -m nbstripout --keep-id notebooks/topics.ipynb
python -m nbstripout --verify --keep-id notebooks/topics.ipynb
```

From the submissions repository root:

```bash
sync-assign check 9.2
```

The untouched template runs through Part 1 and stops at the first Part 2
completion check until you add your own work. There is no separate pytest suite.
Submit your completed notebook with outputs cleared, preserving code, reflection
markdown, and source/access instructions. The teacher reruns it to view results.
Preserve the reference data and supplied cells. Do not submit your virtual
environment or installed dependencies. Follow course Jupyter conventions;
failure to follow them halves the total score.

## References

- [LatentDirichletAllocation — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html)
- [Topic extraction example — scikit-learn](https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html)
- Teaching sequence inspired by the instructor's master's notebook,
  [Modelado de tópicos: LSI/LDA](https://github.com/ludanortmun/tareas-nlp-aj-2024-ludanortmun/blob/main/Equipo33_semanas6y7.ipynb).
  This activity uses only LDA and qualitative interpretation.
