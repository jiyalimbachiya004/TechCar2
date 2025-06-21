import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime
import io
from PIL import Image
import base64

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Use absolute imports
from utils.otp_sender import send_otp, verify_otp
from utils.dropdowns import (
    models, locations, fuel_types, transmission_types,
    ownership_types, variants, extra_features,
    get_models_for_maker, get_cities_for_state
)
from utils.db import get_db_connection, add_buyer_inquiry_new

def display_image(image_data):
    """Display an image from binary data"""
    try:
        if image_data:
            # Convert binary data to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return f'<img src="data:image/jpeg;base64,{image_base64}" style="width:100%;height:100%;object-fit:cover;" />'
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")
    return ''

def get_car_listings(filters=None):
    """Get car listings with optional filters"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.*,
            s.email as seller_email,
            s.phone as seller_phone,
            s.state as seller_state,
            s.city as seller_city,
            ci.image_data as image_data
        FROM cars c
        JOIN sellers s ON c.seller_id = s.id
        LEFT JOIN car_images ci ON c.id = ci.car_id
        WHERE c.status = 'approved'
    """
    
    params = []
    if filters:
        conditions = []
        if filters.get('maker'):
            conditions.append("c.maker = ?")
            params.append(filters['maker'])
        if filters.get('model'):
            conditions.append("c.model = ?")
            params.append(filters['model'])
        if filters.get('fuel_type'):
            conditions.append("c.fuel_type = ?")
            params.append(filters['fuel_type'])
        if filters.get('transmission'):
            conditions.append("c.transmission = ?")
            params.append(filters['transmission'])
        if filters.get('min_price'):
            conditions.append("c.price >= ?")
            params.append(filters['min_price'])
        if filters.get('max_price'):
            conditions.append("c.price <= ?")
            params.append(filters['max_price'])
        if filters.get('state'):
            conditions.append("c.state = ?")
            params.append(filters['state'])
        if filters.get('city'):
            conditions.append("c.city = ?")
            params.append(filters['city'])
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
    
    query += " ORDER BY c.created_at DESC"
    
    cursor.execute(query, params)
    cars = cursor.fetchall()
    
    # Process the results to group images by car
    car_dict = {}
    for car in cars:
        car_id = car['id']
        if car_id not in car_dict:
            car_dict[car_id] = dict(car)
            car_dict[car_id]['images'] = []
        if car['image_data']:
            car_dict[car_id]['images'].append(car['image_data'])
    
    conn.close()
    return list(car_dict.values())

