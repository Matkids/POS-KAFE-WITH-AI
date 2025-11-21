import { apiClient } from './api.js';
import { showToast } from './ui-helpers.js';

const form = document.getElementById('product-form');
const heading = document.getElementById('form-heading');
const submitBtn = document.getElementById('submit-btn');
const nameInput = document.getElementById('name');
const categoryInput = document.getElementById('category');
const priceInput = document.getElementById('price');
const stockInput = document.getElementById('stock');
const activeInput = document.getElementById('is_active');

const params = new URLSearchParams(window.location.search);
const productId = params.get('id');

const loadProduct = async () => {
  if (!productId) return;
  heading.innerText = 'Edit Product';
  submitBtn.innerText = 'Update Product';
  try {
    const product = await apiClient.fetchProduct(productId);
    nameInput.value = product.name;
    categoryInput.value = product.category_name || '';
    priceInput.value = product.price;
    stockInput.value = product.stock;
    activeInput.checked = !!product.is_active;
  } catch (error) {
    showToast(error.message, 'error');
  }
};

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    name: nameInput.value,
    category_name: categoryInput.value,
    price: priceInput.value,
    stock: stockInput.value,
    is_active: activeInput.checked,
  };

  try {
    if (productId) {
      await apiClient.updateProduct(productId, payload);
      showToast('Product updated');
    } else {
      await apiClient.createProduct(payload);
      showToast('Product created');
    }
    setTimeout(() => (window.location.href = './products.html'), 350);
  } catch (error) {
    showToast(error.message, 'error');
  }
});

document.addEventListener('DOMContentLoaded', loadProduct);
