interface OrderPayload {
    client_id: string;
    items: Array<{
        product_id: string;
        quantity: number;
    }>;
}

interface OrderItemResponse {
    product_id: string;
    quantity: number;
}

interface OrderResponse {
    id: string;
    client_id: string;
    total_amount: string;
    items: OrderItemResponse[];
}

async function submitOrder(): Promise<void> {
    const clientSelect = document.getElementById('clientSelect') as HTMLSelectElement;
    const productSelect = document.getElementById('productSelect') as HTMLSelectElement;
    const quantityInput = document.getElementById('quantity') as HTMLInputElement;

    const clientId = clientSelect.value;
    const productId = productSelect.value;
    const quantity = parseInt(quantityInput.value, 10);

    if (!clientId || !productId) {
        alert("Please select client and product");
        return;
    }

    const payload: OrderPayload = {
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
        const checkClient = document.getElementById('checkClient') as HTMLSelectElement;
        if (checkClient.value === clientId) {
            loadOrders();
        }
    } else {
        alert("Failed to create order");
    }
}

async function loadOrders(): Promise<void> {
    const checkClient = document.getElementById('checkClient') as HTMLSelectElement;
    const container = document.getElementById('ordersList');
    if (!container) return;

    container.innerHTML = '';

    const clientId = checkClient.value;
    if (!clientId) return;

    const response = await fetch(`/api/orders/client/${clientId}`);
    if (response.ok) {
        const orders: OrderResponse[] = await response.json();

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
(window as any).submitOrder = submitOrder;
(window as any).loadOrders = loadOrders;