def main():
    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h1 style="margin:0;font-size:36px;">🚗 Find Your Perfect Car</h1>
            <p style="margin:10px 0 0 0;opacity:0.9;">Browse through our extensive collection of verified cars</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'selected_car' not in st.session_state:
        st.session_state.selected_car = None
    if 'otp_verified' not in st.session_state:
        st.session_state.otp_verified = False
    if 'email' not in st.session_state:
        st.session_state.email = None
    if 'show_contact' not in st.session_state:
        st.session_state.show_contact = False
    if 'current_image_index' not in st.session_state:
        st.session_state.current_image_index = 0
    
    # Filters in a collapsible section
    with st.expander("🔍 Advanced Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🚗 Car Details")
            maker = st.selectbox("Car Maker", [""] + list(models.keys()))
            if maker:
                model = st.selectbox("Car Model", [""] + get_models_for_maker(maker))
            else:
                model = ""
            fuel_type = st.selectbox("Fuel Type", [""] + fuel_types)
        
        with col2:
            st.markdown("### 💰 Price Range")
            min_price = st.number_input("Min Price (₹)", min_value=0, value=0, step=100000)
            max_price = st.number_input("Max Price (₹)", min_value=0, value=10000000, step=100000)
            transmission = st.selectbox("Transmission", [""] + transmission_types)
        
        with col3:
            st.markdown("### 📍 Location")
            state = st.selectbox("State", [""] + list(locations.keys()))
            if state:
                city = st.selectbox("City", [""] + get_cities_for_state(state))
            else:
                city = ""
    
    # Apply filters
    filters = {
        'maker': maker if maker else None,
        'model': model if model else None,
        'fuel_type': fuel_type if fuel_type else None,
        'transmission': transmission if transmission else None,
        'min_price': min_price if min_price > 0 else None,
        'max_price': max_price if max_price < 10000000 else None,
        'state': state if state else None,
        'city': city if city else None
    }
    
    # Get and display car listings
    cars = get_car_listings(filters)
    
    if not cars:
        st.info("No cars found matching your criteria.")
        return
    
    st.markdown(f"### 🚗 Found {len(cars)} Cars")

    # --- Streamlit-native horizontal scroll using columns ---
    card_cols = st.columns(min(len(cars), 4))  # Show up to 4 cards per row
    for idx, car in enumerate(cars):
        with card_cols[idx % 4]:
            # Session state for image index, details, and contact
            img_key = f"img_idx_{car['id']}"
            details_key = f"details_{car['id']}"
            contact_key = f"contact_{car['id']}"
            if img_key not in st.session_state:
                st.session_state[img_key] = 0
            if details_key not in st.session_state:
                st.session_state[details_key] = False
            if contact_key not in st.session_state:
                st.session_state[contact_key] = False

            # Card container
            st.markdown("<div style='background: #232323; border-radius: 12px; padding: 18px; margin-bottom: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'>", unsafe_allow_html=True)

            # Image carousel
            images = car.get('images', [])
            if images:
                img_idx = st.session_state[img_key]
                img = images[img_idx]
                st.image(Image.open(io.BytesIO(img)), use_column_width=True)
                col_img1, col_img2, col_img3 = st.columns([1,2,1])
                with col_img1:
                    if st.button("❮", key=f"prev_{car['id']}"):
                        st.session_state[img_key] = (img_idx - 1) % len(images)
                with col_img3:
                    if st.button("❯", key=f"next_{car['id']}"):
                        st.session_state[img_key] = (img_idx + 1) % len(images)
            else:
                st.image("https://via.placeholder.com/350x200?text=No+Image", use_column_width=True)

            # Car title and price
            st.markdown(f"<h3 style='color:white;margin:10px 0 0 0;'>{car['maker']} {car['model']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#4CAF50;font-size:22px;font-weight:700;margin-bottom:8px;'>₹{car['price']:,}</div>", unsafe_allow_html=True)

            # Quick stats
            st.markdown(f"<div style='color:#bbb;font-size:15px;margin-bottom:8px;'>"
                        f"<b>{car['year']}</b> • <b>{car['km_driven']:,} km</b> • <b>{car['fuel_type']}</b> • <b>{car['transmission']}</b>"
                        f"</div>", unsafe_allow_html=True)

            # More Details toggle
            if st.button("Show Less" if st.session_state[details_key] else "More Details", key=f"details_btn_{car['id']}"):
                st.session_state[details_key] = not st.session_state[details_key]
            if st.session_state[details_key]:
                st.markdown("<div style='background:#181818;padding:10px 12px;border-radius:8px;margin:10px 0;color:#eee;'>", unsafe_allow_html=True)
                st.write(f"**Variant:** {car['variant']}")
                st.write(f"**Ownership:** {car['ownership']}")
                st.write(f"**Location:** {car['city']}, {car['state']}")
                if car.get('extra_features'):
                    st.write("**Features:**")
                    for feature in car['extra_features'].split(','):
                        st.markdown(f"<span style='background:#2196F3;color:white;padding:4px 10px;border-radius:12px;margin:2px;display:inline-block;font-size:13px;'>{feature.strip()}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Contact Seller
            if st.button("Contact Seller", key=f"contact_btn_{car['id']}"):
                st.session_state[contact_key] = True
            if st.session_state[contact_key]:
                st.markdown("<div style='background:#181818;padding:16px 12px;border-radius:8px;margin:10px 0;color:#eee;'>", unsafe_allow_html=True)
                st.write("**Contact Seller**")
                email = st.text_input("Enter your email address", key=f"email_{car['id']}")
                if st.button("Send OTP", key=f"send_otp_{car['id']}"):
                    if email:
                        success, message = send_otp(email)
                        if success:
                            st.success(message)
                            st.session_state[f"otp_email_{car['id']}"] = email
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter your email address")
                otp_input = st.text_input("Enter OTP", key=f"otp_{car['id']}")
                if st.button("Verify OTP", key=f"verify_otp_{car['id']}"):
                    if otp_input and st.session_state.get(f"otp_email_{car['id']}"):
                        success, message = verify_otp(st.session_state[f"otp_email_{car['id']}"] , otp_input)
                        if success:
                            st.success(message)
                            st.write(f"Seller's Phone: **{car['seller_phone']}**")
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter both email and OTP")
                if st.button("Close", key=f"close_contact_{car['id']}"):
                    st.session_state[contact_key] = False
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 