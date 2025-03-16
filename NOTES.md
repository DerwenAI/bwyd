## TODOs

  * refactor the `NOTE` objects to be Op -- or `HEADER` ?
  * scan a module to produce a total ingredients list
  * express conversions as function of densities
  * add a Corpus class to handle collections of parsed modules
  * use `NetworkX` to build a dependency graph of closures from a corpus of modules
  * leverage `pydantic-graph` to build trees from directed cliques
  * generate _mermaid diagrams_ for a graph (e.g., in Jupyter)
  * incorporate `Bootstrap` layouts
  

## Taxonomy

At the core, the configuration of the **Bwyd** language is based on a
_knowledge graph_.

  - ratios
  - ingredients
  - techniques
  - tools


## Research

  * <https://huggingface.co/collections/pacoid/bwyd-66fa446360ff0bbc5deddd59>


---

## Ideation

Other language constructs to be added are `Substitutions` and `Pairings`,
per Niki Segnit, [_The Flavor Thesaurus_](https://www.nikisegnit.com/the-flavour-thesaurus)
and the concepts of _lateral cooking_ which she's explored.

Each `Closure` of a recipe is by definition a 
[_causal graph_](https://medium.com/@gxyang13/close-back-door-for-causal-models-a-guide-to-causal-graph-d4483cd5a276),
where:

  * `Yields` represent intermediate _outcomes_
  * substitutions/pivots correspond to _interventions_


Each `Step` within a `Closure` specifies its required ingredients in
specific ratios and the tools which must be available, applying
well-defined techniques, until some measurable state is reached.

Consequently this formulation structures each `Step` as a
[Petri net](https://en.wikipedia.org/wiki/Petri_net)
composed of _places_, _transitions_, and _arcs_, where:

  * ingredients getting transformed into `Yields` correspond to _tokens_
  * measurable states correspond to _guard expressions_


References to other elements within a `Closure` imply:

  * "ADD TO FOCUS MENTIONED MOST RECENTLY"
  * "USE TOOL MENTIONED MOST RECENTLY"

As a consequence, a language model could render text from any
parameterized recipe.


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
