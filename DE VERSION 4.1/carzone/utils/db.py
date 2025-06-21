import sqlite3
import os
from datetime import datetime
import hashlib

# Get the absolute path of the carzone directory
CARZONE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Database file path
DB_PATH = os.path.join(CARZONE_DIR, 'carzone.db')

def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables
    c.executescript('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            maker TEXT NOT NULL,
            model TEXT NOT NULL,
            variant TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            transmission TEXT NOT NULL,
            year INTEGER NOT NULL,
            km_driven INTEGER NOT NULL,
            mileage REAL NOT NULL,
            ownership TEXT NOT NULL,
            price REAL NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            extra_features TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES sellers (id)
        );
        
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            preferred_date TEXT NOT NULL,
            preferred_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES cars (id)
        );
        
        CREATE TABLE IF NOT EXISTS price_estimations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maker TEXT NOT NULL,
            model TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            transmission TEXT NOT NULL,
            year INTEGER NOT NULL,
            km_driven INTEGER NOT NULL,
            mileage REAL NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            estimated_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS car_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            image_data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES cars (id)
        );
        
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            document_type TEXT,
            document_data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES cars (id)
        );
        
        CREATE TABLE IF NOT EXISTS buyer_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            message TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES cars (id)
        );
    ''')
    
    # Add admin user if not exists
    admin_username = "TechCar2Admin"
    admin_password = "TechCar2Admin"
    password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
    
    try:
        c.execute('INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                 (admin_username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        # Admin already exists
        pass
    
    conn.close()

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_seller(email, phone, state, city):
    """Add a new seller to the database"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO sellers (email, phone, state, city)
            VALUES (?, ?, ?, ?)
        ''', (email, phone, state, city))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def add_car(seller_id, car_data):
    """Add a new car listing to the database"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO cars (
                seller_id, maker, model, fuel_type, transmission,
                variant, year, km_driven, mileage, ownership,
                price, state, city, extra_features
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            seller_id,
            car_data['maker'],
            car_data['model'],
            car_data['fuel_type'],
            car_data['transmission'],
            car_data['variant'],
            car_data['year'],
            car_data['km_driven'],
            car_data['mileage'],
            car_data['ownership'],
            car_data['price'],
            car_data['state'],
            car_data['city'],
            ','.join(car_data['extra_features'])
        ))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()

def add_buyer_inquiry(car_id, buyer_data):
    """Add a new buyer inquiry to the database"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO buyers (
                car_id, email, phone, state, city,
                preferred_date, preferred_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            car_id,
            buyer_data['email'],
            buyer_data['phone'],
            buyer_data['state'],
            buyer_data['city'],
            buyer_data['preferred_date'],
            buyer_data['preferred_time']
        ))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()

def add_price_estimation(estimation_data):
    """Add a new price estimation to the database"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO price_estimations (
                maker, model, fuel_type, transmission,
                year, km_driven, mileage, state, city,
                estimated_price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            estimation_data['maker'],
            estimation_data['model'],
            estimation_data['fuel_type'],
            estimation_data['transmission'],
            estimation_data['year'],
            estimation_data['km_driven'],
            estimation_data['mileage'],
            estimation_data['state'],
            estimation_data['city'],
            estimation_data['estimated_price']
        ))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()

def add_car_image(car_id, image_data):
    """Add an image for a car"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO car_images (car_id, image_data)
            VALUES (?, ?)
        ''', (car_id, image_data))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding car image: {str(e)}")
        return False
    finally:
        conn.close()

def add_document(car_id, document_type, document_data):
    """Add a document for a car"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO documents (car_id, document_type, document_data)
            VALUES (?, ?, ?)
        ''', (car_id, document_type, document_data))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding document: {str(e)}")
        return False
    finally:
        conn.close()

def add_buyer_inquiry_new(car_id, name, email, phone, message):
    """Add a new buyer inquiry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO buyer_inquiries (car_id, name, email, phone, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (car_id, name, email, phone, message))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error adding buyer inquiry: {str(e)}")
        return None
    finally:
        conn.close()

def add_price_estimation_new(car_id, estimated_price, accuracy, feature_importance):
    """Add a new price estimation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO price_estimations (car_id, estimated_price, accuracy, feature_importance)
            VALUES (?, ?, ?, ?)
        ''', (car_id, estimated_price, accuracy, str(feature_importance)))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error adding price estimation: {str(e)}")
        return None
    finally:
        conn.close()

# Initialize database when module is imported
init_db() 