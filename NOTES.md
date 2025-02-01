## Taxonomy

At the core, the configuration of the **Bwyd** language is based on a
_knowledge graph_.

  - ratio
  - ingredient
  - technique
  - tool

within Closure implies "ADD TO FOCUS MENTIONED MOST RECENTLY"

within Closure implies "USE TOOL MENTIONED MOST RECENTLY"

Then a language model can render text for a parameterized recipe.


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


---

## Example

### 1. CLOSURE: prepare dough

NOTE: best to work with cold ingredients and chilled utensils

RATIO: dough

FOCUS (CONTAINER: chilled mixing bowl)

ADD (INGREDIENT: 1 large chicken egg)

ACTION: using (TOOL: small whisk or a fork)
	(UNTIL: egg is beaten lightly)
	(TIME: 30 sec)

ADD (INGREDIENT: 250 ml whole milk ricotta), (INGREDIENT: 50 g grated parmesan), (INGREDIENT: 1 g freshly grated nutmeg)

STIR using (TOOL: spatula)
	(UNTIL: well mixed)
	(TIME: 30 sec)

ADD (INGREDIENT: 1 cup reduced veggie purée)

FOLD
	(UNTIL: lightly mixed)
	(TIME: 30 sec)

ADD (INGREDIENT: 240 g flour - rice, oat, etc.)
    (UNTIL: dough is no longer sticky)
    (TIME: 60 sec))

MIX
	(UNTIL: dough just becomes smooth)
	(TIME: 30 sec)


### 2. CLOSURE: cut dumplings

NOTE: divide dough into 8 pieces, rolling out one at a time

FOCUS (CONTAINER: rolling surface)

SPREAD (INGREDIENT: 10 g flour - rice, semolina)
	(TIME: 30 sec)

ADD (DEPEND: .125 dough)

ROLL by hand
	carefully
	(RESULT: 2 cm diameter "rope")
	(TIME: 60 sec)

CUT using (TOOL: fork)
	(RESULT: 1 cm dumplings pieces, which resemble little pillows)
	(TIME: 30 sec)


### 3. CLOSURE frozen dumplings

NOTE: add layers of dumplings to fill depth of baking dish

FOCUS (CONTAINER: baking dish)

LINE with (INGREDIENT: cut parchment paper)
	(TIME: 30 sec)

ROLL (DEPEND: cut dumplings) using (TOOL: fork or gnocchi grater)
ARRANGE on parchment paper, without touching other dumplings
	(TIME: 10 sec)

FREEZE
	(RESULT: solid dumplings)
	(TIME: 2 hrs)


### 4. STORE gnocchi

FOCUS (CONTAINER: freezer bag)

TRANSFER (DEPEND: frozen dumplings) from parchment paper
	(TIME: 5 min)

(STORE: in freezer until ready to cook)

(YIELDS: 6 servings)
(SOURCE: https://derwen.ai/r/gnocchi)
