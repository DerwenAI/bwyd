
## TODO:

 - UI gen misses:
   + `INTERMEDIATE` on YIELDS
   + `PREP filling`

 - simplify CSS from Bootstrap examples in use
   + "trash" shows on add, not at top
   + structured items need a border
   + "url" isn't monospace
   + "add" should not be draggable
   + "textarea" doesn't have vertical resize

 - renaming in grammar
   + `USE` => `PREP`

 - rework TextX grammar to sync with editor UI changes
   + migrate existing Bwyd module examples
   + update Pydantic classes to read parse trees
   + update JSON serialization to sync schema with editor
   + adapt Jinja2 templates to updated JSON
   + round-trip edit/parse/render

 - private GH repo for `bwyd-app`

 - impl FastAPI webapp
   + load Bwyd module examples to confirm roundtrip

 - HTML "i" descriptions for each type, e.g., to distinguish among <select/> options

 - autocomplete symbols for ADD, TRANSFER, ACTION, etc.

 - capture recipe HTML:
   + <https://github.com/alston001/full-capture-extension>

 - color analysis and suggestions
