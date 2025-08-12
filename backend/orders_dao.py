from datetime import datetime
from sql_connection import get_sql_connection  # Updated to use psycopg2

def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table and get the order_id
    order_query = """
        INSERT INTO orders (customer_name, total, order_datetime)
        VALUES (%s, %s, %s)
        RETURNING order_id
    """
    cursor.execute(order_query, (order['customer_name'], order['grand_total'], datetime.now()))
    order_id = cursor.fetchone()[0]  # fetch the returned ID

    # Insert into order_details table
    order_details_query = """
        INSERT INTO order_details (order_id, product_id, quantity, total_price)
        VALUES (%s, %s, %s, %s)
    """
    order_details_data = [
        (order_id, int(item['product_id']), float(item['quantity']), float(item['total_price']))
        for item in order['order_details']
    ]
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()
    cursor.close()
    return order_id


def get_order_details(connection, order_id):
    cursor = connection.cursor()
    query = """
        SELECT od.order_id, od.quantity, od.total_price,
               p.name, p.price_per_unit
        FROM order_details od
        LEFT JOIN products p ON od.product_id = p.product_id
        WHERE od.order_id = %s
    """
    cursor.execute(query, (order_id,))

    records = []
    for row in cursor.fetchall():
        records.append({
            'order_id': row[0],
            'quantity': row[1],
            'total_price': row[2],
            'product_name': row[3],
            'price_per_unit': row[4]
        })

    cursor.close()
    return records


def get_all_orders(connection):
    cursor = connection.cursor()
    query = "SELECT order_id, customer_name, total, order_datetime FROM orders"
    cursor.execute(query)

    response = []
    for row in cursor.fetchall():
        response.append({
            'order_id': row[0],
            'customer_name': row[1],
            'total': row[2],
            'datetime': row[3],
        })

    cursor.close()

    # Append order details to each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response


if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
