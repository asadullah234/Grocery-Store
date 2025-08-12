from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = """
        SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name
        FROM products
        INNER JOIN uom ON products.uom_id = uom.uom_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    response = []
    for row in rows:
        product_id, name, uom_id, price_per_unit, uom_name = row
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    return response


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = """
        INSERT INTO products (name, uom_id, price_per_unit)
        VALUES (%s, %s, %s)
        RETURNING product_id
    """
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    cursor.execute(query, data)
    product_id = cursor.fetchone()[0]  # Get the inserted ID
    connection.commit()

    return product_id


def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM products WHERE product_id = %s RETURNING product_id"
    cursor.execute(query, (product_id,))
    deleted_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None
    connection.commit()

    return deleted_id


if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': 1,
        'price_per_unit': 10
    }))
