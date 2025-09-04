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

// dummy data simulating DB response
const entries = [
  {
    entry_id: 1,
    title: "Gratitude Walk",
    prompt: "Describe one moment today that made you feel truly grateful.",
    content: "I enjoyed a quiet walk in the park...",
    date_posted: "2025-09-02",
    sentiments: "Positive"
  },
  {
    entry_id: 2,
    title: "Challenging Day",
    prompt: "Write about a challenge you overcame.",
    content: "Work was stressful but I managed to push through...",
    date_posted: "2025-09-01",
    sentiments: "Mixed"
  }
];

// populate table with entries
const entriesTableBody = document.getElementById("entriesTableBody");

function renderEntries(data) {
  entriesTableBody.innerHTML = "";
  data.forEach(entry => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${entry.entry_id}</td>
      <td>${entry.title}</td>
      <td>${entry.prompt}</td>
      <td>${entry.sentiments}</td>
      <td>${entry.date_posted}</td>
    `;
    row.addEventListener("click", () => openEntryPopup(entry));

    entriesTableBody.appendChild(row);
  });
}

// initial render
renderEntries(entries);

// search functionality
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");

searchBtn.addEventListener("click", () => {
  const query = searchInput.value.toLowerCase();
  const filtered = entries.filter(e =>
    e.title.toLowerCase().includes(query) ||
    e.prompt.toLowerCase().includes(query) ||
    e.content.toLowerCase().includes(query) ||
    e.sentiments.toLowerCase().includes(query)
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

let currentEntry = null;

function openEntryPopup(entry) {
  currentEntry = entry;
  popupTitle.value = entry.title;
  popupPrompt.value = entry.prompt;
  popupContent.value = entry.content;
  popupSentiment.value = entry.sentiments;

  entryPopupOverlay.style.display = "flex";
}

popupCloseBtn.addEventListener("click", () => {
  entryPopupOverlay.style.display = "none";
});

popupSaveBtn.addEventListener("click", () => {
  if (currentEntry) {
    currentEntry.title = popupTitle.value;
    currentEntry.prompt = popupPrompt.value;
    currentEntry.content = popupContent.value;
    currentEntry.sentiments = popupSentiment.value;
    renderEntries(entries);
  }
  entryPopupOverlay.style.display = "none";
});

