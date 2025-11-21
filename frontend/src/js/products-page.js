import { apiClient } from './api.js';
import { formatCurrency, renderStatusBadge, showToast } from './ui-helpers.js';

const tableBody = document.getElementById('product-table-body');
const emptyState = document.getElementById('empty-state');
const filterSelect = document.getElementById('filter-status');
const refreshButton = document.getElementById('refresh-button');

const renderProducts = (products) => {
  tableBody.innerHTML = '';
  if (!products.length) {
    emptyState.classList.remove('hidden');
    return;
  }
  emptyState.classList.add('hidden');

  products.forEach((product) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td class="font-semibold text-slate-800">${product.name}</td>
      <td class="text-slate-500">${product.category_name || '-'}</td>
      <td class="font-medium">${formatCurrency(product.price)}</td>
      <td class="text-slate-600">${product.stock}</td>
      <td>${renderStatusBadge(product.is_active)}</td>
      <td class="space-x-2">
        <a href="./add-product.html?id=${product.id}" class="text-indigo-600 font-semibold">Edit</a>
        <button data-id="${product.id}" data-name="${product.name}" class="text-rose-600 font-semibold deactivate-btn">
          Deactivate
        </button>
      </td>
    `;
    tableBody.appendChild(row);
  });
  bindDeactivateButtons();
};

const fetchAndRender = async () => {
  try {
    const filter = filterSelect.value;
    const params = {};
    if (filter !== 'all') params.is_active = filter === 'active';
    const products = await apiClient.fetchProducts(params);
    renderProducts(products);
  } catch (error) {
    showToast(error.message, 'error');
  }
};

const bindDeactivateButtons = () => {
  document.querySelectorAll('.deactivate-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      const name = btn.dataset.name;
      if (!confirm(`Deactivate ${name}?`)) return;
      try {
        await apiClient.deactivateProduct(id);
        showToast(`${name} deactivated`);
        fetchAndRender();
      } catch (error) {
        showToast(error.message, 'error');
      }
    });
  });
};

filterSelect?.addEventListener('change', fetchAndRender);
refreshButton?.addEventListener('click', fetchAndRender);

document.addEventListener('DOMContentLoaded', fetchAndRender);
