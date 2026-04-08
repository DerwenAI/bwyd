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
			"count": "zero-one",
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
		{
		    "list": {
			"count": "one-many",
			"id": "activity-list-%",
			"label": "Activities",
			"verb": "ACTIVITY",
			"type": [
			    {
				"list": {
				    "count": "one-many",
				    "id": "input-list-%",
				    "label": "Inputs",
				    "verb": "INPUT",
				    "type": [
					{
					    "select": {
						"count": "one",
						"id": "input-%",
						"type": {
						    "add": [
							{
							    "field": {
								"count": "one",
								"id": "add-name-%",
								"label": "Name",
								"placeholder": "Add name",
								"verb": "ADD",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "add-measure-%",
								"label": "Measure",
								"placeholder": "Add measure",
								"verb": "MEASURE",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "zero-one",
								"id": "add-text-%",
								"label": "Text",
								"placeholder": "Add description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
						    ],
						    "transfer": [
							{
							    "field": {
								"count": "one",
								"id": "transfer-name-%",
								"label": "Name",
								"placeholder": "Transfer name",
								"verb": "TRANSFER",
								"type": "text",
							    },
							},
						    ],
						},
					    },
					},
				    ],
				},
			    },
			    {
				"list": {
				    "count": "one-many",
				    "id": "operation-list-%",
				    "label": "Ops",
				    "verb": "OP",
				    "type": [
					{
					    "select": {
						"count": "one",
						"id": "operation-%",
						"type": {
						    "action": [
							{
							    "field": {
								"count": "one",
								"id": "action-name-%",
								"label": "Name",
								"placeholder": "Action name",
								"verb": "ACTION",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "zero-one",
								"id": "action-text-%",
								"label": "Description",
								"placeholder": "Action description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "action-until-%",
								"label": "Until",
								"placeholder": "Action until",
								"verb": "UNTIL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "action-duration-%",
								"label": "Duration",
								"placeholder": "Action duration",
								"verb": "DURATION",
								"type": "text",
							    },
							},
						    ],
						    "wait": [
							{
							    "field": {
								"count": "zero-one",
								"id": "wait-text-%",
								"label": "Description",
								"placeholder": "Wait description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "wait-until-%",
								"label": "Until",
								"placeholder": "Wait until",
								"verb": "UNTIL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "wait-duration-%",
								"label": "Duration",
								"placeholder": "Wait duration",
								"verb": "DURATION",
								"type": "text",
							    },
							},
						    ],
						    "heat": [
							{
							    "field": {
								"count": "one",
								"id": "heat-name-%",
								"label": "Name",
								"placeholder": "Heat name",
								"verb": "HEAT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "zero-one",
								"id": "heat-text-%",
								"label": "Description",
								"placeholder": "Heat description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "heat-until-%",
								"label": "Until",
								"placeholder": "Heat until",
								"verb": "UNTIL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "heat-duration-%",
								"label": "Duration",
								"placeholder": "Heat duration",
								"verb": "DURATION",
								"type": "text",
							    },
							},
						    ],
						    "chill": [
							{
							    "field": {
								"count": "one",
								"id": "chill-name-%",
								"label": "Name",
								"placeholder": "Chill name",
								"verb": "CHILL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "zero-one",
								"id": "chill-text-%",
								"label": "Description",
								"placeholder": "Chill description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "chill-until-%",
								"label": "Until",
								"placeholder": "Chill until",
								"verb": "UNTIL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "chill-duration-%",
								"label": "Duration",
								"placeholder": "Chill duration",
								"verb": "DURATION",
								"type": "text",
							    },
							},
						    ],
						    "bake": [
							{
							    "select": {
								"count": "one",
								"id": "bake-mode-%",
								"label": "Oven Mode",
								"type": {
								    "bake": [],
								    "toast": [],
								    "broil": [],
								    "roast": [],
								},
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "bake-name-%",
								"label": "Name",
								"placeholder": "Bake name",
								"verb": "BAKE",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "zero-one",
								"id": "bake-text-%",
								"label": "Description",
								"placeholder": "Bake description",
								"verb": "TEXT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "bake-at-%",
								"label": "At",
								"placeholder": "Bake temperature",
								"verb": "AT",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "bake-until-%",
								"label": "Until",
								"placeholder": "Bake until",
								"verb": "UNTIL",
								"type": "text",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "bake-duration-%",
								"label": "Duration",
								"placeholder": "Bake duration",
								"verb": "DURATION",
								"type": "text",
							    },
							},
						    ],
						},
					    },
					}
				    ],
				},
			    },
			],
		    },
		},
	    ],
        },
    },
]
