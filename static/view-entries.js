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
async function fetchEntries() {
  try {
    const response = await fetch("/display_entries");
    const data = await response.json();
    if (data.status === 200 && Array.isArray(data.entries)) {
      entries = data.entries; // sync local array with backend
      renderEntries(entries);
    } else {
      console.error("Failed to fetch entries:", data);
    }
  } catch (err) {
    console.error("Error fetching entries:", err);
  }
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

searchBtn.addEventListener("click", async () => {
  const query = searchInput.value.trim();
  if (!query) return;

  try {
    const resp = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const payload = await resp.json();
    if (payload.status === 200 && Array.isArray(payload.entries)) {
      entries = payload.entries; // replace local array with backend results
      renderEntries(entries);
    } else {
      console.error("Search failed:", payload);
    }
  } catch (err) {
    console.error("Error searching entries:", err);
  }
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
popupDeleteBtn.addEventListener("click", async () => {
  if (!currentEntry) return;

  try {
    const resp = await fetch(`/entries/${currentEntry.entry_id}`, {
      method: "DELETE"
    });
    const payload = await resp.json();
    if (payload.status === 200) {
      const index = entries.findIndex(e => e.entry_id === currentEntry.entry_id);
      if (index !== -1) entries.splice(index, 1);
      renderEntries(entries);
      currentEntry = null;
      entryPopupOverlay.style.display = "none";
    } else {
      console.error("Failed to delete entry:", payload);
    }
  } catch (err) {
    console.error("Error deleting entry:", err);
  }
});


// save button functionality
popupSaveBtn.addEventListener("click", async () => {
  if (!currentEntry) return;

  const updatedData = {
    entry_id: currentEntry.entry_id,
    title: popupTitle.value,
    prompt: popupPrompt.value,
    content: popupContent.value,
    sentiment: popupSentiment.value
  };

  try {
    const resp = await fetch(`/entries/${currentEntry.entry_id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedData)
    });
    const payload = await resp.json();
    if (payload.status === 200) {
      // update local array
      Object.assign(currentEntry, updatedData);
      renderEntries(entries);
      entryPopupOverlay.style.display = "none";
    } else {
      console.error("Failed to update entry:", payload);
    }
  } catch (err) {
    console.error("Error updating entry:", err);
  }
});
