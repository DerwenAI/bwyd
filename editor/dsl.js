const BWYD_DEBUG = [];
const CALLBACK_QUEUE = [];

const ELEM_META = {};

const DESIGN_META = [
    {
        "field": {
            "grammar": "TITLE",
            "type": "text",
            "count": "one",
	    "label": "Title",
	    "id": "module-title",
	    "placeholder": "My Recipe",
        }
    },
    {
        "field": {
            "grammar": "TEXT",
            "type": "text",
            "count": "one",
	    "label": "Text",
	    "id": "module-text",
	    "placeholder": "Text Description",
	}
    },
    {
        "list": {
            "grammar": "CITE",
            "type": "url",
            "count": "zero-many",
	    "label": "Sources",
	    "id": "cite-list",
	    "placeholder": "Source URL",
        }
    },
    {
        "list": {
            "grammar": "POST",
            "type": "url",
            "count": "zero-many",
	    "label": "Gallery",
	    "id": "post-list",
	    "placeholder": "Gallery URL",
        }
    },
]


function build_frag (frag, design) {
    var elem = null;

    for (const [kind, meta] of Object.entries(design)) {
	switch (kind) {
	case "field":
	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", meta["id"]);
	    elem.appendChild(document.createTextNode(meta["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("input");
	    ELEM_META[meta["id"]] = meta;

	    elem.setAttribute("class", "form-control");
	    elem.setAttribute("id", meta["id"]);
	    elem.setAttribute("type", meta["type"]);
	    elem.setAttribute("placeholder", meta["placeholder"]);
	    frag.appendChild(elem);
	    break;

	case "list":
	    const group_id = meta["id"];
	    var callback = `list_add('${group_id}')`;

	    elem = document.createElement("br");
	    frag.appendChild(elem);

	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", group_id);
	    elem.appendChild(document.createTextNode(meta["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("a");
	    elem.setAttribute("class", "btn btn-primary btn-sm float-end");
	    elem.setAttribute("href", "#");
	    elem.setAttribute("role", "button");
	    elem.appendChild(document.createTextNode("+"));

	    elem.setAttribute("onclick", callback);
	    frag.appendChild(elem);

	    elem = document.createElement("div");
	    ELEM_META[group_id] = meta;

	    elem.setAttribute("class", "list-group");
	    elem.setAttribute("id", group_id);

	    new Sortable(elem, {
		animation: 150,
		ghostClass: "blue-background-class",
	    });

	    frag.appendChild(elem);

	    callback = `list_del('${group_id}', 0)`;
	    CALLBACK_QUEUE.push(callback);
	    break;

	default:
	    break;
	};
    };

    return frag;
};


// list add/delete handling

function list_add (group_id) {
    const list_group = document.getElementById(group_id);

    // remove any "empty" placeholder element
    if (list_group.children.length == 1) {
	var first = list_group.children[0];

	if (first.classList.contains("disabled")) {
	    list_group.removeChild(first);
	};
    };

    // append another element
    const meta = ELEM_META[group_id];
    const item_id = self.crypto.randomUUID();

    var elem = document.createElement("div");
    elem.setAttribute("class", "row list-group-item");
    elem.setAttribute("draggable", true);

    var input = document.createElement("input");
    ELEM_META[item_id] = meta;

    input.setAttribute("class", "form-control url-field");
    input.setAttribute("id", item_id);
    input.setAttribute("type", meta["type"]);
    input.setAttribute("placeholder", meta["placeholder"]);
    input.setAttribute("required", true);
    input.setAttribute("style", "display: inline-block; width: 93%;");

    if (meta["type"] === "url") {
	// const URL_PATTERN = new RegExp('(?:http[s]?:\\\/\\\/.)?(?:www\\.)?[-a-zA-Z0-9@%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b(?:[-a-zA-Z0-9@:%_\\+.~#?&\\\/\\\/=]*)', 'gm')
	// "^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$";
	// input.setAttribute("pattern", URL_PATTERN);
    };

    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-light btn-sm float-end");
    button.setAttribute("style", "width: 2.1em;");

    var icon = document.createElement("i");
    icon.setAttribute("class", "bi bi-x");
    button.appendChild(icon);

    var callback = `list_del('${group_id}', '${item_id}')`;
    button.setAttribute("onclick", callback);

    elem.appendChild(input);
    elem.appendChild(button);

    list_group.appendChild(elem);
};


function list_del (group_id, item_id) {
    const list_group = document.getElementById(group_id);

    if (list_group.children.length == 0) {
	var elem = document.createElement("a");
	elem.setAttribute("class", "list-group-item disabled");
	elem.setAttribute("href", "#");

	var empty = document.createElement("em");
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

function encode_statement (elem, code, line) {
    const num_lines = code.split(/\r\n|\r|\n/).length;

    // track HTML element vs. Bwyd script line number, for debugging
    var debug = {
	elem_id: elem.id,
	code: code,
	min_line: line,
	max_line: line + num_lines - 1,
    };

    console.log(debug);
    BWYD_DEBUG.push(debug);

    return line + num_lines;
};


function encode_dom () {
    var script = [];
    var line = 1;

    // top-level inputs for the module
    var input_list = document.querySelectorAll("#editor-inputs > input");

    for (var i = 0; i < input_list.length; i++) {
	var elem = input_list[i];
	var verb = ELEM_META[elem.id].grammar;
	var code = `${verb} ${elem.value};`;
	line = encode_statement(elem, code, line);
	script.push(code);
    };

    // encode the CITE list
    input_list = document.querySelectorAll("#cite-list > .list-group-item > input");

    for (var i = 0; i < input_list.length; i++) {
	var elem = input_list[i];
	var verb = ELEM_META["cite-list"].grammar;
	var code = `${verb} ${elem.value};`;
	line = encode_statement(elem, code, line);
	script.push(code);
    };

    // encode the POST list
    input_list = document.querySelectorAll("#post-list > .list-group-item > input");

    for (var i = 0; i < input_list.length; i++) {
	var elem = input_list[i];
	var verb = ELEM_META["post-list"].grammar;
	var code = `${verb} ${elem.value};`;
	line = encode_statement(elem, code, line);
	script.push(code);
    };

    // update the <textarea/> display
    document.getElementById("bwyd-script").value = script.join("\n");
};


// run after the page loads

window.addEventListener("load", function() {
    // build the default editor
    for (var i = 0; i < DESIGN_META.length; i++) {
	document.getElementById("editor-inputs").appendChild(
	    build_frag(
		document.createDocumentFragment(),
		DESIGN_META[i],
	    )
	);
    };

    // clean-up at end
    while (CALLBACK_QUEUE.length > 0) {
	const callback = CALLBACK_QUEUE.pop();
	eval(callback);
    };
});
