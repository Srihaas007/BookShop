from flask import Flask
from flask import render_template
import sqlite3 

con = sqlite3.connect('products.db')

con.execute('CREATE TABLE products(id INT unsigned, name VARCHAR(255), code VARCHAR(255), image TEXT, price DOUBLE)')

con.close()  
con = sqlite3.connect('products.db')

con.execute('INSERT INTO products(id, name, code, image, price) VALUES (1, "Anna Karenina", "8919076702111", "product-images/AnnaKarenina.jpg", 50.00),(2, "Beloved", "8919076702112", "product-images/Beloved.jpg", 60.00),(3, "Eleven Minutes", "8919076702113", "product-images/ElevenMinutes.jpg", 60.00),(4, "Jane Eyre", "8919076702114", "product-images/JaneEyre.jpg", 80.00),(5, "The Alchemist", "8919076702115", "product-images/TheAlchemist.jpg", 30.00),(6, "The Color Purple", "8919076702116", "product-images/TheColorPurple.jpg", 70.00),(7, "The Great Gatsby", "8919076702117", "product-images/TheGreatGatsby.jpg", 80.00),(8, "To Kill A Mocking Bird", "8919076702118", "product-images/ToKillAMockingBird.jpg", 40.00),(9, "War and Peace", "8919076702119", "product-images/WarAndPeace.jpg", 40.00),(10, "Forbidden", "8919076702110", "product-images/Forbidden.jpg", 90.00);')

con.commit()
con.close()

con = sqlite3.connect('products.db')

con.execute('CREATE TABLE users(uid INT unsigned, username VARCHAR(255), password VARCHAR(255))')

con.close()  
con = sqlite3.connect('products.db')

con.execute('INSERT INTO users(uid, username, password) VALUES (1, "customer1", "p455w0rd"),(2, "customer2", "p455w0rd");')
            
con.commit()
con.close()  

con = sqlite3.connect('products.db')

con.execute('CREATE TABLE administrator(uid INT unsigned, username VARCHAR(255), password VARCHAR(255))')

con.close()  
con = sqlite3.connect('products.db')

con.execute('INSERT INTO administrator(uid, username, password) VALUES (1, "Admin", "p455w0rd");')

con.commit()
con.close()







