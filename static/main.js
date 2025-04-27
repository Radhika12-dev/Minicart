async function createOrder() {
    const customerId = document.getElementById('customer_id').value;
    const productIdsRaw = document.getElementById('product_ids').value;
    const productIds = productIdsRaw.split(',').map(id => parseInt(id.trim()));

    const response = await fetch('/orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_id: parseInt(customerId), product_ids: productIds })
    });

    if (response.ok) {
        alert('Order created!');
    } else {
        const error = await response.json();
        alert('Error: ' + error.detail);
    }
}

async function createProduct() {
    const name = document.getElementById('name').value;
    const price = document.getElementById('price').value;

    const response = await fetch('/products/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price: parseFloat(price) })
    });

    if (response.ok) {
        alert('Product created!');
    } else {
        const error = await response.json();
        alert('Error: ' + error.detail);
    }
}

async function CreateCustomer() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;

    const response = await fetch('/customers/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, phone, address })
    });

    if (response.ok) {
        alert('Customer created successfully!');
    } else {
        const error = await response.json();
        alert('Error: ' + error.detail);
    }
}
