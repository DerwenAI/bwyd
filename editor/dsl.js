const dsl_stack = [];
const dsl_locate = {};

const dsl_design = [
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
]


function build_frag (frag, design) {
    var elem = null;

    for (const [kind, dat] of Object.entries(design)) {
	switch (kind) {
	case "field":
	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("for", dat["id"]);
	    elem.appendChild(document.createTextNode(dat["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("input");
	    elem.setAttribute("class", "form-control");
	    elem.setAttribute("id", dat["id"]);
	    elem.setAttribute("type", dat["type"]);
	    elem.setAttribute("placeholder", dat["placeholder"]);
	    frag.appendChild(elem);
	    break;

	case "list":
	    elem = document.createElement("br");
	    frag.appendChild(elem);

	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.appendChild(document.createTextNode(dat["label"]));
	    frag.appendChild(elem);

	    elem = document.createElement("a");
	    elem.setAttribute("class", "btn btn-primary btn-sm float-end");
	    elem.setAttribute("href", "#");
	    elem.setAttribute("role", "button");
	    elem.appendChild(document.createTextNode("+"));

	    const group_id = dat["id"];
	    var callback = `list_add('${group_id}')`;
	    elem.setAttribute("onclick", callback);
	    dsl_locate[group_id] = dat;
	    frag.appendChild(elem);

	    elem = document.createElement("div");
	    elem.setAttribute("class", "list-group");
	    elem.setAttribute("id", group_id);
	    frag.appendChild(elem);

	    callback = `list_del('${group_id}', 0)`;
	    dsl_stack.push(callback);
	    break;

	default:
	    break;
	};
    };

    return frag;
};


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
    const dat = dsl_locate[group_id];
    const item_id = self.crypto.randomUUID();

    var elem = document.createElement("div");
    elem.setAttribute("class", "row list-group-item");

    var input = document.createElement("input");
    input.setAttribute("class", "form-control");
    input.setAttribute("id", item_id);
    input.setAttribute("type", dat["type"]);
    input.setAttribute("placeholder", dat["placeholder"]);
    input.setAttribute("style", "display: inline-block; width: 93%;");

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

	var sub = document.createElement("em");
	sub.appendChild(document.createTextNode("(empty)"));

	elem.appendChild(sub);
	list_group.appendChild(elem);
    }
    else if (item_id != 0){
	const item = document.getElementById(item_id);
	item.parentNode.remove();
	list_del(group_id, 0);
    };
};


// run after the page loads

window.addEventListener("load", function() {
    // build the default editor
    for (var i = 0; i < dsl_design.length; i++) {
	document.getElementById("editor-inputs").appendChild(
	    build_frag(
		document.createDocumentFragment(),
		dsl_design[i],
	    )
	);
    };

    // clean-up at end
    while (dsl_stack.length > 0) {
	const callback = dsl_stack.pop();
	eval(callback);
    };
});
