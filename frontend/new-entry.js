// toggling sidebar
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');

if (toggleBtn) {
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
  });
}

// navigating between pages
function navigate(pageName) {
  window.location.href = pageName;
}

// updating character count in journal entry
const journalEntry = document.getElementById('journalEntry');
const characterCount = document.getElementById('characterCount');

if (journalEntry) {
  journalEntry.addEventListener('input', () => {
    const length = journalEntry.value.length;
    characterCount.textContent = `${length} / 5000`;
  });
}

// displaying and handling the generate journal prompt popup card
const generateBtn = document.getElementById('generateBtn');
const popupOverlay = document.getElementById('popupOverlay');
const closeBtn = document.getElementById('closeBtn');
const doneBtn = document.getElementById('doneBtn');

generateBtn.addEventListener('click', () => {
  popupOverlay.style.display = 'flex';
  updateDoneButtonState(); // initializing the state of generate button inside popup card
});

closeBtn.addEventListener('click', () => {
  popupOverlay.style.display = 'none';
});

doneBtn.addEventListener('click', () => {
  popupOverlay.style.display = 'none';
  // For now, no additional functionality
});


// add previous journal entry titles to previous entries dropdown
const prevEntriesList = document.getElementById('prevEntriesList');

// example list of titles (placeholder for backend data)
const titles = [
  "yahooo",
  "Entry 2",
  "Entry 3",
  "Entry 4",
  "lmaooo",
  "Entry 6",
  "Entry 7",
  "Entry 8",
  "Entry 9",
  "Entry 10"
];

function populateOptions(selectElement, options) {
  selectElement.innerHTML = ""; // clearing old options
  options.forEach(item => {
    const option = document.createElement("option");
    option.textContent = item;
    option.value = item;
    selectElement.appendChild(option);
  });
}

if (prevEntriesList) {
  populateOptions(prevEntriesList, titles);
}


// handling options for the popup dropdown
const optionsDropdown = document.getElementById('generatingOptionsDropdown');
const prevEntriesContainer = document.getElementById('prevEntriesContainer');
const ideaInputContainer = document.getElementById('ideaInputContainer');

optionsDropdown.addEventListener('change', () => {
  if (optionsDropdown.value === "Generate from Previous Entry") {
    prevEntriesContainer.style.display = "block";
    ideaInputContainer.style.display = "none";

  } else if (optionsDropdown.value === "Generate from Idea") {
    ideaInputContainer.style.display = "block";
    prevEntriesContainer.style.display = "none";

  } else {
    // "Generate Random Prompt"
    prevEntriesContainer.style.display = "none";
    ideaInputContainer.style.display = "none";
  }

  updateDoneButtonState();
});


// enable/disable logic for generate button
const ideaInput = document.getElementById('ideaInput');

function updateDoneButtonState() {
  const selectedOption = optionsDropdown.value;

  if (selectedOption === "Generate from Idea") {
    doneBtn.disabled = ideaInput.value.trim() === "";

  } else if (selectedOption === "Generate from Previous Entry") {
    doneBtn.disabled = !prevEntriesList.value;

  } else {
    // Generate Random Prompt
    doneBtn.disabled = false;
  }
}

// event listeners for input changes
ideaInput.addEventListener('input', updateDoneButtonState);
prevEntriesList.addEventListener('change', updateDoneButtonState);
