# Bwyd cooking DSL

Have you ever considered, "How does language generate food?"

While not quite that, language does convey passion, desire, learnings
-- all of which translate into preparing food to be shared lovingly.


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
["Today's AI"](https://pangaro.com/designconversation/2021/08/newmacy-in-2021-pandemics-ai/)
-- which are intended to provide _abstractive summarization_ --
are beginning to show indications of republishing that degraded content.
A positive feedback loop follows, and it won't be pretty.

Consequently this project is an application of contemporary software
engineering -- particularly drawn from _functional programming_ --
into the process of how people in professional kitchens think about
their work.
Think of this project as a domain specific language for authoring and
navigating cookbooks, customized for use with language models, causal
graphs, neurosymbolic reasoning, and other building blocks for AI
applications.

Code in **Bwyd** language represents the "structure" and "art" of cooking,
which can then be parameterized and rendered as text to generate recipes
for a broader audience of home cooks.

A secondary use for **Bwyd** as a DSL is to provide an intermediate
form for leveraging _generative_ approaches to manipulate recipes
while ensuring the quality required by use in professional kitchens.


## Documentation

  * how to install: [INSTALL.md](https://github.com/DerwenAI/bwyd/blob/main/docs/INSTALL.md)
  * project notes: [NOTES.md](https://github.com/DerwenAI/bwyd/blob/main/NOTES.md)
