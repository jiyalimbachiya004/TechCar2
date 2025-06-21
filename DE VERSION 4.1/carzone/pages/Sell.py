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
from utils.otp_sender import send_otp, verify_otp
from utils.dropdowns import (
    models, locations, fuel_types, transmission_types,
    ownership_types, variants, extra_features,
    get_models_for_maker, get_cities_for_state
)
from utils.db import get_db_connection, add_seller, add_car, add_car_image, add_document, DB_PATH

def render_sell_page():
    st.markdown("""
        <style>
        .sell-header {
            background: linear-gradient(120deg, #232526 0%, #414345 100%);
            color: white;
            padding: 32px 24px 24px 24px;
            border-radius: 18px;
            margin-bottom: 32px;
            box-shadow: 0 6px 32px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
        }
        .sell-header h1 {
            font-size: 44px;
            font-weight: 800;
            margin: 0 0 8px 0;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
        }
        .sell-header .car-emoji {
            font-size: 48px;
            margin-right: 18px;
            filter: drop-shadow(0 2px 8px #0008);
        }
        .sell-header p {
            font-size: 20px;
            opacity: 0.92;
            margin: 0;
        }
        .sell-header::before {
            content: '';
            position: absolute;
            top: -60px; left: -60px;
            width: 200px; height: 200px;
            background: radial-gradient(circle, #2196F3 0%, transparent 70%);
            opacity: 0.18;
            animation: shine 4s linear infinite;
        }
        @keyframes shine {
            0% { left: -60px; top: -60px; }
            100% { left: 80vw; top: 60px; }
        }
        .sell-card {
            background: linear-gradient(120deg, #232526 0%, #393939 100%);
            border-radius: 16px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.18);
            padding: 32px 24px;
            margin-bottom: 32px;
            color: white;
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .sell-card:hover {
            box-shadow: 0 8px 32px rgba(33,150,243,0.18);
            transform: translateY(-2px) scale(1.01);
        }
        .sell-btn {
            width: 100%;
            padding: 16px;
            font-size: 20px;
            font-weight: 700;
            border-radius: 12px;
            border: none;
            background: linear-gradient(90deg, #2196F3 0%, #38f9d7 100%);
            color: #232323;
            margin-top: 18px;
            margin-bottom: 8px;
            box-shadow: 0 2px 8px #38f9d755;
            transition: background 0.3s, color 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .sell-btn:hover {
            background: linear-gradient(90deg, #38f9d7 0%, #2196F3 100%);
            color: #111;
            box-shadow: 0 4px 16px #2196F355;
        }
        .sell-feature-tag {
            background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
            color: #232323;
            padding: 6px 16px;
            border-radius: 15px;
            font-size: 15px;
            margin: 4px 6px 4px 0;
            display: inline-block;
            font-weight: 500;
            box-shadow: 0 1px 4px #38f9d755;
            transition: background 0.3s;
        }
        .sell-feature-tag:hover {
            background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
        }
        /* Blue-wine gradient border for all Streamlit inputs */
        .stTextInput > div > div > input,
        .stNumberInput > div > input,
        .stSelectbox > div[data-baseweb="select"] > div,
        .stMultiSelect > div[data-baseweb="select"] > div,
        .stFileUploader > div {
            border: 2.5px solid;
            border-image: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) 1;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(33,150,243,0.10), 0 1px 4px rgba(156,39,176,0.10);
        }
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > input:focus,
        .stSelectbox > div[data-baseweb="select"] > div:focus-within,
        .stMultiSelect > div[data-baseweb="select"] > div:focus-within,
        .stFileUploader > div:focus-within {
            border-width: 3px;
            border-image: linear-gradient(90deg, #9C27B0 0%, #1976d2 100%) 1;
            box-shadow: 0 4px 16px rgba(156,39,176,0.18), 0 2px 8px rgba(33,150,243,0.12);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sell-header">
            <h1><span class="car-emoji">🚙</span>Sell Your Car</h1>
            <p>List your car in minutes and reach thousands of buyers!</p>
        </div>
    """, unsafe_allow_html=True)

    if 'otp_verified_sell' not in st.session_state:
        st.session_state.otp_verified_sell = False
    if 'email_sell' not in st.session_state:
        st.session_state.email_sell = None

    # Step 1: Email OTP Verification
    if not st.session_state.otp_verified_sell:
        st.markdown("<div class='sell-card'>", unsafe_allow_html=True)
        st.subheader("Step 1: Email Verification")
        email = st.text_input("Enter your email address", key="sell_email")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send OTP", key="send_otp_sell_btn", help="Send OTP to your email"):
                if email:
                    success, message = send_otp(email)
                    if success:
                        st.success(message)
                        st.session_state.email_sell = email
                    else:
                        st.error(message)
                else:
                    st.error("Please enter your email address")
        with col2:
            otp_input = st.text_input("Enter OTP", key="sell_otp_input")
            if st.button("Verify OTP", key="verify_otp_sell_btn", help="Verify the OTP sent to your email"):
                if otp_input and st.session_state.email_sell:
                    success, message = verify_otp(st.session_state.email_sell, otp_input)
                    if success:
                        st.success(message)
                        st.session_state.otp_verified_sell = True
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both email and OTP")
        st.markdown("</div>", unsafe_allow_html=True)

    # Car type and color options
    car_types = ["Sedan", "Hatchback", "SUV", "MPV", "Convertible", "Coupe", "Crossover", "Pickup", "Van", "Truck", "Other"]
    car_colors = ["White", "Black", "Silver", "Grey", "Red", "Blue", "Green", "Yellow", "Orange", "Brown", "Gold", "Other"]

    # Dynamic dropdowns outside the form
    maker = st.selectbox("Car Maker", list(models.keys()), key="car_maker_dynamic")
    model_list = get_models_for_maker(maker)
    model = st.selectbox("Car Model", model_list, key="car_model_dynamic")

    state = st.selectbox("State", list(locations.keys()), key="state_dynamic")
    city_list = get_cities_for_state(state)
    city = st.selectbox("City", city_list, key="city_dynamic")

    if st.session_state.otp_verified_sell:
        st.markdown("<div class='sell-card'>", unsafe_allow_html=True)
        st.subheader("Step 2: Car Details")
        with st.form("car_details_form"):
            col1, col2 = st.columns(2)
            with col1:
                km_driven = st.number_input("Kilometers Driven", min_value=0, value=10000)
            with col2:
                mileage = st.number_input("Mileage (km/l)", min_value=0.0, value=20.0)

            col1, col2 = st.columns(2)
            with col1:
                fuel_type = st.selectbox("Fuel Type", fuel_types)
            with col2:
                transmission = st.selectbox("Transmission Type", transmission_types)

            col1, col2 = st.columns(2)
            with col1:
                ownership = st.selectbox("Ownership", ownership_types)
            with col2:
                car_color = st.selectbox("Car Color", car_colors)

            col1, col2 = st.columns(2)
            with col1:
                car_type = st.selectbox("Car Type", car_types)
            with col2:
                variant = st.selectbox("Variant", variants)

            extra = st.multiselect("Extra Features", extra_features)

            price = st.number_input("Expected Price (₹)", min_value=0, value=500000)

            phone = st.text_input("Contact Number")
            contact_time = st.text_input("Preferred Contact Time (e.g., 10 AM - 6 PM)")
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
            st.markdown("<div>", unsafe_allow_html=True)
            for feature in extra:
                st.markdown(f"<span class='sell-feature-tag'>{feature}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.subheader("Upload Images")
            car_images = st.file_uploader(
                "Upload Car Images (at least 8, up to 12)",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True
            )
            st.subheader("Upload Documents")
            rc_book = st.file_uploader("Upload RC Book (PDF)", type=['pdf'])
            insurance = st.file_uploader("Upload Insurance Document (PDF)", type=['pdf'])
            submitted = st.form_submit_button("Submit Car Details", help="Submit your car for listing")
            if submitted:
                if not car_images or len(car_images) < 8:
                    st.error("Please upload at least 8 car images.")
                elif not rc_book:
                    st.error("Please upload RC Book (PDF).")
                elif not insurance:
                    st.error("Please upload Insurance Document (PDF).")
                else:
                    # Try to add seller, or fetch existing seller_id
                    seller_id = add_seller(
                        st.session_state.email_sell,
                        phone,
                        state,
                        city
                    )
                    if not seller_id:
                        # Try to fetch by email
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("SELECT id FROM sellers WHERE email = ?", (st.session_state.email_sell,))
                        row = c.fetchone()
                        conn.close()
                        if row:
                            seller_id = row[0]
                        else:
                            st.error("Error saving seller details. Please try again.")
                    if seller_id:
                        car_data = {
                            'maker': maker,
                            'model': model,
                            'fuel_type': fuel_type,
                            'transmission': transmission,
                            'variant': variant,
                            'year': datetime.now().year,  # You can add a year field if needed
                            'km_driven': km_driven,
                            'mileage': mileage,
                            'ownership': ownership,
                            'price': price,
                            'state': state,
                            'city': city,
                            'extra_features': extra,
                            'car_color': car_color,
                            'car_type': car_type
                        }
                        car_id = add_car(seller_id, car_data)
                        if car_id:
                            for image in car_images:
                                image_bytes = image.getvalue()
                                add_car_image(car_id, image_bytes)
                            rc_book_bytes = rc_book.getvalue()
                            add_document(car_id, 'rc_book', rc_book_bytes)
                            insurance_bytes = insurance.getvalue()
                            add_document(car_id, 'insurance', insurance_bytes)
                            st.success("Car submitted successfully! After admin verification, it will be listed within 24 hours.")
                            st.session_state.otp_verified_sell = False
                            st.session_state.email_sell = None
                        else:
                            st.error("Error saving car details. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    render_sell_page()

__all__ = ['main']
