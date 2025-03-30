## TODOs

  * scan a module to produce a total ingredients list
  * define SLUG symbol
  * licenses: https://spdx.org/licenses/CC-BY-NC-ND-4.0.html
  * align BS style colors with Derwen palette
  * express conversions as function of densities
  * PARALLEL/SERIAL for scaling durations
  * override graph for densities, etc.
  * schedule use of appliances: oven, fridge, range, instantpot, etc.
  * add a Corpus class to handle collections of parsed modules
  * use `NetworkX` to build a dependency graph of closures from a corpus of modules
  * leverage `pydantic-graph` to build trees from directed cliques
  * generate _mermaid diagrams_ for a graph (e.g., in Jupyter)
  * embeddings based on ingredients, form

  
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


## Research

  * <https://huggingface.co/collections/pacoid/bwyd-66fa446360ff0bbc5deddd59>


---

## Questions

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

Q: Can we use AI building blocks (e.g., language models, causal
graphs, reinforcement learning, etc.) to restate sequences of `Step`
procedures, i.e., to improve recipes?
