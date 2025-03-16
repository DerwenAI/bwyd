## Language constructs

> "Everything said is said by an observer." –
Maturana and Varela, [_Autopoiesis_](https://www.researchgate.net/publication/232231194_Autopoiesis_40_years_Later_A_Review_and_a_Reformulation)

> "I predict that in the future we will increasingly see cookbooks doing what books do best, tell stories and inspire." –
[Michael Ruhlman](https://ruhlman.substack.com/p/on-cookbooks-and-writing?publication_id=218241&post_id=154625487)


### `Ratio`

These dimensionless relations represent the ratios (by weight) of key
components in cooking.

A close programming analogy would be _abstract classes_.
Per author Michael Ruhlman, `Ratios` represent
"the _truth_ of cooking, all that is unchanging, fixed, elemental."
Meanwhile the structure in recipes defines the "craft" of cooking.

**In practice**: `Ratio` objects allow for scaling recipes.


### `Closure`

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


### `Observable`

These represent the experienced end-consumer of a graph of
parameterized `Closure` objects, for a particular event.

A close programming analogy would be _logs_ for one CI pipeline
instance, where ops data gets collected and feedback may be
used to guide subsequent modifications of the `Closure`
definitions which were invoked.

Experience defines the shared  "communication" of cooking.

**In practice**: `Observable` objects collect audience annotations
(photos, comments, stories, successs/failures) for recipes.
