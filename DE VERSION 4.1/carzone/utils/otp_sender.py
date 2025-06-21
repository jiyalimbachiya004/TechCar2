import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import streamlit as st
import time

# Load environment variables
load_dotenv()

# Gmail configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "TechCaar2@gmail.com"
SENDER_PASSWORD = "plck pyqf cqma aqpd"  # Using the original app password

# Store OTPs temporarily (in production, use a proper database)
otp_store = {}

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email):
    """Send OTP to the specified email"""
    try:
        # Generate OTP
        otp = generate_otp()
        otp_store[email] = {
            'otp': otp,
            'timestamp': time.time()
        }

        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = "Your TechCar2 Verification Code"

        body = f"""
        Hello,

        Your verification code for TechCar2 is: {otp}

        This code will expire in 10 minutes.

        If you didn't request this code, please ignore this email.

        Best regards,
        TechCar2 Team
        """

        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email
        server.send_message(msg)
        server.quit()

        return True, "OTP sent successfully! Please check your email."

    except Exception as e:
        print(f"Error sending email: {str(e)}")  # For debugging
        return False, f"Error sending OTP: {str(e)}"

def verify_otp(email, otp):
    """Verify the OTP for the specified email"""
    try:
        stored_data = otp_store.get(email)
        if not stored_data:
            return False, "No OTP found for this email. Please request a new OTP."

        # Check if OTP has expired (10 minutes)
        if time.time() - stored_data['timestamp'] > 600:
            del otp_store[email]
            return False, "OTP has expired. Please request a new OTP."

        if otp == stored_data['otp']:
            # Remove OTP after successful verification
            del otp_store[email]
            return True, "OTP verified successfully!"
        else:
            return False, "Invalid OTP. Please try again."

    except Exception as e:
        print(f"Error verifying OTP: {str(e)}")  # For debugging
        return False, f"Error verifying OTP: {str(e)}"

def send_otp_streamlit(to_email):
    """
    Send OTP to the specified email address.
    Returns the generated OTP for verification.
    """
    try:
        # Generate 4-digit OTP
        otp = ''.join(str(random.randint(0, 9)) for _ in range(4))
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = 'TechCar2 - OTP Verification'
        msg['From'] = 'TechCaar2@gmail.com'
        msg['To'] = to_email
        msg.set_content(f'''
        Your OTP for TechCar2 verification is: {otp}
        
        This OTP is valid for 10 minutes.
        Please do not share this OTP with anyone.
        
        Best regards,
        Team TechCar2
        ''')
        
        # Connect to SMTP server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('TechCaar2@gmail.com', 'plck pyqf cqma aqpd')
        server.send_message(msg)
        server.quit()
        
        # Store OTP in session state for verification
        st.session_state['otp'] = otp
        st.session_state['otp_time'] = time.time()
        
        return True, "OTP sent successfully!"
        
    except Exception as e:
        return False, f"Error sending OTP: {str(e)}"

def verify_otp_streamlit(input_otp):
    """
    Verify the OTP entered by the user.
    Returns True if OTP is valid, False otherwise.
    """
    if 'otp' not in st.session_state:
        return False, "No OTP has been sent. Please request an OTP first."
    
    if time.time() - st.session_state['otp_time'] > 600:  # 10 minutes expiry
        return False, "OTP has expired. Please request a new OTP."
    
    if input_otp == st.session_state['otp']:
        # Clear OTP from session state after successful verification
        del st.session_state['otp']
        del st.session_state['otp_time']
        return True, "OTP verified successfully!"
    
    return False, "Invalid OTP. Please try again." 