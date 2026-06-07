const DESIGN_META = {
    "editor": [
	{
            "field": {
		"count": "one",
		"id": "recipe-title",
		"label": "Title",
		"placeholder": "Recipe name",
		"verb": "RECIPE",
		"json_loc": "title",
		"type": "text",
            },
	},
	{
            "field": {
		"count": "one",
		"id": "recipe-text",
		"label": "Text",
		"placeholder": "Recipe description",
		"verb": "TEXT",
		"json_loc": "text",
		"type": "textarea",
	    },
	},
	{
	    "summary": {
		"label": "header",
		"open": true,
		"type": [
		    {
			"list": {
			    "count": "zero-many",
			    "id": "cite-list",
			    "label": "sources",
			    "placeholder": "Source link",
			    "verb": "CITE",
			    "json_loc": "sources",
			    "type": "url",
			},
		    },
		    {
			"list": {
			    "count": "zero-many",
			    "id": "post-list",
			    "label": "galleries",
			    "placeholder": "Galleries link",
			    "verb": "POST",
			    "json_loc": "gallery",
			    "type": "url",
			},
		    },
		],
	    },
	},
	{
            "list": {
		"count": "one-many",
		"id": "closure-list",
		"label": "closures",
		"verb": "CLOSURE",
		"json_loc": "closures",
		"type": [
		    {
			"summary": {
			    "label": "closure",
			    "open": true,
			    "type": [
				{
				    "field": {
					"count": "one",
					"id": "closure-name-%",
					"label": "Name",
					"placeholder": "Closure name",
					"verb": "NAME",
					"json_loc": "title",
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
					"json_loc": "text",
					"type": "textarea",
				    },
				},
				{
				    "summary": {
					"label": "header",
					"open": true,
					"type": [
					    {
						"list": {
						    "count": "zero-many",
						    "id": "super-list-%",
						    "label": "supers",
						    "placeholder": "Supers",
						    "verb": "SUPER",
						    "json_loc": "supers",
						    "type": "symbol",
						},
					    },
					    {
						"list": {
						    "count": "zero-many",
						    "id": "keyword-list-%",
						    "label": "keywords",
						    "placeholder": "Keywords",
						    "verb": "KEYWORD",
						    "json_loc": "keywords",
						    "type": "symbol",
						},
					    },
					],
				    },
				},
				{
				    "summary": {
					"label": "dependencies",
					"open": true,
					"type": [
					    {
						"list": {
						    "count": "one-many",
						    "id": "container-list-%",
						    "label": "containers",
						    "verb": "CONTAINER",
						    "json_loc": "containers",
						    "type": [
							{
							    "field": {
								"count": "one",
								"id": "container-name-%",
								"label": "Name",
								"placeholder": "Container name",
								"verb": "NAME",
								"json_loc": "name",
								"type": "symbol",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "container-text-%",
								"label": "Text",
								"placeholder": "Container description",
								"verb": "TEXT",
								"json_loc": "text",
								"type": "textarea",
							    },
							},
							{
							    "lookup": "note",
							},
						    ],
						},
					    },
					    {
						"list": {
						    "count": "one-many",
						    "id": "tool-list-%",
						    "label": "tools",
						    "verb": "TOOL",
						    "json_loc": "tools",
						    "type": [
							{
							    "field": {
								"count": "one",
								"id": "tool-name-%",
								"label": "Name",
								"placeholder": "Tool name",
								"verb": "NAME",
								"json_loc": "name",
								"type": "symbol",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "tool-text-%",
								"label": "Text",
								"placeholder": "Tool description",
								"verb": "TEXT",
								"json_loc": "text",
								"type": "textarea",
							    },
							},
							{
							    "lookup": "note",
							},
						    ],
						},
					    },
					    {
						"list": {
						    "count": "one-many",
						    "id": "ingredient-list-%",
						    "label": "ingredients",
						    "verb": "INGREDIENT",
						    "json_loc": "ingredients",
						    "type": [
							{
							    "field": {
								"count": "one",
								"id": "ingredient-name-%",
								"label": "Name",
								"placeholder": "Ingredient name",
								"verb": "NAME",
								"json_loc": "name",
								"type": "symbol",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "ingredient-text-%",
								"label": "Text",
								"placeholder": "Ingredient description",
								"verb": "TEXT",
								"json_loc": "text",
								"type": "textarea",
							    },
							},
							{
							    "lookup": "note",
							},
						    ],
						},
					    },
					    {
						"list": {
						    "count": "one-many",
						    "id": "use-list-%",
						    "label": "uses",
						    "verb": "USE",
						    "json_loc": "uses",
						    "type": [
							{
							    "field": {
								"count": "one",
								"id": "use-name-%",
								"label": "Name",
								"placeholder": "Use name",
								"verb": "NAME",
								"json_loc": "name",
								"type": "symbol",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "use-text-%",
								"label": "Text",
								"placeholder": "Use description",
								"verb": "TEXT",
								"json_loc": "text",
								"type": "textarea",
							    },
							},
							{
							    "lookup": "note",
							},
						    ],
						},
					    },
					],
				    },
				},
				{
				    "list": {
					"count": "one-many",
					"id": "activity-list-%",
					"label": "activities",
					"verb": "ACTIVITY",
					"json_loc": "activities",
					"type": [
					    {
						"summary": {
						    "label": "activity",
						    "open": true,
						    "type": [
							{
							    "field": {
								"count": "one",
								"id": "activity-name-%",
								"label": "Container",
								"placeholder": "Activity container",
								"verb": "ACTIVITY",
								"json_loc": "container",
								"type": "symbol",
							    },
							},
							{
							    "field": {
								"count": "one",
								"id": "activity-text-%",
								"label": "Text",
								"placeholder": "Activity description",
								"verb": "TEXT",
								"json_loc": "title",
								"type": "textarea",
							    },
							},
							{
							    "list": {
								"count": "one-many",
								"id": "input-list-%",
								"label": "inputs",
								"verb": "INPUT",
								"json_loc": "inputs",
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "add-measure-%",
											    "label": "Measure",
											    "placeholder": "Add measure",
											    "verb": "MEASURE",
											    "json_loc": "amount",
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
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"lookup": "note",
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"lookup": "note",
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
								"label": "ops",
								"verb": "OP",
								"json_loc": "ops",
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"field": {
											    "count": "zero-one",
											    "id": "action-text-%",
											    "label": "Description",
											    "placeholder": "Action description",
											    "verb": "TEXT",
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "action-until-%",
											    "label": "Until",
											    "placeholder": "Action until",
											    "verb": "UNTIL",
											    "json_loc": "until",
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
											    "json_loc": "time",
											    "type": "text",
											},
										    },
										    {
											"lookup": "yields",
										    },
										    {
											"lookup": "note",
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
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "wait-until-%",
											    "label": "Until",
											    "placeholder": "Wait until",
											    "verb": "UNTIL",
											    "json_loc": "until",
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
											    "json_loc": "time",
											    "type": "text",
											},
										    },
										    {
											"lookup": "yields",
										    },
										    {
											"lookup": "note",
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"field": {
											    "count": "zero-one",
											    "id": "heat-text-%",
											    "label": "Description",
											    "placeholder": "Heat description",
											    "verb": "TEXT",
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "heat-until-%",
											    "label": "Until",
											    "placeholder": "Heat until",
											    "verb": "UNTIL",
											    "json_loc": "until",
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
											    "json_loc": "time",
											    "type": "text",
											},
										    },
										    {
											"lookup": "yields",
										    },
										    {
											"lookup": "note",
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"field": {
											    "count": "zero-one",
											    "id": "chill-text-%",
											    "label": "Description",
											    "placeholder": "Chill description",
											    "verb": "TEXT",
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "chill-until-%",
											    "label": "Until",
											    "placeholder": "Chill until",
											    "verb": "UNTIL",
											    "json_loc": "until",
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
											    "json_loc": "time",
											    "type": "text",
											},
										    },
										    {
											"lookup": "yields",
										    },
										    {
											"lookup": "note",
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
												"broil": [],
												"roast": [],
												"toast": [],
												"pressure": [],
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
											    "json_loc": "name",
											    "type": "symbol",
											},
										    },
										    {
											"field": {
											    "count": "zero-one",
											    "id": "bake-text-%",
											    "label": "Description",
											    "placeholder": "Bake description",
											    "verb": "TEXT",
											    "json_loc": "text",
											    "type": "textarea",
											},
										    },
										    {
											"field": {
											    "count": "one",
											    "id": "bake-at-%",
											    "label": "At",
											    "placeholder": "Bake temperature",
											    "verb": "AT",
											    "json_loc": "at",
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
											    "json_loc": "until",
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
											    "type": "time",
											},
										    },
										    {
											"lookup": "yields",
										    },
										    {
											"lookup": "note",
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
				{
				    "summary": {
					"label": "ratio",
					"type": [
					    {
						"field": {
						    "count": "zero-one",
						    "id": "ratio-name-%",
						    "label": "Name",
						    "placeholder": "Ratio name",
						    "verb": "RATIO",
						    "json_loc": "name",
						    "type": "text",
						},
					    },
					    {
						"field": {
						    "count": "zero-one",
						    "id": "ratio-parts-%",
						    "label": "Parts",
						    "placeholder": "Ratio parts",
						    "verb": "PARTS",
						    "json_loc": "parts",
						    "type": "textarea",
						},
					    },
					    {
						"field": {
						    "count": "zero-one",
						    "id": "ratio-formula-%",
						    "label": "Formula",
						    "placeholder": "Ratio formula",
						    "verb": "FORMULA",
						    "json_loc": "formula",
						    "type": "textarea",
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
    ],
    "yields": [
	{
	    "summary": {
		"label": "yields",
		"type": [
		    {
			"field": {
			    "count": "zero-one",
			    "id": "yields-name-%",
			    "label": "Name",
			    "placeholder": "Yields name",
			    "verb": "YIELDS",
			    "json_loc": "name",
			    "type": "symbol",
			},
		    },
		    {
			"field": {
			    "count": "one",
			    "id": "yields-measure-%",
			    "label": "Measure",
			    "placeholder": "Yields measure",
			    "verb": "MEASURE",
			    "json_loc": "amount",
			    "type": "text",
			},
		    },
		    {
			"checkbox": {
			    "count": "one",
			    "id": "yields-intermediate-%",
			    "label": "Intermediate",
			    "placeholder": "Yields intermediate",
			    "verb": "INTERMEDIATE",
			    "json_loc": "intermediate",
			    "type": "checkbox",
			},
		    },
		    {
			"lookup": "store",
		    },
		],  
	    },
	},
    ],
    "store": [
	{
	    "summary": {
		"label": "store",
		"type": [
		    {
			"field": {
			    "count": "zero-one",
			    "id": "store-text-%",
			    "label": "Storage",
			    "placeholder": "Store description",
			    "verb": "STORE",
			    "json_loc": "text",
			    "type": "text",
			},
		    },
		    {
			"field": {
			    "count": "one",
			    "id": "store-duration-%",
			    "label": "Duration",
			    "placeholder": "Store duration",
			    "verb": "DURATION",
			    "json_loc": "time",
			    "type": "text",
			},
		    },
		],
	    },
	},
    ],
    "note": [
	{
	    "summary": {
		"label": "note",
		"type": [
		    {
			"field": {
			    "count": "zero-one",
			    "id": "note-text-%",
			    "label": "Note",
			    "placeholder": "Text description",
			    "verb": "NOTE",
			    "json_loc": "text",
			    "type": "textarea",
			},
		    },
		],
	    },
	},
    ],
}
