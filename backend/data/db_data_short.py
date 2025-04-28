db_summary = (
    "The database has 4 tables: users, products, orders, and orders_content.\n"
    "Relationships:\n"
    "- Each order belongs to one user (user_id).\n"
    "- Each order has multiple orders_content entries.\n"
    "- Each orders_content links to one product (product_id).\n\n"
    "Tables overview:\n"
    "- users: user_id (PK), first_name, last_name, age (non-negative), registration_date\n"
    "- products: product_id (PK), product_name, product_desc, price\n"
    "- orders: order_id (PK), user_id (FK), date\n"
    "- orders_content: orders_content_id (PK), order_id (FK), product_id (FK), units"
)
