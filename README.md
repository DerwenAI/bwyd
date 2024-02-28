# Bwyd cooking DSL

> "Everything said is said by an observer." – Maturana and Varela, _Autopoiesis_


## Abstract

Goal: _Implement a DSL to simplify means for defining good recipes rapidly,
while using computational tools to catch errors and inconsistencies, scale
portions, calculate yields, and so on._

The seed crazy idea behind the scenes here is to consider how human cooks
behave somewhat like robots, following recipes as instructions.
Recipes make cooks "programmable" to some extent.

Conversely, what if detailed cooking instructions could be expressed in a way
that was computable and represented independently of specific human languages?
In other words, representing the processes of cooking as source code plus
semi-structured data?

This project is an application of contemporary software engineering to how
people in professional kitchens think about their work.

Code in **Bwyd** language represents the "structure" and "art" of cooking,
which can then be parameterized and rendered as text to generate recipes
for a broader audience of home cooks.

A secondary use for **Bwyd** as a DSL is to provide an intermediate for
leveraging _Generative AI_ to manipulate recipes at the quality required
by use in professional kitchens.
