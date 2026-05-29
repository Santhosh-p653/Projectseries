import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DB_NAME = "economy_index.db"

# -------------------------------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT NOT NULL,
            price REAL NOT NULL,
            location TEXT NOT NULL,
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------------------------------------------------
# FRONTEND HTML/CSS/JS (Updated with Short Routes)
# -------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoPulse // Local Price Index</title>
    <style>
        :root {
            --bg: #f8fafc;
            --panel: #ffffff;
            --text: #0f172a;
            --primary: #10b981;
            --primary-hover: #059669;
            --border: #e2e8f0;
            --danger: #ef4444;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 2rem;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        header { margin-bottom: 2rem; border-bottom: 2px solid var(--text); padding-bottom: 1rem; }
        header h1 { margin: 0; font-size: 2rem; font-weight: 800; }
        header p { margin: 0.5rem 0 0 0; color: #64748b; }
        .layout { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; }
        @media (max-width: 768px) { .layout { grid-template-columns: 1fr; } }
        .card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; }
        h2 { margin-top: 0; font-size: 1.25rem; margin-bottom: 1rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 600; }
        input { width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
        button { width: 100%; background: var(--text); color: white; border: none; padding: 0.75rem; border-radius: 4px; font-weight: 600; cursor: pointer; }
        button:hover { background: #334155; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 0.75rem; border-bottom: 1px solid var(--border); }
        th { background: #f1f5f9; font-size: 0.875rem; }
        .btn-sm { padding: 0.25rem 0.5rem; font-size: 0.75rem; width: auto; display: inline-block; margin-right: 0.25rem; }
        .btn-danger { background: var(--danger); }
        .btn-danger:hover { background: #dc2626; }
        .btn-update { background: var(--primary); }
        .btn-update:hover { background: var(--primary-hover); }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>EcoPulse Index API</h1>
        <p>A streamlined tracker for hyper-local pricing metrics using short REST routes.</p>
    </header>

    <div class="layout">
        <div class="card">
            <h2 id="form-title">Log Price Point</h2>
            <form id="economyForm">
                <input type="hidden" id="entry-id">
                <div class="form-group">
                    <label for="commodity">Commodity</label>
                    <input type="text" id="commodity" placeholder="e.g., Gas, Coffee" required>
                </div>
                <div class="form-group">
                    <label for="price">Price (USD)</label>
                    <input type="number" step="0.01" id="price" placeholder="e.g., 3.80" required>
                </div>
                <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" id="location" placeholder="e.g., Boston, MA" required>
                </div>
                <button type="submit" id="submit-btn">Submit Price</button>
                <button type="button" id="cancel-btn" style="display:none; background:#94a3b8; margin-top:0.5rem;">Cancel</button>
            </form>
        </div>

        <div class="card">
            <h2>Current Price Index</h2>
            <table>
                <thead>
                    <tr>
                        <th>Commodity</th>
                        <th>Price</th>
                        <th>Location</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="ledger-body"></tbody>
            </table>
        </div>
    </div>
</div>

<script>
    const form = document.getElementById('economyForm');
    const ledgerBody = document.getElementById('ledger-body');
    const submitBtn = document.getElementById('submit-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const entryIdInput = document.getElementById('entry-id');

    document.addEventListener('DOMContentLoaded', fetchPrices);

    // 1. READ - GET /api/prices
    async function fetchPrices() {
        const response = await fetch('/api/prices');
        const data = await response.json();
        
        ledgerBody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${item.commodity}</strong></td>
                <td>$${item.price.toFixed(2)}</td>
                <td><small>${item.location}</small></td>
                <td>
                    <button class="btn-sm btn-update" onclick="prepareUpdate(${item.id}, '${item.commodity}', ${item.price}, '${item.location}')">Edit</button>
                    <button class="btn-sm btn-danger" onclick="deletePrice(${item.id})">Delete</button>
                </td>
            `;
            ledgerBody.appendChild(row);
        });
    }

    // Handle Form Submit (CREATE / UPDATE)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = entryIdInput.value;
        const payload = {
            commodity: document.getElementById('commodity').value,
            price: parseFloat(document.getElementById('price').value),
            location: document.getElementById('location').value
        };

        if (id) {
            // 3. UPDATE - PUT /api/prices/<id>
            await fetch(`/api/prices/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            // 2. CREATE - POST /api/prices
            await fetch('/api/prices', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        resetForm();
        fetchPrices();
    });

    function prepareUpdate(id, commodity, price, location) {
        document.getElementById('form-title').innerText = "Update Entry";
        entryIdInput.value = id;
        document.getElementById('commodity').value = commodity;
        document.getElementById('price').value = price;
        document.getElementById('location').value = location;
        submitBtn.innerText = "Save Changes";
        cancelBtn.style.display = "block";
    }

    // 4. DELETE - DELETE /api/prices/<id>
    async function deletePrice(id) {
        if(confirm("Remove this entry?")) {
            await fetch(`/api/prices/${id}`, { method: 'DELETE' });
            fetchPrices();
        }
    }

    cancelBtn.addEventListener('click', resetForm);

    function resetForm() {
        document.getElementById('form-title').innerText = "Log Price Point";
        entryIdInput.value = '';
        form.reset();
        submitBtn.innerText = "Submit Price";
        cancelBtn.style.display = "none";
    }
</script>
</body>
</html>
"""

# -------------------------------------------------------------------------
# REFACTORED CLEAN FLASK API ROUTES
# -------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/prices', methods=['GET'])
def get_prices():
    """ROUTE 1: GET all prices"""
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM market_index ORDER BY reported_at DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200


@app.route('/api/prices', methods=['POST'])
def add_price():
    """ROUTE 2: POST a new price entry"""
    data = request.get_json()
    if not data or not all(k in data for k in ('commodity', 'price', 'location')):
        return jsonify({"error": "Invalid data format"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO market_index (commodity, price, location) VALUES (?, ?, ?)',
        (data['commodity'], data['price'], data['location'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "status": "Created"}), 201


@app.route('/api/prices/<int:entry_id>', methods=['PUT'])
def update_price(entry_id):
    """ROUTE 3: PUT updates to an existing price entry"""
    data = request.get_json()
    conn = get_db_connection()
    
    item = conn.execute('SELECT * FROM market_index WHERE id = ?', (entry_id,)).fetchone()
    if not item:
        conn.close()
        return jsonify({"error": "Entry not found"}), 404
        
    conn.execute(
        'UPDATE market_index SET commodity = ?, price = ?, location = ? WHERE id = ?',
        (data['commodity'], data['price'], data['location'], entry_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "Updated"}), 200


@app.route('/api/prices/<int:entry_id>', methods=['DELETE'])
def delete_price(entry_id):
    """ROUTE 4: DELETE a price entry"""
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM market_index WHERE id = ?', (entry_id,)).fetchone()
    
    if not item:
        conn.close()
        return jsonify({"error": "Entry not found"}), 404
        
    conn.execute('DELETE FROM market_index WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "Deleted"}), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)