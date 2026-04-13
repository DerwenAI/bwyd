//////////////////////////////////////////////////////////////////////
// global data structures

var BWYD_DEBUG = [];
var CALLBACK_QUEUE = [];
var ELEM_META = {};


//////////////////////////////////////////////////////////////////////
// utility methods for navigating dynamic HTML
//

// append a UUID as a relative component to an ID
function get_rel_id (id) {
    if (id.slice(-1) === "%") {
	return id.replace(/%/g, self.crypto.randomUUID());
    };

    return id;
};


// generators for filtering the "caboose" from item lists
function* gen_items (list_group) {
    for (const item of list_group.children) {
        if (!item.id.startsWith("caboose-")) {
	    yield item;
	};
    };
};


function* gen_inputs (item, node_names) {
    for (const input of item.children) {
	if (node_names.includes(input.nodeName)) {
	    yield input;
	};
    };
};


//////////////////////////////////////////////////////////////////////
// dynamically generate HTML from design metadata fragments,
// driven by context from: input files, user edits
//

function build_input (meta, item_id) {
    var input = null;

    if (["text", "symbol", "url"].includes(meta["type"])) {
	input = document.createElement("input");
	input.setAttribute("type", "text");
	input.setAttribute("class", "form-control");
	input.setAttribute("id", item_id);
    }
    else if (["textarea"].includes(meta["type"])) {
	input = document.createElement("textarea");
	input.setAttribute("class", "form-control");
	input.setAttribute("id", item_id);
    }
    else if (["checkbox"].includes(meta["type"])) {
	input = document.createElement("input");
	input.setAttribute("type", "checkbox");
	input.setAttribute("class", "form-check-input");
	input.setAttribute("id", item_id);
	input.setAttribute("name", item_id);
	input.setAttribute("value", meta["label"]);
    };

    return input;
};


function build_field (frag, meta, depth) {
    var item_id = get_rel_id(meta["id"]);
    ELEM_META[item_id] = meta;

    var label = document.createElement("label");
    label.setAttribute("class", "form-label");
    label.setAttribute("for", item_id);
    label.appendChild(document.createTextNode(meta["label"]));
    frag.appendChild(label);

    var input = build_input(meta, item_id);
    input.setAttribute("placeholder", meta["placeholder"]);
    frag.appendChild(input);
};


function build_checkbox (frag, meta, depth) {
    var item_id = get_rel_id(meta["id"]);
    ELEM_META[item_id] = meta;

    var input = build_input(meta, item_id);
    input.setAttribute("style", "margin-top: 1rem;");
    frag.appendChild(input);

    var label = document.createElement("label");
    label.setAttribute("class", "form-check-label");
    label.setAttribute("for", item_id);
    label.setAttribute("style", "margin-left: 1rem; margin-top: .7rem;");
    label.appendChild(document.createTextNode(meta["label"]));
    frag.appendChild(label);
};


function build_list (frag, meta, depth) {
    var group_id = get_rel_id(meta["id"]);
    var color = Math.round((1.0 - (depth * .03)) * 100.0);

    var row = document.createElement("div");
    row.setAttribute("class", "row");
    row.setAttribute("id", get_rel_id("%"));
    row.setAttribute("style", `min-height: 8rem; width: 100%; margin-top: 2rem; margin-left: -2rem; background: hsl(0 0 ${color});`);
    frag.appendChild(row);

    var col = document.createElement("div");
    col.setAttribute("class", "col-1");
    col.setAttribute("style", "padding: 0;");
    row.appendChild(col);

    var label = document.createElement("label");
    label.setAttribute("class", "form-label");
    label.setAttribute("for", group_id);
    label.setAttribute("style", "margin-top: 1rem; rotate: 270deg; color: hsl(0, 0%, 75%); font-weight: bold; padding-left: 0;");
    label.appendChild(document.createTextNode(meta["label"]));
    col.appendChild(label);

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
    var caboose = document.createElement("div");
    caboose.setAttribute("id", get_rel_id("caboose-%"));
    caboose.setAttribute("class", "list-group-item");

    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-outline-primary btn-sm");
    button.setAttribute("style", "width: 2.1em; display: inline;");

    var callback = `list_add('${group_id}', ${depth})`;
    button.setAttribute("onclick", callback);

    var icon = document.createElement("i");
    icon.setAttribute("class", "bi bi-plus");
    button.appendChild(icon);
    caboose.appendChild(button);

    var para = document.createElement("span");
    var text = `add new ${meta["label"].toLowerCase()}`;
    para.appendChild(document.createTextNode(text));
    para.setAttribute("style", "font-size: .75em; font-style: oblique; color: #aaa; margin-left: 1em;");

    caboose.appendChild(para);
    list_group.appendChild(caboose);
};


function build_select (frag, meta, depth) {
    var item_id = get_rel_id(meta["id"]);
    ELEM_META[item_id] = meta;

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

    var callback = `menu_select('${item_id}', ${depth})`;
    select.setAttribute("onchange", callback);
    frag.appendChild(select);
};


