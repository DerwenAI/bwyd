const dsl_design = [
    {
        "field": {
	    "id": "module-title",
	    "label": "Title",
	    "placeholder": "My Recipe",
            "grammar": "TITLE",
            "count": "one",
            "type": "text"
        }
    },
    {
        "field": {
	    "id": "module-text",
	    "label": "Text",
	    "placeholder": "Text Description",
            "grammar": "TEXT",
            "count": "one",
            "type": "text"

	}
    }
]


function build_frag (frag, design) {
    for (const [kind, dat] of Object.entries(design)) {
	if (kind == "field") {
	    var elem = document.createElement("label");
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
