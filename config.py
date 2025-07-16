# Format as Shopify
def format_as_shopify(data):
    pass


# Format as Woocommerce

# Format as plain csv
def format_as_csv(data: list):
    products = []
    for record in data:
        product = {
            "handle": record.get("handle"),
            "title": record.get("title"),
            "body_html": record.get("body_html"),
            "vendor": record.get("vendor"),
            "product_type": record.get("product_type"),
            "tags": ",".join(record.get("tags")),
            "published": record.get("published_at"),
            "images": ",".join(list(map(lambda x: x.get("src"), record.get("images", [])))),
        }
        for idx,option in enumerate(record.get("options", []), start=1):
            product[f'option_{idx}'] = option.get("name")
            product[f'option_{idx}_values'] = ",".join(option.get("values"))

        products.append(product)

    return products