function build_summary (frag, meta, depth) {
    const details = document.createElement("details");
    details.open = true;

    const summary = document.createElement("summary");
    const para = document.createElement("span");
    const text = meta["label"].toLowerCase();

    para.appendChild(document.createTextNode(text));
    para.setAttribute("style", "font-size: .75em; font-style: oblique; color: #aaa; margin-left: 1em;");

    summary.appendChild(para);
    details.appendChild(summary);

    meta["type"].forEach(function(struct_meta) {
	var item = design_build(struct_meta, depth);
	details.appendChild(item);
    });

    frag.appendChild(details);
};


function design_build (design_meta, depth) {
    const frag = document.createDocumentFragment();

    for (const [kind, meta] of Object.entries(design_meta)) {
	switch (kind) {
	case "field":
	    build_field(frag, meta, depth);
	    break;

	case "checkbox":
	    build_checkbox(frag, meta, depth);
	    break;

	case "list":
	    build_list(frag, meta, depth);
	    break;

	case "select":
	    build_select(frag, meta, depth);
	    break;

	case "summary":
	    build_summary(frag, meta, depth);
	    break;

	default:
	    console.log("UNKNOWN DESIGN:", kind, meta, depth);
	    break
	};
    };

    return frag;
};


//////////////////////////////////////////////////////////////////////
// list handling
//

