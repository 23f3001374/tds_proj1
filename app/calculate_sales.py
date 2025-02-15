import sqlite3

db_path = "/data/ticket-sales.db"
output_file = "/data/ticket-sales-gold.txt"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0]

    with open(output_file, "w") as f:
        f.write(str(total_sales))

    print(f"Total sales for Gold tickets: {total_sales}")

    conn.close()

except Exception as e:
    print(f"Error calculating sales: {e}")
