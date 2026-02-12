import psycopg2
from api_request import fetch_data,wmo_weather_codes

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    print("Creating table if not exists...")
    try:
        cursor=conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id serial PRIMARY KEY,
                city TEXT,
                temperature FlOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                timezone TEXT
            )
        """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise



def insert_records(conn, data, weather_codes):
    print("Inserting weather data into the database...")
    try:
        weather = data['weather']
        location = data['location'] 
        cursor=conn.cursor()
        cursor.execute("""
            INSERT INTO dev.raw_weather_data (
                city,
                temperature,
                weather_descriptions,
                wind_speed,
                time,
                inserted_at,
                timezone
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """,(
            location['city'],
            weather['temperature_2m'],
            weather_codes[weather['weather_code']],
            weather['wind_speed_10m'],
            weather['time'],
            data['metadata']['timezone']           
            )
        )
        conn.commit()
        print("Data successfully inserted")

    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")
        raise


def main():
    try:    
        weather_codes = wmo_weather_codes()
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn,data,weather_codes)
    except Exception as e:
        print(f"An error occurred during exception: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

