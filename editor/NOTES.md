
## TODO:

 - renaming in grammar
   + `USE` => `PREP`

 - simplify CSS from Bootstrap examples in use
   + fix the `placeholder`
   + back-out all of the Bootstrap CSS:

container-fluid
row
col-1
col-8
list-group
list-group-item

form-check-input
form-check-label
form-control
form-label

bywd-input
add-item
delete-item
delete-structure
group
caboose

blue-background-class


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
