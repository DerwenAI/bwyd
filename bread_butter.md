TITLE: "Bread and ButteAr Pickles"
TEXT: "Much better than store-bought pickles"
LICENSE: "CC-BY-NC-SA-4.0"
UPDATED: "2020-07-24"
CITE: "https://www.browneyedbaker.com/bread-and-butter-pickles/"
POST: "https://www.instagram.com/p/CDJy2u7JqSO/"
POST: "https://www.instagram.com/p/C_EzMRLPEgn/"

//  * yields: 4-5 cups

CLOSURE: "leached veggies"
    TEXT: "Start with ripe but crisp cukes, then brine them."

    CONTAINER sink: "kitchen sink"
    CONTAINER board: "cutting board"
    CONTAINER bowl: "mixing bowl"
    TOOL hand: "clean hands"
    TOOL knife: "French chef knife"
    TOOL spatula: "silicone spatula"

    INGREDIENT cucumbers: "persian cucumbers"
    INGREDIENT onion: "small white onion"
    INGREDIENT salt: "pickling salt"

    FOCUS sink

    ACTIVITY: "clean cucumbers"

    ADD cucumbers (500 g)
    // 5 medium sized

    ACTION hand: "rinse in running cold water"
        UNTIL: "cukes are clean, and any extra gunk has been removed"
        TIME (2 min)

    FOCUS board

    ACTIVITY: "prep cucumbers"

    ADD onion (100 g)
    // 1 small white onion

    ACTION hand: "peel onions"
        UNTIL: "cut off ends, peel off outer/paper skin"
        TIME (30 sec)

    TRANSFER cucumbers

    ACTION knife: "blend"
        UNTIL: "slice cukes and onion to .5 cm thick pieces"
	TIME (4 min)

    FOCUS bowl

    ACTIVITY: "leaching"

    TRANSFER cucumbers
    TRANSFER onion
    ADD salt (25 g)

    ACTION spatula: "toss slices with salt"
        UNTIL: "thoroughly coated"
	TIME: (30 sec)

    ACTION hand: "cover with ice"
        UNTIL: "veggies are fully covered"
        TIME (1 min)

    CHILL bowl: "chill"
        UNTIL: "liquid from cukes has leeched out"
        TIME (1.5 hrs)

    FOCUS sink

    ACTIVITY: "rinse"

    ACTION hand: "rinse in running cold water"
        UNTIL: "remove the bitterness of the brine"
        TIME (1 min)

YIELDS leached_veggies (400 g) INTERMEDIATE


CLOSURE: "brine the pickles"
    TEXT: "Change the spices, sugars, and vinegars to combine sweet and tangy flavors."

    CONTAINER pan: "medium saucepan"
    TOOL spatula: "silicone spatula"

    INGREDIENT mustard: "mustard powder"
    INGREDIENT tumeric: "tumeric powder"
    INGREDIENT celery_seeds: "whole celery seeds"
    INGREDIENT coriander_seeds: "whole coriander seeds"
    INGREDIENT sugar: "granulated sugar, or brown"
    INGREDIENT vinegar: "raw apple cider vinegar, or white wine"
    USE leached_veggies

    FOCUS pan

    ACTIVITY: "prep brine"

    ADD mustard (2 g)
    // 1 tsp
    ADD tumeric (2 g)
    // 1/8 tsp
    ADD celery_seeds (1 g)
    // 1/2 tsp
    ADD coriander_seeds (1 g)
    // 1/2 tsp
    ADD sugar (200 g)
    // 1 cup
    ADD vinegar (350 g)
    // 1.5 cup

    ACTION spatula: "gently mix"
        UNTIL: "sugar dissolves"
	TIME (30 sec)

    HEAT pan: "simmer over medium heat"
        UNTIL: "bring to a light boil"
        TIME (5 min)

    ADD leached_veggies (400 g)

    HEAT pan: "simmer over medium heat"
        UNTIL: "bring to a light boil"
        TIME (3 min)

YIELDS brined_veggies (.9 l) INTERMEDIATE


CLOSURE: "jar the pickles"
    TEXT: "Refrigerate +1 days before eating"

    CONTAINER jar: "sanitized quart jar, still hot"
    TOOL spatula: "silicone spatula"
    TOOL hand: "clean hands"

    FOCUS jar

    ACTIVITY: "pack jar"

    USE brined_veggies (.9 l)

    ACTION spatula: "transfer brined veggies into jar"
        UNTIL: "jar is almost filled, with 1 cm air gap from top"
	TIME (30 sec)

    ACTIVITY: "let cool"

    ACTION hand: "shake jar to loosen any bubbles, then seal"
        UNTIL: "jar is sealed"
        TIME (30 sec)

    CHILL jar: "let cool on countertop"
        UNTIL: "room temperature"
        TIME (1 hrs)

    CHILL jar: "in refrigerator"
        UNTIL: "allow mild fermentation"
        TIME (1 day)

    STORE jar: "in refrigerator"
        UPTO (1 mon)

YIELDS pickles (.9 l)


// modify cucumber/liquid ratio to increase veggies by 1/3
// substitute: sugar with 2/3 honey
// substitute: mustard powder with 1/2 mustard seed
