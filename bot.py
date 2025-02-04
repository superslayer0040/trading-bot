from flask import Flask, request, jsonify
import os
import ccxt

app = Flask(__name__)

# Configure Exchange API using environment variables
exchange = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('SECRET_KEY')
})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    symbol = data.get('symbol')
    side = data.get('side')
    order_type = data.get('order_type')
    quantity = data.get('quantity')

    if not symbol or not side or not order_type or not quantity:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        order = exchange.create_order(symbol, order_type, side, float(quantity))
        return jsonify({"success": True, "order_id": order['id']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)