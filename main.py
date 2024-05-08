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

# Create operation for 'tema' and associated 'mensajes'
@app.route('/api/tema/', methods=['POST'])
def create_tema_with_mensajes():
    data = request.get_json()
    conn = connect_to_database()
    cursor = get_cursor(conn)

    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500

    try:
        # Insert the 'tema'
        tema_query = "INSERT INTO tema (nombre) VALUES (%s)"
        cursor.execute(tema_query, (data['nombre'],))
        tema_id = cursor.lastrowid  # Get the ID of the newly inserted 'tema'

        # Insert the 'mensajes'
        mensajes_query = "INSERT INTO mensajes (tema_id, texto) VALUES (%s, %s)"
        for mensaje in data['mensajes']:
            cursor.execute(mensajes_query, (tema_id, mensaje['texto']))

        conn.commit()
        return jsonify({'message': 'Tema and mensajes created successfully'}), 201
    
    except Error as e:
        conn.rollback()
        print(e)
        return jsonify({'error': 'Failed to create tema and mensajes'}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

# Read operation for 'tema' and associated 'mensajes'
@app.route('/api/tema/', methods=['GET'])
def get_all_temas():
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    try:
        cursor.execute("SELECT * FROM tema")
        temas = cursor.fetchall()
        all_data = []
        for tema in temas:
            cursor.execute("SELECT * FROM mensajes WHERE tema_id = %s", (tema[0],))
            mensajes = cursor.fetchall()
            all_data.append({
                'tema': tema[1],
                'mensajes': [{'id': msg[0], 'texto': msg[2]} for msg in mensajes]
            })
        return jsonify(all_data), 200
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Update operation for 'mensajes' (example for updating a specific message)
@app.route('/api/mensajes/<int:mensaje_id>', methods=['PUT'])
def update_mensaje(mensaje_id):
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        query = "UPDATE mensajes SET texto = %s WHERE id = %s"
        cursor.execute(query, (data.get('texto'), mensaje_id))
        conn.commit()
        return jsonify({'message': 'Mensaje updated successfully'}), 200
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to update mensaje'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Delete operation for 'tema' and associated 'mensajes' (cascade delete)
@app.route('/api/tema/<int:tema_id>', methods=['DELETE'])
def delete_tema(tema_id):
    conn = connect_to_database()
    cursor = get_cursor(conn)
    if not cursor:
        return jsonify({'error': 'Unable to connect to database'}), 500
    
    try:
        query = "DELETE FROM tema WHERE id = %s"
        cursor.execute(query, (tema_id,))
        conn.commit()
        return jsonify({'message': 'Tema and associated mensajes deleted successfully'}), 200
    except Error as e:
        print(e)
        return jsonify({'error': 'Failed to delete tema'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)