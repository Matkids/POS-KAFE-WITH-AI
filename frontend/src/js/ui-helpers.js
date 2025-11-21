export const formatCurrency = (value = 0) => {
  const numberValue = Number.isNaN(Number(value)) ? 0 : Number(value);
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(
    numberValue,
  );
};

export const renderStatusBadge = (isActive) =>
  `<span class="badge ${isActive ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}">${
    isActive ? 'Active' : 'Inactive'
  }</span>`;

export const showToast = (message, type = 'success') => {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.position = 'fixed';
    container.style.top = '16px';
    container.style.right = '16px';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
  }

  const el = document.createElement('div');
  el.className = `glass-panel shadow-lg px-4 py-3 mb-3 rounded-xl text-sm ${
    type === 'error' ? 'border-rose-200 text-rose-800' : 'border-emerald-200 text-emerald-800'
  }`;
  el.innerText = message;
  container.appendChild(el);

  setTimeout(() => {
    el.remove();
  }, 3000);
};

export const setLoadingState = (button, isLoading, label = 'Loading...') => {
  if (!button) return;
  if (isLoading) {
    button.dataset.originalText = button.innerText;
    button.innerText = label;
    button.setAttribute('disabled', 'true');
    button.classList.add('opacity-70');
  } else {
    const original = button.dataset.originalText;
    if (original) button.innerText = original;
    button.removeAttribute('disabled');
    button.classList.remove('opacity-70');
  }
};
