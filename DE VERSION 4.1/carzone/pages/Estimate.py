import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import joblib
from sklearn.preprocessing import LabelEncoder
import sqlite3

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Use absolute imports
from utils.dropdowns import (
    models, locations, fuel_types, transmission_types,
    ownership_types, variants, extra_features,
    get_models_for_maker, get_cities_for_state
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from utils.db import get_db_connection, add_price_estimation

def load_data():
    try:
        # Get the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the carzone directory
        carzone_dir = os.path.dirname(current_dir)
        # Construct path to data file
        data_path = os.path.join(carzone_dir, 'data', 'car_data.csv')
        
        if not os.path.exists(data_path):
            st.error(f"Data file not found at: {data_path}")
            st.info("Please ensure car_data.csv exists in the carzone/data directory")
            return None
            
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def preprocess_data(df):
    df = df.dropna()
    possible_values = {
        'fuel_type': fuel_types,
        'seller_type': ["Individual", "Dealer", "Trustmark Dealer"],
        'transmission': transmission_types,
        'car_condition': ["Excellent", "Good", "Fair", "Poor"],
        'insurance_type': ["Comprehensive", "Third Party"],
        'make': list(models.keys()),
        'model': [model for models_list in models.values() for model in models_list],
        'variant': variants,
        'location': [city for cities in locations.values() for city in cities],
        'color': ["White", "Black", "Silver", "Grey", "Red", "Blue", "Green", "Yellow", "Orange", "Brown", "Gold", "Other"]
    }
    categorical_cols = ['make', 'model', 'variant', 'fuel_type', 'seller_type', 'transmission', 'car_condition', 'insurance_type', 'location', 'color']
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        if col in possible_values:
            df[col] = df[col].astype(str)
            all_vals = list(df[col].unique()) + [v for v in possible_values[col] if v not in df[col].unique()]
            le.fit(all_vals)
        else:
            le.fit(df[col].astype(str))
        df[col] = le.transform(df[col].astype(str))
        encoders[col] = le
    scaler = StandardScaler()
    num_cols = ['year', 'present_price', 'kilometers_driven', 'engine_cc', 'power_bhp', 'seats', 'owner']
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df, encoders, scaler, categorical_cols, num_cols

def train_model(df):
    X = df.drop(['selling_price'], axis=1)
    y = df['selling_price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test

def get_price_range(pred, present_price):
    # Clamp prediction to a reasonable range
    pred = min(pred, present_price)
    pred = max(pred, present_price * 0.3)
    # Return a range for different conditions
    return {
        "Excellent": (pred, pred * 1.1),
        "Good": (pred * 0.9, pred),
        "Fair": (pred * 0.8, pred * 0.9)
    }

def rule_based_price(present_price, year, kilometers, condition, owner):
    age = 2024 - year
    
    # Calculate base price based on age
    if age <= 3:
        base_price = present_price * 0.7  # 70% of present price for very new cars
    elif age <= 5:
        base_price = present_price * 0.6  # 60% of present price for 3-5 year old cars
    elif age <= 8:
        base_price = present_price * 0.5  # 50% of present price for 5-8 year old cars
    elif age <= 10:
        base_price = present_price * 0.4  # 40% of present price for 8-10 year old cars
    elif age <= 15:
        base_price = present_price * 0.3  # 30% of present price for 10-15 year old cars
    else:
        base_price = present_price * 0.2  # 20% of present price for very old cars
    
    # Kilometer-based adjustment
    km_factor = 1.0
    if kilometers > 100000:
        km_factor = 0.7
    elif kilometers > 75000:
        km_factor = 0.8
    elif kilometers > 50000:
        km_factor = 0.9
    
    # Condition factor
    condition_factor = {
        "Excellent": 1.0,
        "Good": 0.85,
        "Fair": 0.7,
        "Poor": 0.5
    }[condition]
    
    # Owner factor
    owner_factor = 1.0
    if owner > 1:
        owner_factor = 1.0 - (0.15 * (owner - 1))  # 15% reduction per additional owner
    
    # Calculate final price
    price = base_price * km_factor * condition_factor * owner_factor
    
    # Ensure price stays within reasonable limits
    min_price = present_price * 0.1  # Minimum 10% of present price
    max_price = present_price * 0.7  # Maximum 70% of present price
    
    return min(max(price, min_price), max_price)

def main():
    st.title("🚗 Car Price Estimator (ML Powered)")
    st.write("Get an instant price estimate for your car, just like Cars24, CarDekho, CarWale!")
    
    df = load_data()
    if df is None or df.empty:
        st.error("No data available.")
        return

    # Use predefined makes from models dictionary
    makes = sorted(list(models.keys()))
    selected_make = st.selectbox("Car Make", makes)
            
    # Get models for selected make using the utility function
    available_models = get_models_for_maker(selected_make)
    selected_model = st.selectbox("Car Model", available_models)
            
    # Get variants from the database for the selected make and model
    variants = sorted(df[(df['make'] == selected_make) & (df['model'] == selected_model)]['variant'].unique())
    if not variants:  # If no variants found in database, use default variants
        variants = ["LXI", "VXI", "ZXI", "ZXI+", "AMT", "Diesel", "Petrol"]
    selected_variant = st.selectbox("Variant", variants)

    # Try to get car details from database, if not found use default values
    car_row = df[(df['make'] == selected_make) & (df['model'] == selected_model) & (df['variant'] == selected_variant)]
    if car_row.empty:
        st.warning("Car not found in the database. Using default values.")
        car = {
            'year': 2020,
            'kilometers_driven': 30000,
            'owner': 1,
            'present_price': 8.0,
            'engine_cc': 1200,
            'power_bhp': 80,
            'seats': 5
        }
    else:
        car = car_row.iloc[0]

    st.write("### Enter Car Details")
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Year", min_value=2000, max_value=2024, value=int(car['year']))
        kilometers = st.number_input("Kilometers Driven", min_value=0, value=int(car['kilometers_driven']))
        car_condition = st.selectbox("Car Condition", ["Excellent", "Good", "Fair", "Poor"], index=0)
        owner = st.number_input("Number of Previous Owners", min_value=1, max_value=5, value=int(car['owner']))
        insurance_type = st.selectbox("Insurance Type", ["Comprehensive", "Third Party"], index=0)
        transmission = st.selectbox("Transmission", ["Manual", "Automatic", "AMT", "CVT", "DCT"], index=0)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "Electric", "Hybrid"], index=0)
    with col2:
        location = st.selectbox("Location", sorted(df['location'].unique()), index=0)
        seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"], index=0)
        present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=float(car['present_price']), step=0.1, format="%.2f")
        engine_cc = st.number_input("Engine CC", min_value=500, max_value=10000, value=int(car['engine_cc']))
        power_bhp = st.number_input("Power (BHP)", min_value=20, max_value=1000, value=int(car['power_bhp']))
        seats = st.number_input("Seats", min_value=2, max_value=10, value=int(car['seats']))
        color = st.selectbox("Color", sorted(df['color'].unique()), index=0)
                    
    if st.button("Predict Price", type="primary"):
        df_encoded, encoders, scaler, categorical_cols, num_cols = preprocess_data(df.copy())
        model, X_train, X_test, y_train, y_test = train_model(df_encoded)

        input_dict = {
            'make': selected_make,
            'model': selected_model,
            'variant': selected_variant,
            'year': year,
            'present_price': present_price,
            'kilometers_driven': kilometers,
            'fuel_type': fuel_type,
            'seller_type': seller_type,
            'transmission': transmission,
            'owner': owner,
            'car_condition': car_condition,
            'insurance_type': insurance_type,
            'location': location,
            'engine_cc': engine_cc,
            'power_bhp': power_bhp,
            'seats': seats,
            'color': color
        }
        for col in categorical_cols:
            input_dict[col] = encoders[col].transform([input_dict[col]])[0]
        input_df = pd.DataFrame([input_dict])
        input_df[num_cols] = scaler.transform(input_df[num_cols])

        ml_pred = model.predict(input_df)[0]
        rule_pred = rule_based_price(present_price, year, kilometers, car_condition, owner)
        
        # Blend ML and rule-based predictions with age-based weighting
        age = 2024 - year
        if age > 10:
            # For older cars, rely more on rule-based prediction
            blended_pred = (0.3 * ml_pred + 0.7 * rule_pred)
        elif age > 5:
            # For middle-aged cars, use equal weighting
            blended_pred = (0.5 * ml_pred + 0.5 * rule_pred)
        else:
            # For newer cars, rely more on ML prediction
            blended_pred = (0.7 * ml_pred + 0.3 * rule_pred)
        
        # Apply age-based maximum price limits
        if age > 15:
            max_price = present_price * 0.2  # 20% of present price for very old cars
        elif age > 10:
            max_price = present_price * 0.3  # 30% of present price for old cars
        elif age > 5:
            max_price = present_price * 0.5  # 50% of present price for middle-aged cars
        else:
            max_price = present_price * 0.7  # 70% of present price for newer cars
            
        min_price = present_price * 0.1  # Minimum 10% of present price
        final_pred = min(max(blended_pred, min_price), max_price)

        # Show warning if prediction is still high
        if final_pred > present_price * 0.7:
            st.warning("Predicted price is unusually high for a used car. Please check your inputs or try a different car.")

        st.success(f"### Estimated Resale Value: ₹{final_pred:.2f} lakhs")
        
        st.write("### Price Comparison")
        st.info(f"Original Price: ₹{present_price:.2f}L")
        st.info(f"Estimated Resale: ₹{final_pred:.2f}L")
        st.info(f"Total Depreciation: {((present_price - final_pred) / present_price * 100):.1f}%")
                                
        # Show summary of how each input affects the price
        st.write("### What Affects Your Price?")
        age = 2024 - year
        st.markdown(f"- **Age:** {age} years old. Older cars depreciate more.")
        st.markdown(f"- **Kilometers Driven:** {kilometers:,} km. Higher mileage reduces value.")
        st.markdown(f"- **Condition:** {car_condition}. Better condition increases value.")
        st.markdown(f"- **Ownership:** {owner} owner(s). More owners usually means lower price.")
        st.markdown(f"- **Fuel Type:** {fuel_type}. Diesel/CNG may have different resale trends.")
        st.markdown(f"- **Transmission:** {transmission}. Automatic cars may fetch a premium.")
        st.markdown(f"- **Location:** {location}. Metro cities often have higher resale values.")
        st.markdown(f"- **Insurance Type:** {insurance_type}. Comprehensive insurance is a plus.")
        st.markdown(f"- **Color:** {color}. Popular colors may sell for more.")
        st.markdown(f"- **Engine/Power/Seats:** {engine_cc}cc, {power_bhp}BHP, {seats} seats.")
        st.write("\n**Summary:**\n\nThe resale value is most affected by age, kilometers, condition, ownership, and location. Keeping your car well-maintained, with fewer owners and lower mileage, will help you get a better price!")

if __name__ == "__main__":
    main()
