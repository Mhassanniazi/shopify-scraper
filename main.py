from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
from scrapers.shopify import main
from db import database

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

    # Trigger scraper
    data = main(store_url)

    # Update query products field
    query = "UPDATE queries SET products=%s WHERE id=%s"
    vals = (json.dumps(data), cursor.lastrowid)
    cursor.execute(query, vals)
    db.commit()

    return jsonify({
        "URL": store_url[:-1] if store_url.endswith('/') else store_url,
        "products": data.get('products', [])[:10],
        "total": data.get('total', 0),
    })

app.run(debug=True)