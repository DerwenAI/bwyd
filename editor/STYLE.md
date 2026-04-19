blue-background-class {
}

btn {
}

btn-light {
}

btn-outline-danger {
}

btn-outline-primary {
}

btn-sm {
}

col-1 {
}

col-8 {
}

form-check-input {
}

form-check-label {
}

form-control {
}

form-label {
}

list-group {
}

list-group-item {
}

row {
}

url-field {
}


//////////////////////////////////////////////////////////////////////

function build_input (meta, item_id) {
    if (["text", "symbol", "url"].includes(meta["type"])) {
	input.setAttribute("class", "form-control");

    else if (["textarea"].includes(meta["type"])) {
	input.setAttribute("class", "form-control");

    else if (["checkbox"].includes(meta["type"])) {
	input.setAttribute("class", "form-check-input");


function build_field (frag, meta, depth) {
    label.setAttribute("class", "form-label");


function build_checkbox (frag, meta, depth) {
    input.setAttribute("style", "margin-top: 1rem;");

    label.setAttribute("class", "form-check-label");
    label.setAttribute("style", "margin-left: 1rem; margin-top: .7rem;");


function build_list (frag, meta, depth) {
    row.setAttribute("class", "row");
    row.setAttribute("style", `min-height: 8rem; width: 100%; margin-top: 2rem; margin-left: -2rem; background: hsl(0 0 ${color});`);

    col.setAttribute("class", "col-1");
    col.setAttribute("style", "padding: 0;");

    label.setAttribute("class", "form-label");

    col.setAttribute("class", "col-8");

    list_group.setAttribute("class", "list-group");

	ghostClass: "blue-background-class",

    caboose.setAttribute("class", "list-group-item");

    button.setAttribute("class", "btn btn-outline-primary btn-sm");
    button.setAttribute("style", "width: 2.1em; display: inline;");

    para.setAttribute("style", "font-size: .75em; font-style: oblique; color: #aaa; margin-left: 1em;");


function build_select (frag, meta, depth) {
    select.setAttribute("class", "form-control");
    select.setAttribute("style", "display: inline-block; width: 93%;");

    para.setAttribute("style", "font-style: oblique; color: #aaa;");


function build_summary (frag, meta, depth) {
    para.setAttribute("style", "font-size: .75em; font-style: oblique; color: #aaa; margin-left: 1em;");


function list_add (group_id, depth) {
    elem.setAttribute("class", "row list-group-item");

    if (["text", "textarea", "symbol", "url", "checkbox"].includes(meta["type"])) {
	input.setAttribute("class", "url-field");
	input.setAttribute("style", "display: inline-block; width: 87%;");

    button.setAttribute("class", "btn btn-sm float-end");
    button.setAttribute("style", "width: 2.1em;");

    if (is_structured) {
	for (const item of built_elem.children) {
	    if ((item.classList !== null) && item.classList.contains("form-control")) {
		item_id = item.id;
		break;
	    };
	};

	button.classList.add("btn-outline-danger");

    else {
	button.classList.add("btn-light");

