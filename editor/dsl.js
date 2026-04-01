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
	    console.log(elem);

	    elem = document.createElement("input");
	    elem.setAttribute("class", "form-control");
	    elem.setAttribute("id", dat["id"]);
	    elem.setAttribute("type", dat["type"]);
	    elem.setAttribute("placeholder", dat["placeholder"]);

	    frag.appendChild(elem);
	    console.log(elem);
	    break;

	case "list":
	    elem = document.createElement("label");
	    elem.setAttribute("class", "form-label");
	    elem.setAttribute("style", "margin-top: .5em;");
	    elem.appendChild(document.createTextNode(dat["label"]));

	    frag.appendChild(elem);
	    console.log(elem);

	    elem = document.createElement("a");
	    elem.setAttribute("class", "btn btn-primary btn-sm float-end");
	    elem.setAttribute("href", "#");
	    elem.setAttribute("role", "button");
	    elem.setAttribute("style", "margin-top: .5em;");
	    elem.appendChild(document.createTextNode("+"));

	    var callback = `console.log('${dat["id"]}')`;
	    elem.setAttribute("onclick", callback);

	    frag.appendChild(elem);
	    console.log(elem);

	    elem = document.createElement("div");
	    elem.setAttribute("class", "list-group");
	    elem.setAttribute("id", dat["id"]);

	    var sub = document.createElement("a");
	    sub.setAttribute("class", "list-group-item disabled");
	    sub.setAttribute("href", "#");
	    sub.appendChild(document.createTextNode("(empty)"));
	    elem.appendChild(sub);

	    frag.appendChild(elem);
	    console.log(elem);
	    break;

	default:
	    break;
	};
    };

    return frag;
};


// run after the page loads

window.addEventListener("load", function() {
    for (var i = 0; i < dsl_design.length; i++) {
	document.getElementById("editor-inputs").appendChild(
	    build_frag(
		document.createDocumentFragment(),
		dsl_design[i],
	    )
	);
    };
});
