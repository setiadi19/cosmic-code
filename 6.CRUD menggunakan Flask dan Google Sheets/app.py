from flask import Flask, request, jsonify, make_response
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Konfigurasi Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
CLIENT = gspread.authorize(CREDS)
SHEET_ID = "1Gw8HNpvgUTiuO5zE79k0s2Fjjrs1oO89ydWG8qcBg9s"
SHEET = CLIENT.open_by_key(SHEET_ID).sheet1

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/fetch_data', methods=['GET', 'OPTIONS'])
def fetch_data():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
    values_list = SHEET.get_all_values()[1:]  # Mengabaikan baris pertama
    response = jsonify(values_list)
    return add_cors_headers(response)

@app.route('/create_data', methods=['POST', 'OPTIONS'])
def create_data():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    
    if name and age:
        SHEET.append_row([name, age])
        response = jsonify({"status": "success"})
        return add_cors_headers(response), 200
    response = jsonify({"status": "error"})
    return add_cors_headers(response), 400

@app.route('/edit_data', methods=['POST', 'OPTIONS'])
def edit_data():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
    data = request.get_json()
    old_name = data.get('oldName')
    new_name = data.get('newName')
    new_age = data.get('newAge')
    
    if old_name and new_name and new_age:
        cell = SHEET.find(old_name)
        if cell:
            SHEET.update_cell(cell.row, 1, new_name)
            SHEET.update_cell(cell.row, 2, new_age)
            response = jsonify({"status": "success"})
            return add_cors_headers(response), 200
    response = jsonify({"status": "error"})
    return add_cors_headers(response), 400

@app.route('/delete_data', methods=['POST', 'OPTIONS'])
def delete_data():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
    data = request.get_json()
    name = data.get('name')
    
    if name:
        cell = SHEET.find(name)
        if cell:
            SHEET.delete_rows(cell.row)
            response = jsonify({"status": "success"})
            return add_cors_headers(response), 200
    response = jsonify({"status": "error"})
    return add_cors_headers(response), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
