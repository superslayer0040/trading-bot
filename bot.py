from flask import Flask, request, jsonify
import os
import ccxt
import re

app = Flask(__name__)

# Configure Exchange API using environment variables
exchange = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('SECRET_KEY')
})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid data"}), 400

    message = data['message']
    
    # Extract data from the message using regex
    match = re.search(r'order (buy|sell) @ (\d+(\.\d+)?) filled on (\w+). New strategy position is (-?\d+(\.\d+)?)', message)
    if not match:
        return jsonify({"error": "Invalid message format"}), 400

    side = match.group(1)
    quantity = match.group(2)
    symbol = match.group(4)
    new_position = match.group(5)

    # Set order_type to 'market' as per the example
    order_type = 'market'

    try:
        # Ensure quantity and new_position are floats
        quantity = float(quantity)
        new_position = float(new_position)
        
        # Validate side and order_type
        if side not in ['buy', 'sell']:
            return jsonify({"error": "Invalid side"}), 400
        if order_type not in ['market', 'limit']:
            return jsonify({"error": "Invalid order type"}), 400

        order = exchange.create_order(symbol, order_type, side, quantity)
        return jsonify({"success": True, "order_id": order['id'], "new_position": new_position}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)