import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime
import sqlite3
import base64
from PIL import Image
import io

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Use absolute imports
from utils.db import get_db_connection

# Admin credentials
ADMIN_USERNAME = "TechCar2Admin"
ADMIN_PASSWORD = "TechCar2Admin"

def login():
    st.markdown("""
        <style>
        .admin-header {
            background: linear-gradient(120deg, #232526 0%, #414345 100%);
            color: white;
            padding: 32px 24px 24px 24px;
            border-radius: 18px;
            margin-bottom: 32px;
            box-shadow: 0 6px 32px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
        }
        .admin-header h1 {
            font-size: 44px;
            font-weight: 800;
            margin: 0 0 8px 0;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
        }
        .admin-header .admin-emoji {
            font-size: 48px;
            margin-right: 18px;
            filter: drop-shadow(0 2px 8px #0008);
        }
        .admin-header p {
            font-size: 20px;
            opacity: 0.92;
            margin: 0;
        }
        .admin-header::before {
            content: '';
            position: absolute;
            top: -60px; left: -60px;
            width: 200px; height: 200px;
            background: radial-gradient(circle, #ff9800 0%, transparent 70%);
            opacity: 0.18;
            animation: shine 4s linear infinite;
        }
        @keyframes shine {
            0% { left: -60px; top: -60px; }
            100% { left: 80vw; top: 60px; }
        }
        .admin-card {
            background: linear-gradient(120deg, #232526 0%, #393939 100%);
            border-radius: 16px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.18);
            padding: 32px 24px;
            margin-bottom: 32px;
            color: white;
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .admin-card:hover {
            box-shadow: 0 8px 32px rgba(255,152,0,0.18);
            transform: translateY(-2px) scale(1.01);
        }
        .admin-btn {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            font-weight: 700;
            border-radius: 12px;
            border: none;
            background: linear-gradient(90deg, #ff9800 0%, #ffc107 100%);
            color: #232323;
            margin-top: 12px;
            margin-bottom: 8px;
            box-shadow: 0 2px 8px #ffc10755;
            transition: background 0.3s, color 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .admin-btn:hover {
            background: linear-gradient(90deg, #ffc107 0%, #ff9800 100%);
            color: #111;
            box-shadow: 0 4px 16px #ff980055;
        }
        .admin-badge {
            display: inline-block;
            background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
            color: #232323;
            font-size: 18px;
            font-weight: 700;
            border-radius: 10px;
            padding: 6px 18px;
            margin-bottom: 8px;
            box-shadow: 0 2px 8px #38f9d755;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="admin-header">
            <h1><span class="admin-emoji">🛡️</span>Admin Login</h1>
            <p>Welcome to the TechCar2 Admin Panel</p>
        </div>
    """, unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="admin_login_btn", help="Login as admin"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

def display_image(image_data):
    if image_data:
        try:
            # Convert binary data to image
            image = Image.open(io.BytesIO(image_data))
            st.image(image, use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")

def display_pdf(pdf_data, filename):
    if pdf_data:
        try:
            # Create a download button for the PDF
            st.download_button(
                label=f"Download {filename}",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error displaying PDF: {str(e)}")

def main():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if not st.session_state.admin_logged_in:
        login()
        return
    st.markdown("""
        <div class="admin-header">
            <h1><span class="admin-emoji">🛡️</span>Admin Panel</h1>
            <p>Manage car listings, inquiries, and price estimations</p>
        </div>
    """, unsafe_allow_html=True)
    # Removed sidebar UI
    # if st.sidebar.button("Logout"):
    #     st.session_state.admin_logged_in = False
    #     st.rerun()
    # page = st.sidebar.radio(
    #     "Select Section",
    #     ["Car Listings", "Buyer Inquiries", "Price Estimations"]
    # )
    # Default to "Car Listings" page
    page = "Car Listings"
    conn = get_db_connection()
    cursor = conn.cursor()
    if page == "Car Listings":
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.header("Car Listings")
        cursor.execute("""
            SELECT 
                c.*,
                s.email as seller_email,
                s.phone as seller_phone,
                s.state as seller_state,
                s.city as seller_city,
                s.created_at as seller_created_at
            FROM cars c
            JOIN sellers s ON c.seller_id = s.id
            WHERE c.status = 'pending'
            ORDER BY c.created_at DESC
        """)
        cars = cursor.fetchall()
        if not cars:
            st.info("No car listings found.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        for car in cars:
            with st.expander(f"{car['maker']} {car['model']} - ₹{car['price']:,}"):
                st.markdown("<div class='admin-card' style='background:linear-gradient(120deg,#181818 0%,#232526 100%);'>", unsafe_allow_html=True)
                st.subheader("Car Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Maker:** {car['maker']}")
                    st.write(f"**Model:** {car['model']}")
                    st.write(f"**Variant:** {car['variant']}")
                    st.write(f"**Year:** {car['year']}")
                    st.write(f"**Fuel Type:** {car['fuel_type']}")
                    st.write(f"**Transmission:** {car['transmission']}")
                with col2:
                    st.write(f"**Price:** ₹{car['price']:,}")
                    st.write(f"**Kilometers Driven:** {car['km_driven']:,}")
                    st.write(f"**Mileage:** {car['mileage']} km/l")
                    st.write(f"**Ownership:** {car['ownership']}")
                    st.write(f"**Location:** {car['city']}, {car['state']}")
                if car['extra_features']:
                    st.write("**Extra Features:**")
                    features = car['extra_features'].split(',')
                    for feature in features:
                        st.markdown(f"<span class='admin-badge'>{feature.strip()}</span>", unsafe_allow_html=True)
                st.subheader("Seller Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {car['seller_email']}")
                    st.write(f"**Phone:** {car['seller_phone']}")
                with col2:
                    st.write(f"**Location:** {car['seller_city']}, {car['seller_state']}")
                    st.write(f"**Listed on:** {car['seller_created_at']}")
                st.subheader("Car Images")
                cursor.execute("SELECT image_data FROM car_images WHERE car_id = ?", (car['id'],))
                images = cursor.fetchall()
                if images:
                    cols = st.columns(min(4, len(images)))
                    for idx, image in enumerate(images):
                        with cols[idx % 4]:
                            display_image(image['image_data'])
                else:
                    st.info("No images uploaded")
                st.subheader("Documents")
                col1, col2 = st.columns(2)
                with col1:
                    cursor.execute("SELECT document_data FROM documents WHERE car_id = ? AND document_type = 'rc_book'", (car['id'],))
                    rc_book = cursor.fetchone()
                    if rc_book:
                        display_pdf(rc_book['document_data'], f"RC_Book_{car['id']}.pdf")
                    else:
                        st.info("RC Book not uploaded")
                with col2:
                    cursor.execute("SELECT document_data FROM documents WHERE car_id = ? AND document_type = 'insurance'", (car['id'],))
                    insurance = cursor.fetchone()
                    if insurance:
                        display_pdf(insurance['document_data'], f"Insurance_{car['id']}.pdf")
                    else:
                        st.info("Insurance document not uploaded")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Approve", key=f"approve_{car['id']}", help="Approve this car listing"):
                        cursor.execute("UPDATE cars SET status = 'approved' WHERE id = ?", (car['id'],))
                        conn.commit()
                        st.success("Car listing approved!")
                        st.rerun()
                with col2:
                    if st.button("Reject", key=f"reject_{car['id']}", help="Reject this car listing"):
                        cursor.execute("UPDATE cars SET status = 'rejected' WHERE id = ?", (car['id'],))
                        conn.commit()
                        st.success("Car listing rejected!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    elif page == "Buyer Inquiries":
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.header("Buyer Inquiries")
        cursor.execute("""
            SELECT 
                bi.*,
                c.maker,
                c.model,
                c.price,
                s.email as seller_email
            FROM buyer_inquiries bi
            JOIN cars c ON bi.car_id = c.id
            JOIN sellers s ON c.seller_id = s.id
            ORDER BY bi.created_at DESC
        """)
        inquiries = cursor.fetchall()
        if not inquiries:
            st.info("No buyer inquiries found.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        for inquiry in inquiries:
            with st.expander(f"Inquiry for {inquiry['maker']} {inquiry['model']} - {inquiry['created_at']}"):
                st.markdown("<div class='admin-card' style='background:linear-gradient(120deg,#181818 0%,#232526 100%);'>", unsafe_allow_html=True)
                st.write(f"**Buyer Name:** {inquiry['name']}")
                st.write(f"**Buyer Email:** {inquiry['email']}")
                st.write(f"**Buyer Phone:** {inquiry['phone']}")
                st.write(f"**Message:** {inquiry['message']}")
                st.write(f"**Car Price:** ₹{inquiry['price']:,}")
                st.write(f"**Seller Email:** {inquiry['seller_email']}")
                if st.button("Mark as Contacted", key=f"contacted_{inquiry['id']}", help="Mark this inquiry as contacted"):
                    cursor.execute("UPDATE buyer_inquiries SET status = 'contacted' WHERE id = ?", (inquiry['id'],))
                    conn.commit()
                    st.success("Marked as contacted!")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:  # Price Estimations
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.header("Price Estimations")
        cursor.execute("""
            SELECT 
                pe.*,
                c.maker,
                c.model,
                c.price as actual_price
            FROM price_estimations pe
            JOIN cars c ON pe.car_id = c.id
            ORDER BY pe.created_at DESC
        """)
        estimations = cursor.fetchall()
        if not estimations:
            st.info("No price estimations found.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        for est in estimations:
            with st.expander(f"Estimation for {est['maker']} {est['model']} - {est['created_at']}"):
                st.markdown("<div class='admin-card' style='background:linear-gradient(120deg,#181818 0%,#232526 100%);'>", unsafe_allow_html=True)
                st.write(f"**Estimated Price:** ₹{est['estimated_price']:,}")
                st.write(f"**Actual Price:** ₹{est['actual_price']:,}")
                st.write(f"**Difference:** ₹{abs(est['estimated_price'] - est['actual_price']):,}")
                st.write(f"**Accuracy:** {est['accuracy']:.2f}%")
                if est['feature_importance']:
                    st.write(f"**Feature Importance:** {est['feature_importance']}")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 