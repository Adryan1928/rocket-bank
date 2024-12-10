import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get the payment with ID 11
payment_id = 11
cursor.execute("SELECT id, date FROM payments_payment WHERE id = ?", (payment_id,))
payment = cursor.fetchone()

if payment:
    # Set the date to yesterday
    yesterday = datetime.now() - timedelta(days=1)
    new_date = yesterday.date()

    # Update the payment date
    cursor.execute("UPDATE payments_payment SET date = ? WHERE id = ?", (new_date, payment_id))
    conn.commit()

    print(f"Payment ID {payment_id} date set to {new_date}")
else:
    print(f"Payment with ID {payment_id} not found")

# Close the connection
conn.close()
