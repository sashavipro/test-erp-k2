"use strict";
async function submitOrder() {
    const clientSelect = document.getElementById('clientSelect');
    const productSelect = document.getElementById('productSelect');
    const quantityInput = document.getElementById('quantity');
    const clientId = clientSelect.value;
    const productId = productSelect.value;
    const quantity = parseInt(quantityInput.value, 10);
    if (!clientId || !productId) {
        alert("Please select client and product");
        return;
    }
    const payload = {
        client_id: clientId,
        items: [{ product_id: productId, quantity: quantity }]
    };
    const response = await fetch('/api/orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (response.ok) {
        alert("Order created successfully!");
        const checkClient = document.getElementById('checkClient');
        if (checkClient.value === clientId) {
            loadOrders();
        }
    }
    else {
        alert("Failed to create order");
    }
}
async function loadOrders() {
    const checkClient = document.getElementById('checkClient');
    const container = document.getElementById('ordersList');
    if (!container)
        return;
    container.innerHTML = '';
    const clientId = checkClient.value;
    if (!clientId)
        return;
    const response = await fetch(`/api/orders/client/${clientId}`);
    if (response.ok) {
        const orders = await response.json();
        if (orders.length === 0) {
            container.innerHTML = '<p>No orders found.</p>';
            return;
        }
        const ul = document.createElement('ul');
        orders.forEach((order) => {
            const li = document.createElement('li');
            li.textContent = `Order ID: ${order.id} | Total: $${order.total_amount}`;
            ul.appendChild(li);
        });
        container.appendChild(ul);
    }
}
// Make functions available globally so they can be called from inline event handlers
window.submitOrder = submitOrder;
window.loadOrders = loadOrders;
