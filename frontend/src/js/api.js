const BASE_URL = window.API_BASE_URL || 'http://localhost:8000/api';

const request = async (path, options = {}) => {
  const resp = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await resp.text();
  const data = text ? JSON.parse(text) : null;
  if (!resp.ok) {
    const message = data?.detail || data?.error || resp.statusText;
    throw new Error(message);
  }
  return data;
};

const fetchProducts = (params = {}) => {
  const searchParams = new URLSearchParams(params);
  const query = searchParams.toString();
  return request(`/products/${query ? `?${query}` : ''}`);
};
const fetchProduct = (id) => request(`/products/${id}/`);
const createProduct = (payload) => request('/products/', { method: 'POST', body: JSON.stringify(payload) });
const updateProduct = (id, payload, partial = false) =>
  request(`/products/${id}/`, { method: partial ? 'PATCH' : 'PUT', body: JSON.stringify(payload) });
const submitAIInstruction = (instruction) =>
  request('/ai/add-products/', { method: 'POST', body: JSON.stringify({ instruction }) });
const fetchAiLogs = () => request('/ai/logs/');
const deactivateProduct = (id) => updateProduct(id, { is_active: false }, true);

export const apiClient = {
  fetchProducts,
  fetchProduct,
  createProduct,
  updateProduct,
  deactivateProduct,
  submitAIInstruction,
  fetchAiLogs,
};
