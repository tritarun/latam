from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configure Cloud SQL connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='watchful-pier-422221-q7:us-central1:latam-instance',
            user='dbadmin',
            password='dbadmin1234$',
            database='latam-database'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        return None

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
        query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
        values = (data.get('value1'), data.get('value2'))
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Data created successfully'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to create data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Read operation
@app.route('/api/data', methods=['GET'])
def get_all_data():
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    try:
        cursor.execute("SELECT * FROM your_table")
        data = cursor.fetchall()
        return jsonify({'data': data}), 200
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
        query = "UPDATE your_table SET column1 = %s, column2 = %s WHERE id = %s"
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
        query = "DELETE FROM your_table WHERE id = %s"
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
