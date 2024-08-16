
    def store_data(category, jewellery_name, jewellery_price, img_url):
    connection = mysql.connector.connect(
        host='localhost',
        user='root', 
        password='rajatkumar123',  
        database='bluestone'