// toggling sidebar
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');

if (toggleBtn) {
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
  });
}

// navigation between pages
function navigate(pageName) {
  window.location.href = pageName;
}

const entriesTableBody = document.getElementById("entriesTableBody");
let entries = [];

// fetch entries data from fast api
function fetchEntries() {
  fetch("/display_entries")
    .then(response => response.json())
    .then(data => {
      if (data.status === 200) {
        entries = data.entries;
        renderEntries(entries);
      } else {
        console.error("Failed to fetch entries:", data);
      }
    })
    .catch(err => console.error("Error fetching entries:", err));
}

// initial fetch
fetchEntries();

// populate table with entries
function renderEntries(data) {
  entriesTableBody.innerHTML = "";
  data.forEach(entry => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${entry.entry_id}</td>
      <td>${entry.title}</td>
      <td>${entry.prompt}</td>
      <td>${entry.sentiment}</td>
      <td>${entry.date_posted}</td>
    `;
    row.addEventListener("click", () => openEntryPopup(entry));

    entriesTableBody.appendChild(row);
  });
}

// search functionality
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");

searchBtn.addEventListener("click", () => {
  const query = searchInput.value.toLowerCase();
  const filtered = entries.filter(e =>
    e.title.toLowerCase().includes(query) ||
    e.prompt.toLowerCase().includes(query) ||
    e.content.toLowerCase().includes(query) ||
    e.sentiment.toLowerCase().includes(query)
  );
  renderEntries(filtered);
});

// viewing entry in popup
const entryPopupOverlay = document.getElementById("entryPopupOverlay");
const popupTitle = document.getElementById("popupTitle");
const popupPrompt = document.getElementById("popupPrompt");
const popupContent = document.getElementById("popupContent");
const popupSentiment = document.getElementById("popupSentiment");

const popupCloseBtn = document.getElementById("popupCloseBtn");
const popupSaveBtn = document.getElementById("popupSaveBtn");
const popupDeleteBtn = document.getElementById("popupDeleteBtn");

let currentEntry = null;

function openEntryPopup(entry) {
  currentEntry = entry;
  popupTitle.value = entry.title;
  popupPrompt.value = entry.prompt;
  popupContent.value = entry.content;
  popupSentiment.value = entry.sentiment;

  entryPopupOverlay.style.display = "flex";
}

// close button functionality
popupCloseBtn.addEventListener("click", () => {
  entryPopupOverlay.style.display = "none";
});

// close popup when clicking outside of popup-card
entryPopupOverlay.addEventListener("click", (e) => {
  if (e.target === entryPopupOverlay) {
    entryPopupOverlay.style.display = "none";
  }
});

// eelete button functionality
popupDeleteBtn.addEventListener("click", () => {
  if (currentEntry) {
    const index = entries.findIndex(e => e.entry_id === currentEntry.entry_id);
    if (index !== -1) {
      entries.splice(index, 1); // remove from array
      renderEntries(entries);
      currentEntry = null;
    }
  }
  entryPopupOverlay.style.display = "none";
});


// save button functionality
popupSaveBtn.addEventListener("click", () => {
  if (currentEntry) {
    currentEntry.title = popupTitle.value;
    currentEntry.prompt = popupPrompt.value;
    currentEntry.content = popupContent.value;
    currentEntry.sentiment = popupSentiment.value;
    renderEntries(entries);
  }
  entryPopupOverlay.style.display = "none";
});

