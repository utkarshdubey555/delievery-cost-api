from flask import Flask, request, jsonify
from config import Config
from models import db, Warehouse, Product, WarehouseProduct
from utils import calculate_min_cost

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def setup():
    db.create_all()
    if not Warehouse.query.first():
        warehouses = [
            Warehouse(name='C1', distance_to_L1=10),
            Warehouse(name='C2', distance_to_L1=20),
            Warehouse(name='C3', distance_to_L1=30)
        ]
        products = [Product(name=p) for p in "ABCDEFGHI"]
        db.session.add_all(warehouses + products)
        db.session.commit()

        warehouse_map = {
            'C1': "ABFHGI",
            'C2': "BCDEGI",
            'C3': "CEFGHI"
        }
        for w in warehouses:
            for p in warehouse_map[w.name]:
                product = Product.query.filter_by(name=p).first()
                db.session.add(WarehouseProduct(warehouse_id=w.id, product_id=product.id))
        db.session.commit()

    return "Setup complete!"

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    try:
        order_data = request.get_json()
        cost = calculate_min_cost(order_data, db)
        return jsonify({"minimum_cost": cost})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
