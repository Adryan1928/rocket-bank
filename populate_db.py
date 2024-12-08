import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create sample users with all required fields
cursor.execute("""
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ('john_doe', 'password123', 'John', 'Doe', 'john@example.com', 0, 1, datetime.now(), 0))
cursor.execute("""
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ('jane_smith', 'password123', 'Jane', 'Smith', 'jane@example.com', 0, 1, datetime.now(), 0))

# Get user IDs
cursor.execute("SELECT id FROM auth_user WHERE username = ?", ('john_doe',))
user1_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM auth_user WHERE username = ?", ('jane_smith',))
user2_id = cursor.fetchone()[0]

# Create sample clients
cursor.execute("INSERT INTO users_client (user_id, phone_number, cpf, birth_date, cash) VALUES (?, ?, ?, ?, ?)", (user1_id, '1234567890', '123.456.789-00', '1990-01-01', 1000.00))
cursor.execute("INSERT INTO users_client (user_id, phone_number, cpf, birth_date, cash) VALUES (?, ?, ?, ?, ?)", (user2_id, '0987654321', '987.654.321-00', '1992-02-02', 2000.00))

# Get client IDs
cursor.execute("SELECT id FROM users_client WHERE user_id = ?", (user1_id,))
client1_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM users_client WHERE user_id = ?", (user2_id,))
client2_id = cursor.fetchone()[0]

# Create sample Pix keys
cursor.execute("INSERT INTO payments_pix (user_id, type, key) VALUES (?, ?, ?)", (client1_id, 'email', 'john@example.com'))
cursor.execute("INSERT INTO payments_pix (user_id, type, key) VALUES (?, ?, ?)", (client2_id, 'phone', '0987654321'))

# Get Pix IDs
cursor.execute("SELECT id FROM payments_pix WHERE user_id = ?", (client1_id,))
pix1_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM payments_pix WHERE user_id = ?", (client2_id,))
pix2_id = cursor.fetchone()[0]

# Create sample payments
cursor.execute("INSERT INTO payments_payment (sender_id, receiver_id, value, date, pix_id) VALUES (?, ?, ?, ?, ?)", (client1_id, client2_id, 150.00, datetime.now().date(), pix1_id))
cursor.execute("INSERT INTO payments_payment (sender_id, receiver_id, value, date, pix_id) VALUES (?, ?, ?, ?, ?)", (client2_id, client1_id, 200.00, (datetime.now() - timedelta(days=1)).date(), pix2_id))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database populated successfully!")
