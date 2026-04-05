var BWYD_DEBUG = [];
var CALLBACK_QUEUE = [];
var ELEM_META = {};

const DESIGN_META = [
    {
        "field": {
            "count": "one",
	    "id": "module-title",
	    "label": "Title",
	    "placeholder": "Recipe name",
            "verb": "TITLE",
            "type": "text",
        }
    },
    {
        "field": {
            "count": "one",
	    "id": "module-text",
	    "label": "Text",
	    "placeholder": "Recipe description",
            "verb": "TEXT",
            "type": "text",
	}
    },
    {
        "list": {
            "count": "zero-many",
	    "id": "cite-list",
	    "label": "Sources",
	    "placeholder": "Source link",
            "verb": "CITE",
            "type": "url",
        }
    },
    {
        "list": {
            "count": "zero-many",
	    "id": "post-list",
	    "label": "Gallery",
	    "placeholder": "Gallery link",
            "verb": "POST",
            "type": "url",
        }
    },
    {
        "list": {
            "count": "one-many",
	    "id": "closure-list",
	    "label": "Closures",
            "verb": "CLOSURE",
            "type": [
		{
		    "field": {
			"count": "one",
			"id": "closure-name-%",
			"label": "Name",
			"placeholder": "Closure name",
			"verb": "NAME",
			"type": "text",
		    },
		},
		{
		    "field": {
			"count": "one",
			"id": "closure-text-%",
			"label": "Text",
			"placeholder": "Closure description",
			"verb": "TEXT",
			"type": "text",
		    },
		},
		{
		    "list": {
			"count": "one-many",
			"id": "container-list-%",
			"label": "Containers",
			"verb": "CONTAINER",
			"type": [
			    {
				"field": {
				    "count": "one",
				    "id": "container-name-%",
				    "label": "Name",
				    "placeholder": "Container name",
				    "verb": "NAME",
				    "type": "text",
				},
			    },
			    {
				"field": {
				    "count": "one",
				    "id": "container-text-%",
				    "label": "Text",
				    "placeholder": "Container description",
				    "verb": "TEXT",
				    "type": "text",
				},
			    },
			],
		    },
		},
		{
		    "list": {
			"count": "one-many",
			"id": "tool-list-%",
			"label": "Tools",
			"verb": "TOOL",
			"type": [
			    {
				"field": {
				    "count": "one",
				    "id": "tool-name-%",
				    "label": "Name",
				    "placeholder": "Tool name",
				    "verb": "NAME",
				    "type": "text",
				},
			    },
			    {
				"field": {
				    "count": "one",
				    "id": "tool-text-%",
				    "label": "Text",
				    "placeholder": "Tool description",
				    "verb": "TEXT",
				    "type": "text",
				},
			    },
			],
		    },
		},
		{
		    "list": {
			"count": "one-many",
			"id": "ingredient-list-%",
			"label": "Ingredients",
			"verb": "INGREDIENT",
			"type": [
			    {
				"field": {
				    "count": "one",
				    "id": "ingredient-name-%",
				    "label": "Name",
				    "placeholder": "Ingredient name",
				    "verb": "NAME",
				    "type": "text",
				},
			    },
			    {
				"field": {
				    "count": "one",
				    "id": "ingredient-text-%",
				    "label": "Text",
				    "placeholder": "Ingredient description",
				    "verb": "TEXT",
				    "type": "text",
				},
			    },
			],
		    },
		},
		{
		    "list": {
			"count": "one-many",
			"id": "use-list-%",
			"label": "Uses",
			"verb": "USE",
			"type": [
			    {
				"field": {
				    "count": "one",
				    "id": "use-name-%",
				    "label": "Name",
				    "placeholder": "Use name",
				    "verb": "NAME",
				    "type": "text",
				},
			    },
			    {
				"field": {
				    "count": "one",
				    "id": "use-text-%",
				    "label": "Text",
				    "placeholder": "Use description",
				    "verb": "TEXT",
				    "type": "text",
				},
			    },
			],
		    },
		},
	    ],
        },
    },
]


// append a UUID as a relative component to an ID

function get_rel_id (id) {
    if (id.slice(-1) === "%") {
	return id.replace(/%/g, self.crypto.randomUUID());
    };

    return id;
};


// build UI from the design metadata fragment,
// driven by the context of both input files and user edits

