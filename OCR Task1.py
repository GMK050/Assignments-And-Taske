
import pytesseract
from PIL import Image
import random
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
import getpass
import os

def check_possession_factor(verification_method="qr_code", user_input=None, reference_data=None):
    """
    Verify possession factor through various methods
    
    Args:
        verification_method (str): Method to verify possession - "qr_code", "otp", "hardware_token"
        user_input: User's input for verification
        reference_data: Reference data to compare against
    
    Returns:
        bool: True if possession is verified, False otherwise
    """
    
    if verification_method == "qr_code":
        return verify_qr_code_possession(user_input, reference_data)
    
    elif verification_method == "otp":
        return verify_otp_possession(user_input, reference_data)
    
    elif verification_method == "hardware_token":
        return verify_hardware_token(user_input, reference_data)
    
    else:
        print(f"Unknown verification method: {verification_method}")
        return False

def verify_qr_code_possession(user_image_path, reference_text):
    """
    Verify possession by scanning QR code or text from an image
    """
    try:
        if not os.path.exists(user_image_path):
            print(f"Error: Image file not found at {user_image_path}")
            return False
            
        img = Image.open(user_image_path)
        
        extracted_text = pytesseract.image_to_string(img).strip()
        print(f"Extracted from image: '{extracted_text}'")
        print(f"Reference text: '{reference_text}'")
        
        if extracted_text == reference_text:
            print("✓ Possession verified via QR/Image scan")
            return True
        else:
            print("✗ Possession verification failed")
            return False
            
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def verify_otp_possession(user_otp, reference_otp):
    """
    Verify possession using One-Time Password
    """
    print(f"User entered OTP: {user_otp}")
    print(f"Expected OTP: {reference_otp}")
    
    if user_otp == reference_otp:
        print("✓ Possession verified via OTP")
        return True
    else:
        print("✗ OTP verification failed")
        return False

def verify_hardware_token(user_token, reference_token):
    """
    Verify possession using hardware token
    """
    if user_token == reference_token:
        print("✓ Hardware token verified")
        return True
    else:
        print("✗ Hardware token verification failed")
        return False

def generate_otp(length=6):
    """Generate a random OTP"""
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    print(f"Generated OTP: {otp}")
    return otp

class TwoFactorAuth:
    def __init__(self):
        self.otp_storage = {}
        self.backup_codes = {}
    
    def send_otp_email(self, email, otp):
        """
        Simulate sending OTP via email
        In production, you would integrate with an actual email service
        """
        print(f"\n📧 Sending OTP to {email}")
        print(f"Your verification code is: {otp}")
        print("(In production, this would be sent via actual email)")
        return True
    
    def send_otp_sms(self, phone_number, otp):
        """
        Simulate sending OTP via SMS
        """
        print(f"\n📱 Sending OTP to {phone_number}")
        print(f"Your verification code is: {otp}")
        print("(In production, this would be sent via actual SMS)")
        return True
    
    def generate_backup_codes(self, user_id, count=5):
        """Generate backup codes for 2FA"""
        codes = [''.join([str(random.randint(0, 9)) for _ in range(8)]) for _ in range(count)]
        self.backup_codes[user_id] = codes
        print(f"\n🔑 Generated backup codes for {user_id}:")
        for code in codes:
            print(f"  - {code}")
        return codes
    
    def verify_backup_code(self, user_id, code):
        """Verify backup code"""
        if user_id in self.backup_codes and code in self.backup_codes[user_id]:
            self.backup_codes[user_id].remove(code)  # Use once
            print("✓ Backup code verified")
            return True
        return False
    
    def two_factor_auth(self, user_id, method="email", user_email=None, user_phone=None, possession_method=None, possession_input=None):

        print(f"\n{'='*50}")
        print(f"2FA VERIFICATION FOR USER: {user_id}")
        print(f"{'='*50}")
        
        if method == "email":
            if not user_email:
                print("Email required for email 2FA")
                return False
            
            otp = generate_otp()
            self.otp_storage[user_id] = otp
            self.send_otp_email(user_email, otp)
            
            user_input = input("Enter the OTP sent to your email: ")
            if user_input == self.otp_storage.get(user_id):
                print("✓ Email 2FA successful!")
                del self.otp_storage[user_id]  
                return True
            else:
                print("✗ Email 2FA failed")
                return False
        
        elif method == "sms":
            if not user_phone:
                print("Phone number required for SMS 2FA")
                return False
            
            otp = generate_otp()
            self.otp_storage[user_id] = otp
            self.send_otp_sms(user_phone, otp)
            
            user_input = input("Enter the OTP sent to your phone: ")
            if user_input == self.otp_storage.get(user_id):
                print("✓ SMS 2FA successful!")
                del self.otp_storage[user_id]
                return True
            else:
                print("✗ SMS 2FA failed")
                return False
        
        elif method == "possession":
            if not possession_method or not possession_input:
                print("Possession method and input required")
                return False
            
            if possession_method == "qr_code":
                reference_data = "SecureAccessToken123"  
                result = check_possession_factor("qr_code", possession_input, reference_data)
            elif possession_method == "otp":
                reference_otp = generate_otp()
                print(f"Use this OTP for possession verification: {reference_otp}")
                result = check_possession_factor("otp", possession_input, reference_otp)
            else:
                result = check_possession_factor(possession_method, possession_input, "reference_token")
            
            if result:
                print("✓ Possession-based 2FA successful!")
                return True
            else:
                print("✗ Possession-based 2FA failed")
                return False
        
        elif method == "backup":
            backup_code = input("Enter your backup code: ")
            if self.verify_backup_code(user_id, backup_code):
                print("✓ Backup code 2FA successful!")
                return True
            else:
                print("✗ Backup code 2FA failed")
                return False
        
        else:
            print(f"Unknown 2FA method: {method}")
            return False

def demonstrate_system():
    """Demonstrate the complete system"""
    
    auth_system = TwoFactorAuth()
    
    print("🔐 SECURITY SYSTEM DEMONSTRATION")
    print("=" * 50)
    
    user_id = "user123"
    user_email = "user@example.com"
    user_phone = "+1234567890"
    
    auth_system.generate_backup_codes(user_id)
    
    print("\n1. TESTING EMAIL 2FA:")
    print("-" * 30)
    
    print("\n2. TESTING SMS 2FA:")
    print("-" * 30)
    
    print("\n3. TESTING POSSESSION FACTOR (QR CODE):")
    print("-" * 40)
    reference_text = "SecureAccessToken123"
    

    test_image_path = "sample_image.png"  
    
    print("Testing possession factor verification...")
    if os.path.exists(test_image_path):
        possession_result = check_possession_factor(
            verification_method="qr_code",
            user_input=test_image_path,
            reference_data=reference_text
        )
    else:
        print(f"Test image not found at {test_image_path}")
        print("Skipping QR code test...")
    
    print("\n4. TESTING POSSESSION FACTOR (OTP):")
    print("-" * 40)
    test_otp = generate_otp()
    possession_otp_result = check_possession_factor(
        verification_method="otp",
        user_input=test_otp,  
        reference_data=test_otp
    )
    
    print("\n5. TESTING BACKUP CODE 2FA:")
    print("-" * 35)

    
    print("\n" + "=" * 50)
    print("DEMONSTRATION COMPLETE")
    print("=" * 50)

