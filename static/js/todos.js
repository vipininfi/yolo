function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function getCSRFToken() {
  // Try cookie first
  const token = getCookie('csrftoken');
  if (token) return token;
  // Fallback to meta tag
  const meta = document.querySelector('meta[name=csrf-token]');
  return meta ? meta.content : '';
}

async function csrfFetch(url, options = {}) {
  options.headers = options.headers || {};
  if (!options.headers['Content-Type']) options.headers['Content-Type'] = 'application/json';
  options.credentials = options.credentials || 'same-origin';
  const token = getCSRFToken();
  if (token) options.headers['X-CSRFToken'] = token;
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

async function bulkToggle(ids) {
  if (!ids || !ids.length) return;
  const confirmed = confirm(`Toggle completion for ${ids.length} todos?`);
  if (!confirmed) return;
  try {
    await csrfFetch('/api/todos/bulk_toggle/', {
      method: 'POST',
      body: JSON.stringify({ ids }),
    });
    // reload to reflect changes
    window.location.reload();
  } catch (err) {
    console.error(err);
    alert('Bulk action failed. Check console for details.');
  }
}

function updateBulkState() {
  const checkboxes = Array.from(document.querySelectorAll('.select-todo'));
  const selected = checkboxes.filter(cb => cb.checked).map(cb => cb.getAttribute('data-id'));
  const btn = document.getElementById('bulk-toggle-btn');
  const countEl = document.getElementById('bulk-selected-count');
  if (countEl) countEl.textContent = String(selected.length);
  if (btn) btn.disabled = selected.length === 0;
  return selected;
}

function markOverdueRows() {
  const rows = document.querySelectorAll('.todo-row');
  const today = new Date();
  rows.forEach(row => {
    const due = row.getAttribute('data-due');
    if (!due) return;
    const dueDate = new Date(due);
    if (isNaN(dueDate)) return;
    if (dueDate < today && !row.classList.contains('todo-overdue')) {
      row.classList.add('todo-overdue');
    }
  });
}

function initTodosPage() {
  // wire select-all
  const selectAll = document.getElementById('select-all');
  if (selectAll) {
    selectAll.addEventListener('change', (e) => {
      const checked = e.target.checked;
      document.querySelectorAll('.select-todo').forEach(cb => { cb.checked = checked; });
      updateBulkState();
    });
  }

  // wire individual checkboxes
  document.querySelectorAll('.select-todo').forEach(cb => {
    cb.addEventListener('change', () => {
      const all = Array.from(document.querySelectorAll('.select-todo'));
      const allChecked = all.length > 0 && all.every(c => c.checked);
      if (selectAll) selectAll.checked = allChecked;
      updateBulkState();
    });
  });

  // bulk button
  const bulkBtn = document.getElementById('bulk-toggle-btn');
  if (bulkBtn) {
    bulkBtn.addEventListener('click', () => {
      const selected = updateBulkState();
      const ids = selected.map(id => Number(id));
      bulkToggle(ids);
    });
  }

  // mark overdue
  markOverdueRows();
}

// expose for debugging
window.initTodosPage = initTodosPage;
window.bulkToggle = bulkToggle;