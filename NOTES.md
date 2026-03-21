## TODOs

  * convert existing recipes
    + cooked_beans => bean_sauce

  * generate layers:
    - RDF semantics
    - network diagram for Activities

  * refactor YIELD(+STORE) into ACTIVITY
    + ADD/TRANSFER as initial operation
    + bookend with EMPTY and CLEAN events for each Container/Tool

  * integrate _material procurement_ schedules, material lead times, and inventory as task constraints in planning

  * support substitutions/pivots

  * allow measure abbrevs: "g" vs "gram", etc.

  * PARALLEL/SERIAL for scaling durations

  * better support for search/discovery across a directory of recipes

  * support NLWeb too?
    + https://github.com/microsoft/NLWeb

  * use `textX-LS` to generate a VS Code extension?
    + https://github.com/textX/textX-LS  


## Modeling

Module (a named recipe)
 - 1+ Closures (functional, multi-use components)
   - 0+ Supers
   - 0+ Keywords
   - 1+ Activities (milestones)
     - bookend EMPTY/CLEAN events for each Container/Tool
     - 0+ Appliances
     - 0+ Containers
     - 0+ Tools
     - 1+ Inputs (e.g., Ingredients, or Yields from other Closures)
     - 1+ Operations
     - 1+ Yields
       - 0+ Storage

Equipment Inventory
  - Appliances
  - Containers
  - Tools

Ingredient Procurement
  - Supplier
    - Costs
  - Ingredients
    - Conversions
    - Substitutions
Permits


Parse a module to build Pydantic objects:
  - Error handling:
    - debug during edit
    - validate parse
  - Simulation:
    - model semantics in RDF graph (down to Closures, Keywords, Yields)
      - validate generated RDF with SHACL
    - Gantt analysis of Activities, to identify critical paths
      - generate a PERT chart as a network diagram
      - schedule as a Petri net: Appliances/Containers/Tools through Operations
      - plot timelines for Execution
    - Analyze seasonality vs. substitutions (supply network)
    - Validate reachabilitiy
    - Calculate aggregate measures
      - totals for each Ingredient (BOM)
      - total cost, based on inventory vs. suppliers
      - total Execution time
      - inventory for Appliances, Containers, Tools (resource planning)
      - complexity measure as Pareto front: Ingredient count, Operation count

  - Serialize as JSON
    - Jinja2 render to HTML for discovery and execution
    - DSPy integration here?

  - Visualize interactive Graph for edit
  - edit an Execution Plan
  - edit Suppliers network
    + Kanban analysis of Ingredients inventory
  - edit Appliances/Containers/Tools inventory
  

  * define an RDF/SKOS taxonomy
    + optional load additional RDF ?

  * Petri nets
    + schedule use of appliances: oven, fridge, range, instantpot, etc.
    + https://bpogroup.github.io/simpn/

  * use `NetworkX` to build a dependency graph of closures from a corpus of modules
    + include RDF triples
    + optimize for total time, minimal downtime of appliances, etc.
    + leverage `pydantic-graph` to build trees from directed cliques
    + generate _mermaid diagrams_ for a graph (e.g., in Jupyter)
    + load embeddings into `LanceDB`

  * use `DSPy` to parse recipe elements for the DSL
    + https://victorjlamas.github.io/assets/papers/LLMXpertMODELS2024.pdf
    + https://medium.com/itemis/large-language-models-for-domain-specific-language-generation-part-2-how-to-constrain-your-dragon-e0e2439b6a53


## Taxonomy

At the core, the configuration of the **Bwyd** language is based on a
_knowledge graph_.

  - modules (recipes)
  - citations
  - posts describing results
  - closures (components with multiple uses)
  - supers
  - keywords
  - tools, containers
  - appliances
  - ingredients
  - author notes to cooks
  - techniques
  - conversions
  - ratios
  - prepped itermediates
  - substitutions

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

Q: How can we use AI building blocks (e.g., language models, DSPy
declarative LLM integration, causal graphs, reinforcement learning,
etc.) to restate sequences of `Step` procedures, i.e., to improve
recipes?
