import psycopg2

# Update the connection string with the appropriate host and port
conn = psycopg2.connect(
    dbname="backend_core",
    user="postgres",
    password="changethis",
    host="localhost",  # Use 'localhost' if connecting to port 5433 from host, otherwise 'postgres' in Docker
    port=5433,  # Use 5432 if connecting within Docker network
)
print(conn)
