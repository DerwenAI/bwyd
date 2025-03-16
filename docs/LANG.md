# Language constructs

> "Everything said is said by an observer." –
Maturana and Varela, [_Autopoiesis_](https://www.researchgate.net/publication/232231194_Autopoiesis_40_years_Later_A_Review_and_a_Reformulation)

> "I predict that in the future we will increasingly see cookbooks doing what books do best, tell stories and inspire." –
[Michael Ruhlman](https://ruhlman.substack.com/p/on-cookbooks-and-writing?publication_id=218241&post_id=154625487)


## `Ratio`

These dimensionless relations represent the ratios (by weight) of key
components in cooking.

A close programming analogy would be _abstract classes_.
Per author Michael Ruhlman, `Ratios` represent
"the _truth_ of cooking, all that is unchanging, fixed, elemental."
Meanwhile the structure in recipes defines the "craft" of cooking.

**In practice**: `Ratio` objects allow for scaling recipes.


## `Closure`

These define process, based on `Ratios`, for how to use ingredients,
equipment, and techniques to make specific products.

A close programming analogy would be _generators_, and internally
these behave similar to Petri nets with _guard expressions_ as pre-
and post- conditions.
Recalling "Old School" AI from the 1980s, these function much like
unpopulated frames in _frame representation_.

Codifying the practice, `Closure` objects describe sequences of
`Steps` used in cooking.
These specify parameterizations (scale, ingredient substitutions) and
describing the `Yields` produced, while consuming recursively from
other `Closure` definitions drawn from a personalized library.

```
  CLOSURE: "cookie dough"

    // steps ...

  YIELDS (100 g)
```

Process defines the "art" of cooking.

**In practice**: `Closure` objects allow for team collaboration and
planning within a professional kitchen work environment.


## `Observable`

These represent the experienced end-consumer of a graph of
parameterized `Closure` objects, for a particular event.

A close programming analogy would be _logs_ for one CI pipeline
instance, where ops data gets collected and feedback may be
used to guide subsequent modifications of the `Closure`
definitions which were invoked.

Experience defines the shared  "communication" of cooking.

**In practice**: `Observable` objects collect audience annotations
(photos, comments, stories, successs/failures) for recipes.


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
