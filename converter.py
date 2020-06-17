import os
import csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from product.product import Product
from settings import settings

def name_to_slug(name):
    """Fucking .csv export file don't contain slugs.
    Will try to guess it.
    """
    return name.lower().replace(" ", "-")

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8")

def filter_out(product, filters):
    for filter_key in filters.keys():
        if hasattr(product, filter_key):
            for filter in filters[filter_key]:
                try:
                    value = getattr(product, filter_key)
                    if value == filter:
                        return True
                except AttributeError:
                    pass                
    return False

def add_cdata(text):
    return "<![CDATA[" + text + "]]>"

def run():
    products = []
    # Standard .csv file name
    standard_input_file_name = "catalog_products.csv"
    standard_output_file_name = "catalog_products.xml"
    input_file = os.path.join(os.getcwd(), "input", standard_input_file_name)
    output_file = os.path.join(os.getcwd(), "output", standard_output_file_name)
    if not os.path.isfile(input_file):
        print("No input file found.")
        return
    # Create list of products
    with open(input_file, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            products.append(Product(line))
    # Create XML
    # Top element
    offers = Element("offers")    
    offers.set("version", "1")
    offers.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    # Create products
    for product in products:
        if filter_out(product, settings["filters"]): continue
        o = SubElement(offers, "o")
        o.set("id", product.handleId)
        o.set("url", settings["product_page_url_prefix"] + name_to_slug(product.name))
        o.set("price", product.price)
        o.set("avail", "14")
        o.set("stock", product.inventory)
        cat = SubElement(o, "cat")
        cat.text = add_cdata(settings["category"])
        name = SubElement(o, "name")
        name.text = add_cdata(product.name)
        imgs = SubElement(o, "imgs")
        for index, image in enumerate(product.productImageUrl):
            if index == 0:
                main = SubElement(imgs, "main")
                main.set("url", image)
            else:
                i = SubElement(imgs, "i")
                i.set("url", image)
        desc = SubElement(o, "desc")
        desc.text = add_cdata(product.description)

    with open(output_file, "w+") as file:
        content = prettify(offers).decode("utf-8")
        # Add brackets
        content = content.replace("&lt;", "<")
        content = content.replace("&gt;", ">")
        content = content.replace("&amp;", "&")        
        # Write
        file.write(content)

if __name__ == "__main__":
    print("Converter started.")
    run()
    print("Converter finished.")