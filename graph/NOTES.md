## keywords

	Focus Node: <urn:bwyd:pacoid:keyword:american>
	Focus Node: <urn:bwyd:pacoid:keyword:breakfast>
	Focus Node: <urn:bwyd:pacoid:keyword:california>
	Focus Node: <urn:bwyd:pacoid:keyword:entree>
	Focus Node: <urn:bwyd:pacoid:keyword:fermented>
	Focus Node: <urn:bwyd:pacoid:keyword:gluten_free>
	Focus Node: <urn:bwyd:pacoid:keyword:nordic>
	Focus Node: <urn:bwyd:pacoid:keyword:salty>
	Focus Node: <urn:bwyd:pacoid:keyword:savory>
	Focus Node: <urn:bwyd:pacoid:keyword:starch>
	Focus Node: <urn:bwyd:pacoid:keyword:sweet_sour>

	Focus Node: <urn:bwyd:pacoid:ingredient:parchment>
	Focus Node: <urn:bwyd:pacoid:ingredient:turmeric_powder>

---

Recipe = "module"
	wd:Q219239

Closure
	depends_on
	consumes
	wd:Q320346
	wd:Q2235289

Ingredient
	wd:Q25403900
	foodon:00004274

Product rdfs:subClassOf Ingredient
	produces
	wd:Q951964
	foodon:00001002

Super
	rdfs:subClassOf
	foodon:03543945

Keyword
	skos:related	
	wd:Q1072684



appliance
	wd:Q1183543
	wd:Q1751609
container
	wd:Q987767
utensil
	wd:Q1310214

activity
	lrmi:actvityPlan
	wd:Q759676

operation
action
    a bbo:UserTask ;
