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
								"count": "one",
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
			],
		    },
		},
	    ],
        },
    },
]
