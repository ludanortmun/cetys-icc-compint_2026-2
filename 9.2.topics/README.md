# 9.2 Topic modeling: discover and interpret themes

Use Latent Dirichlet Allocation (LDA) to explore themes in a text collection.
The focus is **interpreting evidence**, not implementing an algorithm. Work in
one notebook, `notebooks/topics.ipynb`, with two parts:

1. **Reference example:** complete, runnable code using 64 supplied synthetic
   news headlines. Read its explanations and worked interpretation.
2. **Your dataset:** find a different text dataset, reuse the reference code,
   and answer the five reflection questions. Any language or subject is welcome.

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

Run the first part from top to bottom. It loads headlines, creates document–term
**counts**, fits scikit-learn's `LatentDirichletAllocation`, displays eight
high-weight words and three representative documents per topic, and examines
a document's topic mixture. It repeats the model with a different topic count
and demonstrates a qualitative comparison.

The supplied `analyze_topics` and `show_topics` helpers are complete and reusable.
No library implementation, custom algorithm, or additional Python package is
required. LDA takes counts here, not TF-IDF. A topic's high-weight words are model
estimates, not simply its most frequent words. A document can mix multiple topics;
its largest topic weight is only a convenient summary. Topic IDs have no fixed
meaning and do not correspond between different model runs.

## Part 2 — Choose data and interpret it

Add your own code and markdown cells after each prompt. Preserve all supplied
cells, IDs, and assertions. You may copy and adapt the reference code directly.

- **Choose and document your corpus.** Find a dataset other than the supplied
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
- **Run LDA.** Choose at least two topics and save `student_results` using
  `analyze_topics(student_documents, n_topics=..., stop_words=...)`. The default
  English stopword list is only suitable for English; use your own list or
  `None` for another language and explain the choice. Display results with
  `show_topics(student_results, student_documents)`. You may adapt the helper,
  preserving its result keys. Inspect full documents when printed excerpts are
  insufficient. Record the settings you used.
- **Compare one other topic count.** On the same documents with the same
  preprocessing and random seed, create `alternative_results` with a different
  topic count and display it. There is no need for a parameter search or a
  numerical claim about the best count.
- **Answer all five reflection questions** in new markdown cells. Name every
  topic in your primary model, support each name with terms and at least two
  documents, discuss an ambiguous case and its topic weights, compare the two
  runs by their content, and conclude with limitations. Spanish or English is
  acceptable. Evidence matters more than response length; mixed or unclear
  topics are valid findings when discussed thoughtfully.

## Reflection questions

1. **Dataset and purpose:** Where did the texts come from, what does each
   document represent, and what did you hope to discover? Describe selection,
   language, preprocessing, size, and access for reproduction.
2. **Topic interpretation:** What name would you give each primary-model topic?
   Support every name with high-weight terms and at least two document IDs or
   excerpts. Explain contradictions instead of hiding them.
3. **Ambiguity:** Which topic is hardest to interpret? Discuss a document whose
   topic mixture is ambiguous or surprising. Cite its topic weights and explain
   whether its content supports that mixture.
4. **Effect of topic count:** What changed with the second count? Identify
   themes that split, merge, persist, or become harder to interpret, with terms
   and documents from both runs. Compare content rather than matching topic IDs.
   Which representation is more useful for your exploration question, and why?
5. **Conclusions and limitations:** What did you learn about this corpus? Explain
   how preprocessing, document length, dataset selection, and the model's
   word-count representation might limit your conclusions.

## Scoring — teacher review

| Criterion | Points |
|---|---:|
| Dataset source, description, suitability, and reproducibility (Q1) | 15 |
| Completed analysis: primary and alternative models, readable terms, documents, and topic mixtures | 15 |
| Topic names supported by terms and documents (Q2) | 35 |
| Ambiguity and comparison of topic counts (Q3–Q4) | 20 |
| Conclusions and limitations (Q5) | 15 |
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
