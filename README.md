# Bwyd cooking DSL

> "Everything said is said by an observer." –
Maturana and Varela, [_Autopoiesis_](https://www.researchgate.net/publication/232231194_Autopoiesis_40_years_Later_A_Review_and_a_Reformulation)

> "I predict that in the future we will increasingly see cookbooks doing what books do best, tell stories and inspire." –
[Michael Ruhlman](https://ruhlman.substack.com/p/on-cookbooks-and-writing?publication_id=218241&post_id=154625487)


## Abstract

Goal: _Implement a DSL (domain specific language) to simplify means
for defining reliable recipes rapidly, while leveraging computational
tools to catch errors and inconsistencies, scale portions, calculate
yields, and so on._

The "seed crazy idea" behind the scenes here is to consider how cooks
behave somewhat like robots, following recipes as step-by-step
instructions.
Recipes make cooks "programmable" to some extent.

Conversely, what if detailed cooking instructions could be expressed
in a way that was computable and represented independently of specific
human languages?
In other words, representing the processes of cooking as source code
plus semi-structured data?

To this point also consider: where do the stories which inspire and
the associated human domain expertise get attached into the process of
defining robust recipes?


## Motivations

Clearly the bulk of free recipes online (circa 2025) are intended and
structured as click-bait, and a growing protion of that content simply
does not work in a kitchen.
Now the popular services of 
["Today's AI"](https://pangaro.com/designconversation/2021/08/newmacy-in-2021-pandemics-ai/),
which are intended to provide _abstractive summarization_, have begun to show
indications of leveraging that degraded content.

Consequently this project is an application of contemporary software
engineering into the process of how people in professional kitchens
think about their work.
Think of this as a domain specific language for authoring and navigating
cookbooks, customized for use with large language models.

Code in **Bwyd** language represents the "structure" and "art" of cooking,
which can then be parameterized and rendered as text to generate recipes
for a broader audience of home cooks.

A secondary use for **Bwyd** as a DSL is to provide an intermediate
form for leveraging _Generative AI_ to manipulate recipes with the
quality required by use in professional kitchens.


## Language Constructs

### `Ratio`

These represent dimensionless structures, as the ratios (by weight) of key
components in cooking.

A close programming analogy would be _abstract classes_.
Per author Michael Ruhlman, `Ratios` represent
"the _truth_ of cooking, all that is unchanging, fixed, elemental.

Structure defines the "craft" of cooking.
In practice, `Ratio` objects allow for scaling recipes.

### `Closure`

These define process, based on `Ratios`, for how to use ingredients,
equipment, and techniques to make specific products.

A close programming analogy would be _generators_, and internally
these behave similar to Petri nets with pre- and post- conditions.
Recalling "Old School" AI from the 1980s, these function much like
unpopulated frames.

Codifying the practice, `Closure` objects describe steps in cooking,
specifying parameterizations (scale, ingredient substitutions) and
describing yields produced, while consuming recursively from other
`Closure` definitions within a personalized library.

```
  CLOSURE: "cookie dough"

    // commands...

  YIELD (100 g)
```

Process defines the "art" of cooking.
In practice, `Closure` objects allow for team collaboration and
planning within a professional kitchen work environment.

### `Observable`

These represent the experienced end-consumer of a graph of
parameterized `Closure` objects, for a particular event.

A close programming analogy would be _logs_ for one CI pipeline
instance, where ops data gets collected and feedback may be
used to guide subsequent modifications of the `Closure`
definitions which were invoked.

Experience defines the shared  "communication" of cooking.
In practice, `Observable` objects collect audience annotations
(photos, comments, stories, successs/failures) for recipes.
