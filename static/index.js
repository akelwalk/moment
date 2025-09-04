// toggling sidebar
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('collapsed');
});

// navigating between pages
function navigate(pageName) {
  window.location.href = pageName;
}

// plotting graph
window.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('journalChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Aug 29', 'Aug 30', 'Aug 31', 'Sep 1', 'Sep 2', 'Sep 3', 'Sep 4'],
      datasets: [{
        label: 'Number of Entries',
        data: [2, 0, 1, 1, 4, 2, 0],
        backgroundColor: '#000',
        barThickness: 12
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Journal Entries (Last 7 Days)' }
      },
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Entries' } },
        x: { title: { display: true, text: 'Date' } }
      }
    }
  });
});
