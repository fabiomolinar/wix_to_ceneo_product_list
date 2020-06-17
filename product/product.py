class Product:
    def __init__(self, data):
        """An instance is created from a dictionary
        which contains the field names and values 
        from one row of the .csv file.

        Variable names below will follow javascript
        convetions to facilitate mapping the Object
        attributes to the data on the .csv file.

        Args:
            data (dict): data on the products fields
        """
        # Constants
        self.image_url_prefix = "https://static.wixstatic.com/media/"
        # Attributes from .csv file
        self.handleId = self.process_input(data, "handleId")
        self.fieldType = self.process_input(data, "fieldType")
        self.name = self.process_input(data, "name")
        self.description = self.process_input(data, "description")
        self.productImageUrl = self.process_input(data, "productImageUrl", "not_formated_url_list")
        self.collection = self.process_input(data, "collection", "list")
        self.sku = self.process_input(data, "sku")
        self.ribbon = self.process_input(data, "ribbon")
        self.price = self.process_input(data, "price", "price")
        self.surcharge = self.process_input(data, "surcharge")
        self.visible = self.process_input(data, "visible", "bool")
        self.discountMode = self.process_input(data, "discountMode")
        self.discountValue = self.process_input(data, "discountValue")
        self.inventory = self.process_input(data, "inventory")
        self.weight = self.process_input(data, "weight")

    def process_input(self, data, key, type = None):
        """Check if key exists; return empty string if not.
        This method also formats the data coming from the .csv
        file to a more friendly format. Data treatment depends
        on the <type> attribute.
        """
        if key in data.keys():
            if (data[key] == "" and type != "bool"):
                return ""
            if type == "not_formated_url_list":
                # Exported file don't add the URL prefix. Need to add manually.
                images_list = data[key].split(";")
                for index, image in enumerate(images_list):
                    images_list[index] = self.image_url_prefix + image
                return images_list
            elif type == "list":
                # Standard string list
                return data[key].split(";")
            elif type == "bool":
                return data[key] == "true"
            elif type == "price":
                return "%.2f" % float(data[key])
            else:
                # Just the standard string type
                return data[key]
        else:
            return ""
