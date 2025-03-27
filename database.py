# import mysql.connector

# # Kết nối MySQL
# conn = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='password',
#     database='your_database_name'
# )

# # Tạo bảng users
# conn.cursor().execute('''CREATE TABLE users 
#     (userId INT AUTO_INCREMENT PRIMARY KEY, 
#     password TEXT,
#     email TEXT,
#     firstName TEXT,
#     lastName TEXT,
#     address1 TEXT,
#     address2 TEXT,
#     zipcode TEXT,
#     city TEXT,
#     state TEXT,
#     country TEXT, 
#     phone TEXT)''')

# # Tạo bảng categories
# conn.cursor().execute('''CREATE TABLE categories
#     (categoryId INT AUTO_INCREMENT PRIMARY KEY,
#     name TEXT)''')

# # Tạo bảng products
# conn.cursor().execute('''CREATE TABLE products
#     (productId INT AUTO_INCREMENT PRIMARY KEY,
#     name TEXT,
#     price DECIMAL(10, 2),
#     description TEXT,
#     image TEXT,
#     stock INT,
#     categoryId INT,
#     FOREIGN KEY (categoryId) REFERENCES categories(categoryId))''')

# # Tạo bảng kart
# conn.cursor().execute('''CREATE TABLE kart
#     (userId INT,
#     productId INT,
#     FOREIGN KEY (userId) REFERENCES users(userId),
#     FOREIGN KEY (productId) REFERENCES products(productId))''')

# conn.commit()
# conn.close()



import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT
		)''')


conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''CREATE TABLE kart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')





# conn.close()


