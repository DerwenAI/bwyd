# Bwyd programming language

## Abstract

Goal: make it simpler to define good recipes rapidly while using computed tools to catch errors and inconsistencies

Premise: what if the human cook behaved like a robot, following recipe instructions?

What if cooking instructions could be expressed in a way that was computable, and independent of specific human languages? In other words, as software.

This is an application of contemporary software engineering to how people in professional kitchens think about their work. Programs written in the **Bwyd** language represent the "structure" and "art" of cooking, which can then be parameterized and rendered as text to generate "recipes" for a broader audience of home cooks.


## Taxonomy

At the core, the configuration of the **Bwyd** language is based on a _knowledge graph_.

  - ratio
  - ingredient
  - technique
  - tool


## Constructs

  - craft: **Ratio** (dimensionless, abstract types, unpopulated frames): the _truth_ of cooking, all that is unchanging, fixed, elemental

  - art: **Closure** (process, based on Ratios, one step in cooking, with yields; generators): specifying the substitutions (parameterizations), and behaving like one step in a Petri net with pre/post conditions

  - experience: **Observable** (end consumer of a chain of parameterized Closure objects) describes on instance and its observed experiences

within Closure implies "ADD TO FOCUS MENTIONED MOST RECENTLY"

within Closure implies "USE TOOL MENTIONED MOST RECENTLY"

> "Everything said is said by an observer." – Maturana and Varela, _Autopoiesis_


Then a LLM renders the text for a parameterized recipe.

Observable objects annotate (photos, notes) one experienced instance for a recipe.


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