var BWYD_DEBUG = [];
var CALLBACK_QUEUE = [];
var ELEM_META = {};

// append a UUID as a relative component to an ID

function get_rel_id (id) {
    if (id.slice(-1) === "%") {
	return id.replace(/%/g, self.crypto.randomUUID());
    };

    return id;
};


// build UI from the design metadata fragment,
// driven by the context of both input files and user edits

function design_build (design_meta, depth) {
    const frag = document.createDocumentFragment();

    for (const [kind, meta] of Object.entries(design_meta)) {
	switch (kind) {
	case "field":
	    var item_id = get_rel_id(meta["id"]);
	    var elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", item_id);
	    elem.appendChild(document.createTextNode(meta["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("textarea");
	    ELEM_META[item_id] = meta;

	    elem.setAttribute("class", "form-control");
	    elem.setAttribute("id", item_id);
	    elem.setAttribute("type", meta["type"]);
	    elem.setAttribute("placeholder", meta["placeholder"]);
	    frag.appendChild(elem);
	    break;

	case "list":
	    var group_id = get_rel_id(meta["id"]);
	    var color = Math.round((1.0 - (depth * .03)) * 100.0);

	    console.log(depth, color);

	    var row = document.createElement("div");
	    row.setAttribute("class", "row");
	    row.setAttribute("style", `min-height: 8rem; width: 100%; margin-top: 2rem; margin-left: -2rem; background: hsl(0 0 ${color});`);
	    frag.appendChild(row);

	    var col = document.createElement("div");
	    col.setAttribute("class", "col-1");
	    col.setAttribute("style", "padding: 0;");
	    row.appendChild(col);

	    var elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", group_id);
	    elem.setAttribute("style", "margin-top: 1rem; rotate: 270deg; color: hsl(0, 0%, 75%); font-weight: bold; padding-left: 0;");
	    elem.appendChild(document.createTextNode(meta["label"]));
	    col.appendChild(elem);

	    col = document.createElement("div");
	    col.setAttribute("class", "col-8");
	    row.appendChild(col);

	    var list_group = document.createElement("div");
	    ELEM_META[group_id] = meta;

	    list_group.setAttribute("class", "list-group");
	    list_group.setAttribute("id", group_id);
	    col.appendChild(list_group);

	    new Sortable(list_group, {
		animation: 150,
		ghostClass: "blue-background-class",
	    });

	    // add a "caboose" button
	    elem = document.createElement("div");
	    elem.setAttribute("id", get_rel_id("caboose-%"));
	    elem.setAttribute("class", "list-group-item");

	    var button = document.createElement("button");
	    button.setAttribute("class", "btn btn-outline-primary btn-sm");
	    button.setAttribute("style", "width: 2.1em; display: inline;");

	    var callback = `list_add('${group_id}', ${depth})`;
	    button.setAttribute("onclick", callback);

	    var icon = document.createElement("i");
	    icon.setAttribute("class", "bi bi-plus");
	    button.appendChild(icon);
	    elem.appendChild(button);

	    var para = document.createElement("span");
	    var text = `add new ${meta["label"].toLowerCase()}`;
	    para.appendChild(document.createTextNode(text));
	    para.setAttribute("style", "font-size: .75em; font-style: oblique; color: #aaa; margin-left: 1em;");

	    elem.appendChild(para);
	    list_group.appendChild(elem);
	    break;

	case "select":
	    var item_id = get_rel_id(meta["id"]);

	    if ("label" in meta) {
		var label = document.createElement("span");
		label.appendChild(document.createTextNode(meta["label"]));
		frag.appendChild(label);
	    };

	    var select = document.createElement("select");
	    select.setAttribute("class", "form-control");
	    select.setAttribute("id", item_id);
	    select.setAttribute("style", "display: inline-block; width: 93%;");

	    var option = document.createElement("option");
	    option.setAttribute("disabled", true);
	    option.setAttribute("selected", true);
	    option.setAttribute("value", null);

	    var para = document.createElement("span");
	    para.setAttribute("style", "font-style: oblique; color: #aaa;");
	    para.appendChild(document.createTextNode("(select an option)"));
	    option.appendChild(para);
	    select.appendChild(option);

	    for (const [key, value] of Object.entries(meta["type"])) {
		option = document.createElement("option");
		option.setAttribute("value", key);
		option.appendChild(document.createTextNode(key));
		select.appendChild(option);
	    };

	    // TODO: needs callback to reconfigure structure
	    var callback = `menu_select('${item_id}', ${depth})`;
	    select.setAttribute("onchange", callback);

	    ELEM_META[item_id] = meta;
	    frag.appendChild(select);
	    break;

	default:
	    console.log("UNKNOWN DESIGN:", kind, meta);
	    break
	};
    };

    return frag;
};


// menu handling

function menu_select (menu_id, depth) {
    const menu = document.getElementById(menu_id);
    const meta = ELEM_META[menu_id].type[menu.value];
    const item = menu.parentElement;
    const prev_elems = [];

    if (meta.length > 0) {
	// collect and remove all pre-existing structured elements:
	// everthing which follows the <select/> and delete <button/>
	for (var i = 2; i < item.childNodes.length; i++) {
	    prev_elems.push(item.childNodes[i]);
	};

	for (var i = 0; i < prev_elems.length; i++) {
	    item.removeChild(prev_elems[i]);
	}

	// add the new structured elements
	meta.forEach(function(struct_meta) {
	    const elem = design_build(struct_meta, depth + 1);
	    item.appendChild(elem);
	});
    };
}


// list handling

function list_add (group_id, depth) {
    const list_group = document.getElementById(group_id);

    // build a new item to insert
    const meta = ELEM_META[group_id];
    var item_id = self.crypto.randomUUID();

    const elem = document.createElement("div");
    elem.setAttribute("class", "row list-group-item");

    var is_structured = false;
    ELEM_META[item_id] = meta;

    if (["text", "url"].includes(meta["type"])) {
	const input = document.createElement("textarea");
	input.setAttribute("class", "form-control url-field");
	input.setAttribute("id", item_id);
	input.setAttribute("type", meta["type"]);
	input.setAttribute("placeholder", meta["placeholder"]);
	input.setAttribute("required", true);
	input.setAttribute("style", "display: inline-block; width: 87%;");

	// can we use URL pattern validation?
	if (meta["type"] === "url") {
	    // "^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$";
	    // input.setAttribute("pattern", URL_PATTERN);
	};

	elem.appendChild(input);
    }
    else {
	// recursion handles structured/compound types
	is_structured = true;

	meta["type"].forEach(function(struct_meta) {
	    const item = design_build(struct_meta, depth + 1);
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

    // insert item just before the "caboose" at the end
    list_group.insertBefore(elem, list_group.lastElementChild);

    // reset the focus to the newly built element
    const built_elem = list_group.lastChild.previousElementSibling;

    built_elem.focus({
	focusVisible: true,
	preventScroll: false,
    });

    built_elem.scrollIntoView();

    // for structured types, be sure to use the generated ID from
    // the first child which has class "form-control"
    // NB: must follow `insertBefore` above, or IDs won't be in the DOM
    if (is_structured) {
	for (var i = 0; i < built_elem.children.length; i++) {
	    if (built_elem.children[i].classList.contains("form-control")) {
		item_id = built_elem.children[i].id;
		break;
	    }
	};

	button.classList.add("btn-outline-danger");

	built_elem.removeChild(button);
	built_elem.prepend(button);
    }
    else {
	button.classList.add("btn-light");
    };

    // set up the delete button
    const callback = `list_del('${group_id}', '${item_id}')`;
    button.setAttribute("onclick", callback);
};


function list_del (group_id, item_id) {
    const list_group = document.getElementById(group_id);

    if (item_id != null) {
	const item = document.getElementById(item_id);
	item.parentNode.remove();
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

	    if (!input.id.startsWith("caboose-") && (input.nodeName === "TEXTAREA")) {
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		};
	    };
	};

	if (first_input != null) {
	    var code = `${verb} ${first_input.value.trim()}:`;

	    if (text.length > 0) {
		code = `${code} "${text}"`;
	    };

	    line = encode_statement(first_input, code, line, script);
	};
    };

    return line;
};


function encode_list (selector, line, script) {
    const input_list = document.querySelectorAll(selector);

    for (var i = 0; i < input_list.length; i++) {
	const elem = input_list[i];

	if (!elem.id.startsWith("caboose-")) {
	    const verb = ELEM_META[elem.id].verb;
	    const code = `${verb}: "${elem.value.trim()}"`;

	    line = encode_statement(elem, code, line, script);
	};
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

	if (!closure.id.startsWith("caboose-")) {
	    for (var j = 0; j < closure.children.length; j++) {
		var elem = closure.children[j];

		if (elem.nodeName === "TEXTAREA") {
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
    const item = document.getElementById("editor-inputs");

    DESIGN_META.forEach(function(struct_meta) {
	const elem = design_build(struct_meta, 0);
	item.appendChild(elem);
    });

    // "clean-up in post", if any
    process_callbacks();
});
