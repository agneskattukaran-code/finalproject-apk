import pyodbc
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace the placeholders with your actual Azure SQL details
server = 'server-apk.database.windows.net'
database = 'db-apk'
username = 'adminapk'
password = 'Agnespaul1234' # Use the password you set in the portal
driver = '{ODBC Driver 18 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# --- HTML TEMPLATE (Embedded) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>APK E-Commerce Live Shop</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #0078d4; color: white; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>APK E-Commerce Inventory</h1>
    <p>Status: <strong>Connected to Azure SQL</strong></p>
    <table>
        <tr>
            <th>Product Name</th>
            <th>Price</th>
            <th>Stock</th>
        </tr>
        {table_rows}
    </table>
</body>
</html>
"""

@app.route('/')
def home():
    try:
        # Connect to Database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT ItemName, Price, StockCount FROM Products")
        rows = cursor.fetchall()

        # Build table rows dynamically
        items_html = ""
        for row in rows:
            items_html += f"<tr><td>{row[0]}</td><td>${row[1]}</td><td>{row[2]}</td></tr>"
        
        return HTML_TEMPLATE.format(table_rows=items_html)

    except Exception as e:
        return f"<h1>Connection Error</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    # Run on port 80 so the Load Balancer can find it
    app.run(host='0.0.0.0', port=80)
