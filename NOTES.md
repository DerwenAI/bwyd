## TODOs

  * load graph into `KùzuDB`
  * generate `KùzuDB` embeddings for ingredients, equipment, sequences/communities in actions, etc.
    + https://docs.kuzudb.com/extensions/vector/#create-the-vector-index

  * use `NetworkX` to build a dependency graph of closures from a corpus of modules

  * convert existing recipes

  * better support for search/discovery across a directory of recipes
  * optional load an RDF/SKOS taxonomy
  * validate RDF

  * support MLWeb too?
    + https://github.com/microsoft/NLWeb

  * impl "FERMENT" op
  * support substitutions

  * use `BAML` to parse recipe elements for the DSL

  * allow measure abbrevs: "g" vs "gram", etc.

  * leverage `pydantic-graph` to build trees from directed cliques
  * generate _mermaid diagrams_ for a graph (e.g., in Jupyter)
  * schedule use of appliances: oven, fridge, range, instantpot, etc.
  * PARALLEL/SERIAL for scaling durations

  * use `textX-LS` to generate a VS Code extension
  

## Taxonomy

At the core, the configuration of the **Bwyd** language is based on a
_knowledge graph_.

  - ingredients
  - tools, containers
  - appliances
  - techniques
  - conversions
  - prepped itermediates
  - ratios
  - substitutions
  - keywords
  - author notes to cooks
  - citations
  - posts describing results

See: <https://foodon.org/>


## Research

  * <https://huggingface.co/collections/pacoid/bwyd-66fa446360ff0bbc5deddd59>


---

## Questions

Q: Are there integration paths for working with [Cooklang](https://cooklang.org/)?

This markdown language shares some features with Bwyd.


Q: Can we make use of
[`pydantic-graph`](https://ai.pydantic.dev/graph/)
to represent these intemediate causal graphs as stateful subgraphs?

The underlying graph produces:

  * format recipe for publication
  * scale based on desired `Yields`
  * determine a causal graph to test substitutions as interventions
  * track results of instance (collecting data for CSM, see above)
  * plan with required equipment, ingredients, and timing


Q: Can we link the _verb_ references in `Action` objects to tutorials
via an internal KG?

`mix`, `fold`, `cut`, `spread`, `whisk`, `beat`, `roll`


Q: Can the recent code-completion API in Jupyter notebooks be used
with a **Bwyd** kernel?

  - <https://medium.com/jupyter-blog/jupyterlab-4-1-and-notebook-7-1-are-here-20bfc3c10217>
  - <https://github.com/jupyterlab/jupyter-ai>
  - <https://ipython-books.github.io/16-creating-a-simple-kernel-for-jupyter/>
  - <https://jupyter-client.readthedocs.io/en/stable/wrapperkernels.html>
  - <https://stackoverflow.com/questions/35950433/getting-pygments-to-work-for-my-cell-results>
  - <https://pygments.org/docs/lexerdevelopment/>

Q: Can a saved notebook encapsulate an `Observable` session?

  - use ipywidgets for search, scaling, equipment list, etc., ?
  - https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html

Q: Can `SetFit` and the new `skrub.GapEncoder` be used to parse the
relatively unstructured text from (public domain) online recipes
content?

  - i.e., _transduce_ existing online recipes into a known DSL
  - <https://skrub-data.org/stable/reference/generated/skrub.GapEncoder.html>
  - <https://huggingface.co/docs/setfit/index>

Q: Can we use AI building blocks (e.g., language models, BAML functions,
causal graphs, reinforcement learning, etc.) to restate sequences of `Step`
procedures, i.e., to improve recipes?
