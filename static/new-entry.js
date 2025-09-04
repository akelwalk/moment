const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');
const journalEntry = document.getElementById('journalEntry');
const characterCount = document.getElementById('characterCount');

const generateBtn = document.getElementById('generateBtn');
const popupOverlay = document.getElementById('popupOverlay');
const closeBtn = document.getElementById('closeBtn');
const doneBtn = document.getElementById('doneBtn');
const optionsDropdown = document.getElementById('generatingOptionsDropdown');
const prevEntriesContainer = document.getElementById('prevEntriesContainer');
const ideaInputContainer = document.getElementById('ideaInputContainer');
const ideaInput = document.getElementById('ideaInput');
const prevEntriesList = document.getElementById('prevEntriesList');
const promptInput = document.getElementById('promptInput');
const entryTitle = document.getElementById('entryTitle');
const saveEntryBtn = document.getElementById('saveEntryBtn');


let prevEntries = []; // will hold entry objects fetched from backend
let isLoadingPrompt = false; 

function navigate(pageName) {
  window.location.href = pageName;
}

// populate a <select> with entries (option.value = entry_id, option.text = title)
function populateOptionsFromEntries(selectElement, entriesArray) {
  if (!selectElement) return;
  selectElement.innerHTML = "";
  entriesArray.forEach(ent => {
    const opt = document.createElement('option');
    opt.textContent = ent.title;
    opt.value = String(ent.entry_id); // use id for stable identification
    selectElement.appendChild(opt);
  });
}

// sidebar and character count
if (toggleBtn && sidebar) {
  toggleBtn.addEventListener('click', () => sidebar.classList.toggle('collapsed'));
}

if (journalEntry && characterCount) {
  journalEntry.addEventListener('input', () => {
    const length = journalEntry.value.length;
    characterCount.textContent = `${length} / 5000`;
    updateSaveButtonState(); // keep save button state in sync while typing
  });
}

// save button state and save action
function updateSaveButtonState() {
  // defensively check DOM elements
  const hasPrompt = promptInput && promptInput.value.trim() !== "";
  const hasTitle = entryTitle && entryTitle.value.trim() !== "";
  const hasEntry = journalEntry && journalEntry.value.trim() !== "";

  if (saveEntryBtn) saveEntryBtn.disabled = !(hasPrompt && hasTitle && hasEntry);
}

if (promptInput) promptInput.addEventListener('input', updateSaveButtonState);
if (entryTitle) entryTitle.addEventListener('input', updateSaveButtonState);

async function saveEntry() {
  if (!saveEntryBtn) return;
  saveEntryBtn.disabled = true;

  const data = {
    prompt: promptInput?.value || "",
    title: entryTitle?.value || "",
    content: journalEntry?.value || ""
  };

  try {
    const resp = await fetch("/save_entry", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const payload = await resp.json();
    console.log("Saved:", payload);

    // clear inputs
    if (promptInput) promptInput.value = "";
    if (entryTitle) entryTitle.value = "";
    if (journalEntry) journalEntry.value = "";
    updateSaveButtonState();
  } catch (err) {
    console.error("Error saving entry:", err);
    updateSaveButtonState();
  } finally {
    // ensure the button state is recalculated
    updateSaveButtonState();
  }
}

// expose saveEntry globally
window.saveEntry = saveEntry;

// popup prompt
if (generateBtn && popupOverlay && closeBtn && doneBtn) {
  generateBtn.addEventListener('click', async () => {
    popupOverlay.style.display = 'flex';
    updateDoneButtonState();

    // fetch previous entries only once
    if (prevEntries.length === 0 && prevEntriesList) {
      try {
        const response = await fetch("/display_entries");
        const data = await response.json();
        if (data && data.status === 200 && Array.isArray(data.entries)) {
          prevEntries = data.entries;
          populateOptionsFromEntries(prevEntriesList, prevEntries);
        } else {
          console.warn("Display entries returned unexpected payload:", data);
        }
      } catch (err) {
        console.error("Error fetching previous entries:", err);
      }
    }
  });

  // close popup
  closeBtn.addEventListener('click', () => {
    if (!isLoadingPrompt) popupOverlay.style.display = 'none';
  });

  // close popup when clicking outside card
  popupOverlay.addEventListener('click', (e) => {
    if (!isLoadingPrompt && e.target === popupOverlay) popupOverlay.style.display = 'none';
  });

  // handle dropdown option change
  if (optionsDropdown) {
    optionsDropdown.addEventListener('change', () => {
      if (optionsDropdown.value === "Generate from Previous Entry") {
        if (prevEntriesContainer) prevEntriesContainer.style.display = "block";
        if (ideaInputContainer) ideaInputContainer.style.display = "none";
      } else if (optionsDropdown.value === "Generate from Idea") {
        if (ideaInputContainer) ideaInputContainer.style.display = "block";
        if (prevEntriesContainer) prevEntriesContainer.style.display = "none";
      } else {
        if (prevEntriesContainer) prevEntriesContainer.style.display = "none";
        if (ideaInputContainer) ideaInputContainer.style.display = "none";
      }
      updateDoneButtonState();
    });
  }

  // enable/disable generate button logic
  function updateDoneButtonState() {
    if (!doneBtn) return;
    const option = optionsDropdown?.value || "";

    if (option === "Generate from Idea") {
      doneBtn.disabled = !(ideaInput && ideaInput.value.trim() !== "");
    } else if (option === "Generate from Previous Entry") {
      doneBtn.disabled = !(prevEntriesList && prevEntriesList.value);
    } else {
      doneBtn.disabled = false; // generate random prompt
    }
  }

  if (ideaInput) ideaInput.addEventListener('input', updateDoneButtonState);
  if (prevEntriesList) prevEntriesList.addEventListener('change', updateDoneButtonState);

  // generate prompt on click
  doneBtn.addEventListener('click', async () => {
    const option = optionsDropdown?.value || "";
    let payload = { entry: "" };

    if (option === "Generate from Previous Entry") {
      const selectedId = prevEntriesList?.value;
      const entryObj = prevEntries.find(e => String(e.entry_id) === String(selectedId));
      payload.entry = entryObj ? (entryObj.content || "") : "";
    } else if (option === "Generate from Idea") {
      payload.entry = ideaInput?.value.trim() || "";
    } else {
      payload.entry = ""; // random
    }

    // disable button and show loading
    doneBtn.disabled = true;
    const previousText = doneBtn.textContent;
    doneBtn.textContent = "Loading...";
    isLoadingPrompt = true;

    try {
      const response = await fetch("/generate_prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      if (data && data.status === 200 && data.prompt) {
        // set the main prompt input in the new-entry page
        if (promptInput) promptInput.value = data.prompt;
      } else {
        console.error("Failed to generate prompt:", data);
      }
    } catch (err) {
      console.error("Error generating prompt:", err);
    } finally {
      // restore state
      doneBtn.disabled = false;
      doneBtn.textContent = previousText || "Generate";
      isLoadingPrompt = false;
      if (popupOverlay) popupOverlay.style.display = 'none';
      updateSaveButtonState(); // re-evaluate save button state with new prompt
    }
  });
}

// initial setup state
updateSaveButtonState();
