import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    dbname="120db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Test the connection
print("Connected to the database!")

# Close the connection
conn.close()
