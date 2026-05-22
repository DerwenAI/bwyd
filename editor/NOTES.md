
## TODO:

 - load from JSON document
   - YIELD
   - STORE
   - NOTE / comments

 - encodings for: RATIO, YIELD, STORE, NOTE


 - simplify CSS from Bootstrap examples in use
   + refactor dynamic style into `dsl.css`
   + make the UI/UX more compact, especially for lists

 - rework TextX grammar to sync with editor UI changes
   + migrate existing Bwyd module examples
   + update Pydantic classes to read parse trees
   + update JSON serialization to sync schema with editor
   + adapt Jinja2 templates to updated JSON
   + round-trip edit/parse/render

 - private GH repo for `bwyd-app`

 - descriptions for each type, e.g., to distinguish among <select/> options

 - impl FastAPI webapp
   + load Bwyd module examples to confirm roundtrip

 - autocomplete symbols for ADD, TRANSFER, ACTION, etc.

 - color analysis
