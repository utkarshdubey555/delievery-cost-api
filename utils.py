from models import Warehouse, Product, WarehouseProduct
from collections import defaultdict
import itertools

COST_PER_KG_KM = 2
PRODUCT_WEIGHT_KG = 0.5

def get_warehouse_data(db):
    warehouses = Warehouse.query.all()
    warehouse_info = {w.name: w.distance_to_L1 for w in warehouses}

    product_sources = defaultdict(list)
    for wp in WarehouseProduct.query.all():
        warehouse = Warehouse.query.get(wp.warehouse_id)
        product = Product.query.get(wp.product_id)
        product_sources[product.name].append(warehouse.name)

    return warehouse_info, product_sources

def calculate_min_cost(order_dict, db):
    warehouse_info, product_sources = get_warehouse_data(db)

    centers = list(warehouse_info.keys())
    min_cost = float('inf')

    for start_center in centers:
        route = [start_center]
        remaining_order = dict(order_dict)
        collected = set()
        cost = 0

        while remaining_order:
            for product, qty in list(remaining_order.items()):
                for center in centers:
                    if center not in route:
                        route.append(center)
                    if center in product_sources.get(product, []):
                        weight = qty * PRODUCT_WEIGHT_KG
                        distance = warehouse_info[center]
                        cost += weight * distance * COST_PER_KG_KM
                        collected.add(product)
                        remaining_order.pop(product)
                        break
        min_cost = min(min_cost, cost)

    return int(min_cost)
