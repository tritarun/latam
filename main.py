from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Configure Cloud SQL connection
def connect_to_database():
    try:
        unix_socket = '/cloudsql/{}'.format(os.environ.get('CLOUD_SQL_CONNECTION_NAME'))
        conn = mysql.connector.connect(user=os.environ.get('DB_USER'),
                                       password=os.environ.get('DB_PASSWORD'),
                                       unix_socket=unix_socket,
                                       database=os.environ.get('DB_NAME'))
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
# Load configuration from environment variables
app.config['CLOUD_SQL_CONNECTION_NAME'] = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
app.config['DB_USER'] = os.environ.get('DB_USER')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['DB_NAME'] = os.environ.get('DB_NAME')


# Create a cursor object
def get_cursor(conn):
    if conn:
        return conn.cursor()

# Define API endpoints for CRUD operations

# Create operation
@app.route('/api/data', methods=['POST'])
def create_data():
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        tema_nombre = data.get('nombre')
        if not tema_nombre:
            return jsonify({'error': 'Missing field "nombre"'}), 400
        
        query = "INSERT INTO tema (nombre) VALUES (%s)"
        cursor.execute(query, (tema_nombre,))
        conn.commit()
        return jsonify({'message': 'Tema created successfully'}), 201
    except Error as e:
        conn.rollback()
        print(e)
        return jsonify({'error': 'Failed to create data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Read operation for specific ID
@app.route('/api/data/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    try:
        query = "SELECT * FROM tema WHERE id = %s"
        cursor.execute(query, (data_id,))
        data = cursor.fetchone()  # Fetches only one record
        if data:
            return jsonify({'data': data}), 200
        else:
            return jsonify({'message': 'No data found with provided ID'}), 404
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
            
# Update operation
@app.route('/api/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        query = "UPDATE tema SET column1 = %s, column2 = %s WHERE id = %s"
        values = (data.get('value1'), data.get('value2'), data_id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Data updated successfully'}), 200
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to update data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Delete operation
@app.route('/api/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    try:
        query = "DELETE FROM tema WHERE id = %s"
        cursor.execute(query, (data_id,))
        conn.commit()
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to delete data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)