function list_add (group_id, depth) {
    const list_group = document.getElementById(group_id);
    var is_structured = false;

    // build a new item to insert
    const meta = ELEM_META[group_id];
    var item_id = self.crypto.randomUUID();

    ELEM_META[item_id] = meta;

    const elem = document.createElement("div");
    elem.setAttribute("class", "row list-group-item");

    if (["text", "textarea", "symbol", "url", "checkbox"].includes(meta["type"])) {
	var input = build_input(meta, item_id);
	input.setAttribute("placeholder", meta["placeholder"]);
	input.setAttribute("class", "url-field");
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
	    var item = design_build(struct_meta, depth + 1);
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
	for (const item of built_elem.children) {
	    if ((item.classList != null) && item.classList.contains("form-control")) {
		item_id = item.id;
		break;
	    };
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


//////////////////////////////////////////////////////////////////////
// menu handling
//

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


//////////////////////////////////////////////////////////////////////
// encode the current editor content in the DSL language
//

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


function encode_inputs (list_group, line, script) {
    for (const item of gen_items(list_group)) {
	var kind = item.children[1].value;

	var first_input = null;
	var measure = "";
	var text = "";

	for (const input of gen_inputs(item, ["INPUT", "TEXTAREA"])) {
	    switch (kind) {
	    case "add":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-measure`)) {
		    measure = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		};
		break;

	    case "transfer":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		break;
	    };
	};

	if (first_input != null) {
	    var code = null;

	    switch (kind) {
	    case "add":
		code = `ADD ${first_input.value.trim()} (${measure})`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};
		break;

	    case "transfer":
		code = `TRANSFER ${first_input.value.trim()}`;
		break;
	    };
		
	    if (code != null) {
		line = encode_statement(first_input, code, line, script);
	    };
	};
    };

    return line;
};


function encode_operations (list_group, line, script) {
    for (const item of gen_items(list_group)) {
	var kind = item.children[1].value;

	var first_input = null;
	var mode = "";
	var text = "";
	var until = "";
	var duration = "";

	for (const input of gen_inputs(item, ["INPUT", "TEXTAREA", "SELECT"])) {
	    switch (kind) {
	    case "action":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-until`)) {
		    until = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-duration`)) {
		    duration = input.value.trim();
		};
		break;

	    case "wait":
		if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-until`)) {
		    first_input = input;
		    until = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-duration`)) {
		    duration = input.value.trim();
		};
		break;

	    case "heat":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-until`)) {
		    until = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-duration`)) {
		    duration = input.value.trim();
		};
		break;

	    case "chill":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-until`)) {
		    until = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-duration`)) {
		    duration = input.value.trim();
		};
		break;

	    case "bake":
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-mode`)) {
		    mode = input.value.toUpperCase();
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-until`)) {
		    until = input.value.trim();
		}
		else if (input.id.startsWith(`${kind}-duration`)) {
		    duration = input.value.trim();
		};
		break;
	    };
	};

	if (first_input != null) {
	    var code = null;

	    switch (kind) {
	    case "action":
		code = `ACTION ${first_input.value.trim()}`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};

		code =`${code} \n UNTIL: "${until}" \n TIME (${duration})`;
		break;

	    case "wait":
		code = `WAIT`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};

		code =`${code} \n UNTIL: "${until}" \n TIME (${duration})`;
		break;

	    case "heat":
		code = `HEAT ${first_input.value.trim()}`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};

		code =`${code} \n UNTIL: "${until}" \n TIME (${duration})`;
		break;

	    case "chill":
		code = `CHILL ${first_input.value.trim()}`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};

		code =`${code} \n UNTIL: "${until}" \n TIME (${duration})`;
		break;

	    case "bake":
		code = `${mode} ${first_input.value.trim()}`;

		if (text.length > 0) {
		    code = `${code}: "${text}"`;
		};

		code =`${code} \n UNTIL: "${until}" \n TIME (${duration})`;
		break;
	    };
		
	    if (code != null) {
		line = encode_statement(first_input, code, line, script);
	    };
	};
    };

    return line;
};


function encode_activities (group_id, line, script) {
    for (const item of gen_items(document.getElementById(group_id))) {
	for (const elem of gen_inputs(item, ["DIV"])) {
	    const group = elem.children[1].children[0];

	    if (group.id.startsWith("input-list")) {
		line = encode_inputs(group, line, script);
	    }
	    else if (group.id.startsWith("operation-list")) {
		line = encode_operations(group, line, script);
	    };
	};
    };

    return line;
};


function encode_dependency (group_id, kind, line, script) {
    const verb = ELEM_META[group_id].verb;

    for (const item of document.getElementById(group_id).children) {
	var first_input = null;
	var text = "";

	for (const input of item.children) {
	    if ((input.id in ELEM_META) && !input.id.startsWith("caboose-") && ["INPUT", "TEXTAREA"].includes(input.nodeName)) {
		if (input.id.startsWith(`${kind}-name`)) {
		    first_input = input;
		}
		else if (input.id.startsWith(`${kind}-text`)) {
		    text = input.value.trim();
		};
	    };
	};

	if (first_input != null) {
	    var code = `${verb} ${first_input.value.trim()}: "${text}"`;
	    line = encode_statement(first_input, code, line, script);
	};
    };

    return line;
};


function encode_list (group_id, line, script) {
    document.getElementById(group_id).childNodes.forEach(
	function(item, index) {
	    item.childNodes.forEach(
		function(input, index) {
		    if ((input.id in ELEM_META) && !input.id.startsWith("caboose-")) {
			const verb = ELEM_META[input.id].verb;
			const code = `${verb}: "${input.value.trim()}"`;
			line = encode_statement(input, code, line, script);
		    };
		}
	    );
	}
    );

    return line;
};


function encode_head (group_id, line, script) {
    document.getElementById(group_id).childNodes.forEach(
	function(input, index) {
	    if ((input.id in ELEM_META) && ["INPUT", "TEXTAREA"].includes(input.nodeName)) {
		const verb = ELEM_META[input.id].verb;
		const code = `${verb}: "${input.value.trim()}"`;
		line = encode_statement(input, code, line, script);
	    };
	}
    );

    return line;
};


function encode_module () {
    const script = [];
    var line = 1;
    var code = null;

    BWYD_DEBUG = [];

    // encode top-level inputs for the module
    var group_id = "editor-inputs";
    line = encode_head(group_id, line, script);

    group_id = "cite-list";
    line = encode_list(group_id, line, script);

    group_id = "post-list";
    line = encode_list(group_id, line, script);

    // encode the CLOSURE list, each of which have compound elements
    for (const closure of gen_items(document.getElementById("closure-list"))) {
	// add a leading separator
	line = encode_statement(null, "", line, script);

	for (const input of gen_inputs(closure, ["INPUT", "TEXTAREA"])) {
	    if (input.id.startsWith("closure-name")) {
		code = `CLOSURE: "${input.value.trim()}"`;
		line = encode_statement(input, code, line, script);
	    }
	    else if (input.id.startsWith("closure-text")) {
		code = `TEXT: "${input.value.trim()}"`;
		line = encode_statement(input, code, line, script);
	    };
	};

	for (const input of gen_inputs(closure, ["DIV"])) {
	    var group = input.children[1].children[0];

	    if (group.id.startsWith("super-list")) {
		line = encode_list(group.id, line, script);
	    }
	    else if (group.id.startsWith("keyword-list")) {
		line = encode_list(group.id, line, script);
	    }
	    else if (group.id.startsWith("container-list")) {
		line = encode_dependency(group.id, "container", line, script);
	    }
	    else if (group.id.startsWith("tool-list")) {
		line = encode_dependency(group.id, "tool", line, script);
	    }
	    else if (group.id.startsWith("ingredient-list")) {
		line = encode_dependency(group.id, "ingredient", line, script);
	    }
	    else if (group.id.startsWith("use-list")) {
		line = encode_dependency(group.id, "use", line, script);
	    }
	    else if (group.id.startsWith("activity-list")) {
		line = encode_activities(group.id, line, script);
	    };
	};

	// add a trailing separator
	line = encode_statement(null, ";", line, script);
    };

    // debug: update the <textarea/> script display
    document.getElementById("bwyd-script").value = script.join("\n");

    // TODO: roundtrip with server for parsing and validation
};


//////////////////////////////////////////////////////////////////////
// start-up: run these steps *AFTER* the HTML page loads
//

window.addEventListener("load", function() {
    // build a default editor page from the design metadata
    const item = document.getElementById("editor-inputs");

    DESIGN_META.forEach(function(struct_meta) {
	const elem = design_build(struct_meta, 0);
	item.appendChild(elem);
    });

    // "clean-up in post", if any
    while (CALLBACK_QUEUE.length > 0) {
	const callback = CALLBACK_QUEUE.pop();
	eval(callback);
    };
});
