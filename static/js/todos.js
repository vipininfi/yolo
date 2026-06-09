// Client-side behavior for Todo forms and list filters
(function () {
  'use strict';

  // Due date validation: prevent selecting past dates
  var dueInput = document.getElementById('id_due_date');
  if (dueInput) {
    // set min to today
    var today = new Date();
    var yyyy = today.getFullYear();
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var dd = String(today.getDate()).padStart(2, '0');
    var minDate = yyyy + '-' + mm + '-' + dd;
    try {
      dueInput.setAttribute('min', minDate);
    } catch (e) {
      // ignore
    }

    dueInput.addEventListener('input', function (e) {
      var val = e.target.value;
      if (!val) {
        e.target.setCustomValidity('');
        return;
      }
      var selected = new Date(val + 'T00:00:00');
      var now = new Date();
      // Zero time for today comparison
      now.setHours(0,0,0,0);
      if (selected < now) {
        e.target.setCustomValidity('Due date cannot be in the past.');
        e.target.reportValidity();
      } else {
        e.target.setCustomValidity('');
      }
    });
  }

  // Filters: auto-submit on change
  var filterForm = document.getElementById('todo-filters');
  if (filterForm) {
    filterForm.addEventListener('change', function (e) {
      // submit the form when a filter value changes
      // preserve other query params if present by submitting the form normally
      filterForm.requestSubmit?.();
    });
  }

  // Priority badges: no client-side enhancement needed currently, but expose helper
  window.todosUI = {
    validateDueDateNow: function () {
      if (!dueInput) return true;
      var val = dueInput.value;
      if (!val) return true;
      var selected = new Date(val + 'T00:00:00');
      var now = new Date(); now.setHours(0,0,0,0);
      return selected >= now;
    }
  };
})();
