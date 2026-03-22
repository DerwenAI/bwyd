// ── document model state ──

let keywords = [];
let activities = []; // { name, ingredients:[], steps:[] }

// ── DOM refs ──

const title_input = document.getElementById("doc-title");
const source_input = document.getElementById("doc-source");

const kwBox = document.getElementById("kw-box");
const kwInput = document.getElementById("kw-input");

const actContainer = document.getElementById("activities-container");
const emptyMsg = document.getElementById("empty-msg");
const addActBtn = document.getElementById("add-activity-btn");

const jsonOut = document.getElementById("json-output");
const copyBtn = document.getElementById("copy-btn");


// ── helper functions ──

function esc (s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
}

function renderJSON () {
    const doc = {
	title: title_input.value,
	source: source_input.value,
	keywords,
	activities: activities.map(a => ({
            name: a.name,
            ingredients: a.ingredients,
            steps: a.steps
	}))
    };

    jsonOut.textContent = JSON.stringify(doc, null, 2);
}


// ── tag input factory ──

function initTagBox (box, input, getList, setList, tagClass) {
    function renderTags () {
	box.querySelectorAll(".tag").forEach(t => t.remove());

	getList().forEach((val, i) => {
            const tag = document.createElement("span");
            tag.className = `tag ${tagClass}`;
            tag.innerHTML = `${esc(val)}<button data-i="${i}">&times;</button>`;
            box.insertBefore(tag, input);
	});

	renderJSON();
    }

    function add (raw) {
	const v = raw.trim();
	const list = getList();

	if (v && !list.includes(v)) {
	    list.push(v);
	    setList(list);
	    renderTags();
	}
    }

    input.addEventListener("keydown", e => {
	if ((e.key === "Enter" || e.key === ",") && input.value.replace(",", "").trim()) {
            e.preventDefault();
            add(input.value.replace(",", ""));
            input.value = "";
	}

	if (e.key === "Backspace" && !input.value && getList().length) {
            const list = getList();
	    list.pop();
	    setList(list);
	    renderTags();
	}
    });

    input.addEventListener("input", () => {
	if (input.value.includes(",")) {
            input.value.split(",").forEach(p => {
		if (p.trim()) add(p);
	    });

            input.value = "";
	}
    });

    box.addEventListener("click", e => {
	if (e.target.tagName === "BUTTON" && e.target.dataset.i !== undefined) {
            const list = getList();
	    list.splice(Number(e.target.dataset.i), 1);
	    setList(list);
	    renderTags();
	}

	input.focus();
    });

    input.addEventListener("focus", () => box.classList.add("focused"));
    input.addEventListener("blur",  () => box.classList.remove("focused"));

    return renderTags;
  }


// ── keywords tag box ──

initTagBox(kwBox, kwInput, () => keywords, l => { keywords = l; }, "tag--kw");


// ── activities ──

function renderActivities () {
    emptyMsg.style.display = activities.length ? "none" : "block";

    // remove old cards
    actContainer.querySelectorAll(".activity-card").forEach(c => c.remove());

    activities.forEach((act, ai) => {
	const card = document.createElement("div");
	card.className = "activity-card";
	card.innerHTML = `
        <div class="activity-title-row">
          <input type="text" class="act-name" value="${esc(act.name)}" placeholder="Activity name">
          <button class="btn btn--danger btn--sm remove-act-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="sub-section">
          <label>Ingredients</label>
          <div class="tag-box ing-box">
            <input type="text" class="tag-input ing-input" placeholder="Add ingredient…">
          </div>
          <div class="hint">Press <strong>Enter</strong> or <strong>,</strong> to add</div>
        </div>
        <div class="sub-section">
          <label>Steps</label>
          <ol class="steps-list"></ol>
          <div class="add-step-row">
            <input type="text" class="step-new-input" placeholder="Describe this step…">
            <button class="btn btn--ghost btn--sm add-step-btn"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
       `;

	actContainer.appendChild(card);

	// activity name
	const nameIn = card.querySelector(".act-name");

	nameIn.addEventListener("input", () => {
	    act.name = nameIn.value;
	    renderJSON();
	});

	// remove activity
	card.querySelector(".remove-act-btn").addEventListener("click", () => {
            activities.splice(ai, 1);
            renderActivities();
	});

	// ingredients tag box
	const ingBox = card.querySelector(".ing-box");
	const ingInput = card.querySelector(".ing-input");
	const renderIngTags = initTagBox(
            ingBox, ingInput,
            () => act.ingredients,
            l  => { act.ingredients = l; },
            "tag--ing"
	);

	renderIngTags();

	// steps
	const stepsList = card.querySelector(".steps-list");
	const stepNewInput = card.querySelector(".step-new-input");
	const addStepBtn = card.querySelector(".add-step-btn");

	function renderSteps () {
            stepsList.innerHTML = "";

            act.steps.forEach((step, si) => {
		const li = document.createElement("li");
		li.className = "step-item";

		li.innerHTML = `
            <span class="step-num">${si + 1}</span>
            <textarea rows="1">${esc(step)}</textarea>
            <button class="btn btn--danger btn--sm">×</button>
               `;

		stepsList.appendChild(li);

		const ta = li.querySelector("textarea");

		ta.addEventListener("input", () => {
		    act.steps[si] = ta.value;
		    renderJSON();
		});

		// auto-resize
		ta.style.height = "auto";
		ta.style.height = ta.scrollHeight + "px";

		ta.addEventListener("input", () => {
		    ta.style.height = "auto";
		    ta.style.height = ta.scrollHeight + "px";
		});

		li.querySelector(".btn--danger").addEventListener("click", () => {
		    act.steps.splice(si, 1);
		    renderSteps();
		    renderJSON();
		});
            });

            renderJSON();
	}

	function addStep () {
            const v = stepNewInput.value.trim();

            if (!v) return;

            act.steps.push(v);
            stepNewInput.value = "";
            renderSteps();
            stepNewInput.focus();
	}

	addStepBtn.addEventListener("click", addStep);

	stepNewInput.addEventListener("keydown", e => {
	    if (e.key === "Enter") {
		e.preventDefault(); addStep();
	    }
	});

	renderSteps();
    });

    renderJSON();
}

addActBtn.addEventListener("click", () => {
    activities.push({ name: "", ingredients: [], steps: [] });
    renderActivities();

    // focus the new card's name input
    const cards = actContainer.querySelectorAll(".activity-card");
    cards[cards.length - 1].querySelector(".act-name").focus();
});


// ── copy JSON ──

copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(jsonOut.textContent).then(() => {
	copyBtn.textContent = "Copied!";
	copyBtn.classList.add("copied");

	setTimeout(() => {
	    copyBtn.textContent = "Copy";
	    copyBtn.classList.remove("copied");
	}, 1500);
    });
});


// ── global change listeners ──

title_input.addEventListener("input", renderJSON);
source_input.addEventListener("input", renderJSON);


// initialize the DOM

renderJSON();