function design_build (design_meta) {
    const frag = document.createDocumentFragment();
    var elem = null;

    for (const [kind, meta] of Object.entries(design_meta)) {
	switch (kind) {
	case "field":
	    const item_id = get_rel_id(meta["id"]);

	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", item_id);
	    elem.appendChild(document.createTextNode(meta["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("input");
	    ELEM_META[item_id] = meta;

	    elem.setAttribute("class", "form-control");
	    elem.setAttribute("id", item_id);
	    elem.setAttribute("type", meta["type"]);
	    elem.setAttribute("placeholder", meta["placeholder"]);
	    frag.appendChild(elem);
	    break;

	case "list":
	    const group_id = get_rel_id(meta["id"]);
	    var callback = `list_add('${group_id}')`;

	    elem = document.createElement("br");
	    frag.appendChild(elem);

	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", group_id);
	    elem.setAttribute("style", "display: inline-block; width: 93%;");
	    elem.appendChild(document.createTextNode(meta["label"]));
	    frag.appendChild(elem);

	    const button = document.createElement("button");
	    button.setAttribute("class", "btn btn-primary btn-sm float-end");
	    button.setAttribute("style", "width: 2.1em;");

	    const icon = document.createElement("i");
	    icon.setAttribute("class", "bi bi-plus");
	    button.appendChild(icon);

	    button.setAttribute("onclick", callback);
	    frag.appendChild(button);

	    elem = document.createElement("div");
	    ELEM_META[group_id] = meta;

	    elem.setAttribute("class", "list-group");
	    elem.setAttribute("id", group_id);

	    new Sortable(elem, {
		animation: 150,
		ghostClass: "blue-background-class",
	    });

	    frag.appendChild(elem);

	    callback = `list_del("${group_id}", 0)`;
	    CALLBACK_QUEUE.push(callback);
	    break;

	default:
	    break;
	};
    };

    return frag;
};


// list handling

function list_add (group_id) {
    const list_group = document.getElementById(group_id);

    // remove any "empty" placeholder element
    if (list_group.children.length == 1) {
	const first_item = list_group.children[0];

	if (first_item.classList.contains("disabled")) {
	    list_group.removeChild(first_item);
	};
    };

    // append another element
    const meta = ELEM_META[group_id];
    var item_id = self.crypto.randomUUID();

    const elem = document.createElement("div");
    elem.setAttribute("class", "row list-group-item");

    var is_structured = false;
    ELEM_META[item_id] = meta;

    if (["text", "url"].includes(meta["type"])) {
	const input = document.createElement("input");
	input.setAttribute("class", "form-control url-field");
	input.setAttribute("id", item_id);
	input.setAttribute("type", meta["type"]);
	input.setAttribute("placeholder", meta["placeholder"]);
	input.setAttribute("required", true);
	input.setAttribute("style", "display: inline-block; width: 93%;");

	// can we use URL pattern validation?
	if (meta["type"] === "url") {
	    // "^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$";
	    // input.setAttribute("pattern", URL_PATTERN);
	};

	elem.appendChild(input);
    }
    else {
	// recursion to handle structured/compound types
	is_structured = true;

	meta["type"].forEach(function(struct_meta) {
	    const item = design_build(struct_meta);
	    elem.appendChild(item);
	});
    };

    const button = document.createElement("button");
    button.setAttribute("class", "btn btn-sm float-end");
    button.setAttribute("style", "width: 2.1em;");

    const icon = document.createElement("i");
    icon.setAttribute("class", "bi bi-x");
    button.appendChild(icon);

    elem.setAttribute("draggable", true);
    elem.appendChild(button);
    list_group.appendChild(elem);

    // for structured types, be sure to use the generated ID
    // NB: must follow `appendChild()` calls above, or IDs won't be in the DOM
    if (is_structured) {
	const selector = `#${group_id} > .list-group-item > input:first-of-type`;
	const first_input = document.querySelector(selector);
	item_id = first_input.id;

	button.classList.add("btn-outline-danger");
	elem.removeChild(button);
	elem.prepend(button);
    }
    else {
	button.classList.add("btn-light");
    };

    const callback = `list_del('${group_id}', '${item_id}')`;
    button.setAttribute("onclick", callback);

    process_callbacks();
    console.log(ELEM_META);
};


function list_del (group_id, item_id) {
    const list_group = document.getElementById(group_id);

    if (list_group.children.length == 0) {
	const elem = document.createElement("a");
	elem.setAttribute("class", "list-group-item disabled");
	elem.setAttribute("href", "#");

	const empty = document.createElement("em");
	empty.appendChild(document.createTextNode("(empty)"));

	elem.appendChild(empty);
	list_group.appendChild(elem);
    }
    else if (item_id != 0){
	const item = document.getElementById(item_id);
	item.parentNode.remove();
	list_del(group_id, 0);
    };
};


// encode the current editor content into the DSL language

function encode_statement (elem, code, line, script) {
    const num_lines = code.split(/\r\n|\r|\n/).length;
    var elem_id = null;

    if (elem != null) {
	elem_id = elem.id;
    };

    // track DOM element vs. Bwyd script line number, for debug
    const debug = {
	elem_id: elem_id,
	code: code,
	min_line: line,
	max_line: line + num_lines - 1,
    };

    console.log(debug);
    BWYD_DEBUG.push(debug);

    script.push(code);

    return line + num_lines;
};


function encode_dependency (elem, kind, line, script) {
    const selector = `#${elem.id} > .list-group-item`;
    const item_list = document.querySelectorAll(selector);
    const verb = ELEM_META[elem.id].verb;

    for (var k = 0; k < item_list.length; k++) {
	const item = item_list[k];
	var first_input = null;
	var text = "";

	for (var l = 0; l < item.children.length; l++) {
	    const input = item.children[l];

	    if (input.nodeName === "INPUT") {
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		};
	    };
	};

	var code = `${verb} ${first_input.value.trim()}:`;

	if (text.length > 0) {
	    code = `${code} "${text}"`;
	};

	line = encode_statement(first_input, code, line, script);
    };

    return line;
};


function encode_list (selector, line, script) {
    const input_list = document.querySelectorAll(selector);

    for (var i = 0; i < input_list.length; i++) {
	const elem = input_list[i];
	const verb = ELEM_META[elem.id].verb;
	const code = `${verb}: "${elem.value.trim()}"`;

	line = encode_statement(elem, code, line, script);
    };

    return line;
};


function encode_module () {
    const script = [];
    var line = 1;
    var code = null;
    BWYD_DEBUG = [];

    // encode top-level inputs for the module
    var selector = "#editor-inputs > input";
    line = encode_list(selector, line, script);

    selector = "#cite-list > .list-group-item > input";
    line = encode_list(selector, line, script);

    selector = "#post-list > .list-group-item > input";
    line = encode_list(selector, line, script);

    // encode the CLOSURE list, each of which have compound elements
    const closure_list = document.getElementById("closure-list").children;

    for (var i = 0; i < closure_list.length; i++) {
	const closure = closure_list[i];
	console.log("clos", closure);

	for (var j = 0; j < closure.children.length; j++) {
	    var elem = closure.children[j];

	    if (elem.nodeName === "INPUT") {
		if (elem.id.startsWith("closure-name")) {
		    code = `CLOSURE: "${elem.value.trim()}"`;
		    line = encode_statement(elem, code, line, script);
		}
		else if (elem.id.startsWith("closure-text")) {
		    code = `TEXT: "${elem.value.trim()}"`;
		    line = encode_statement(elem, code, line, script);
		};
	    }
	    else if (elem.nodeName === "DIV") {
		if (elem.id.startsWith("container-list")) {
		    line = encode_dependency(elem, "container", line, script);
		}
		else if (elem.id.startsWith("tool-list")) {
		    line = encode_dependency(elem, "tool", line, script);
		}
		else if (elem.id.startsWith("ingredient-list")) {
		    line = encode_dependency(elem, "ingredient", line, script);
		}
		else if (elem.id.startsWith("use-list")) {
		    line = encode_dependency(elem, "use", line, script);
		};
	    };
	};

	// add a trailing separator
	line = encode_statement(null, ";", line, script);
    };

    // debug: update the <textarea/> script display
    document.getElementById("bwyd-script").value = script.join("\n");

    // TODO: roundtrip with server for parsing and validation
};



// use callbacks to clean-up after creating DOM elements

function process_callbacks () {
    while (CALLBACK_QUEUE.length > 0) {
	const callback = CALLBACK_QUEUE.pop();
	eval(callback);
    };
};


// run after the page loads

window.addEventListener("load", function() {
    // build the default editor
    for (var i = 0; i < DESIGN_META.length; i++) {
	document.getElementById("editor-inputs").appendChild(
	    design_build(DESIGN_META[i])
	);
    };

    process_callbacks();
});
