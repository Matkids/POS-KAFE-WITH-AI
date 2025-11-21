import { apiClient } from './api.js';
import { formatCurrency, showToast } from './ui-helpers.js';

const form = document.getElementById('ai-form');
const instructionInput = document.getElementById('instruction');
const insertedList = document.getElementById('inserted-list');
const failedList = document.getElementById('failed-list');
const logsContainer = document.getElementById('logs-container');
const logsList = document.getElementById('logs-list');

const renderResults = (items, container, isSuccess) => {
  container.innerHTML = '';
  if (!items.length) {
    container.innerHTML = '<p class="text-slate-500 text-sm">No items.</p>';
    return;
  }
  items.forEach((item) => {
    const el = document.createElement('div');
    el.className = `flex justify-between items-center px-3 py-2 rounded-lg mb-2 ${
      isSuccess ? 'bg-emerald-50 text-emerald-800' : 'bg-rose-50 text-rose-800'
    }`;
    el.innerHTML = isSuccess
      ? `<span class="font-semibold">${item.name}</span><span>${formatCurrency(item.price)}</span>`
      : `<span class="font-semibold">${item.name || 'Unknown'}</span><span class="text-xs">${item.reason}</span>`;
    container.appendChild(el);
  });
};

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    const payload = instructionInput.value.trim();
    if (!payload) return showToast('Instruction cannot be empty', 'error');
    const result = await apiClient.submitAIInstruction(payload);
    renderResults(result.inserted, insertedList, true);
    renderResults(result.failed, failedList, false);
    showToast('AI processed your instruction');
    await loadLogs();
  } catch (error) {
    showToast(error.message, 'error');
  }
});

const loadLogs = async () => {
  if (!logsList) return;
  try {
    const logs = await apiClient.fetchAiLogs();
    logsContainer.classList.remove('hidden');
    logsList.innerHTML = '';
    logs.slice(0, 5).forEach((log) => {
      const el = document.createElement('div');
      el.className = 'glass-panel px-3 py-2 mb-2';
      el.innerHTML = `
        <div class="text-xs text-slate-500">${new Date(log.created_at).toLocaleString()}</div>
        <div class="font-semibold text-slate-800">${log.raw_instruction}</div>
        <div class="text-xs mt-1">Status: <span class="font-semibold">${log.status}</span></div>
      `;
      logsList.appendChild(el);
    });
  } catch (error) {
    // optional logging only
  }
};

document.addEventListener('DOMContentLoaded', loadLogs);
