from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import json
from scrapers.shopify import main
from db import database
import io
import pandas as pd
from config import *

app = Flask(__name__)

@app.route('/shopify', methods=['GET','POST'])
def shopify():
    return render_template('shopify.html')

@app.route('/shopify/scrape', methods=['POST'])
def shopify_scraper():
    db, cursor = database.create_connection(parse=True)

    payload = request.get_json()
    email, store_url = (payload.get("email"), payload.get("storeUrl"))

    # Insert query
    query = "INSERT INTO queries(email,store_url) VALUES(%s,%s)"
    vals = (email, store_url)
    cursor.execute(query, vals)
    db.commit()

    # query id
    query_id = cursor.lastrowid

    # Trigger scraper
    data = main(store_url)

    # Update query products field
    query = "UPDATE queries SET products=%s WHERE id=%s"
    vals = (json.dumps(data), query_id)
    cursor.execute(query, vals)
    db.commit()

    # close connection
    database.close_connection(cursor, db)

    return jsonify({
        "id": query_id,
        "url": store_url[:-1] if store_url.endswith('/') else store_url,
        "products": data.get('products', [])[:10],
        "total": data.get('total', 0)
    })

@app.route('/download/<id>', methods=['GET'])
def download(id: int):
    db, cursor = database.create_connection(parse=True)
    file_format = request.args.get("format")

    query = "SELECT products FROM queries WHERE id=%s"
    vals = (id,)
    cursor.execute(query, vals)
    file_content = cursor.fetchone()
    raw_data = json.loads(file_content.get("products")).get("products", [])
    
    if file_format == "csv":
        print("Data formatted")
        data = format_as_csv(raw_data)

    df = pd.DataFrame(data)
    file_obj = io.BytesIO()
    df.to_csv(file_obj, index=False, encoding="utf-8-sig")
    file_obj.seek(0)

    # close connection
    database.close_connection(cursor, db)
    
    return send_file(
        file_obj,
        as_attachment=True,
        download_name=f"shopify_data_{id}.csv"
    )

app.run(debug=True)