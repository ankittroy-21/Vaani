"""
SMS/USSD Integration for Vaani
Enables users without internet access to use essential services via SMS
"""

import os
import json
import re
import hashlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sms_integration.log'
)

logger = logging.getLogger('sms_integration')

class SMSIntegration:
    def __init__(self, api_key=None, config_file="sms_config.json"):
        """Initialize SMS integration with optional API key"""
        self.api_key = api_key
        self.config_file = config_file
        self.load_config()
        self.command_patterns = {
            "help": r'^(?:मदद|help)$',
            "weather": r'^(?:मौसम|weather)\s+(.+)$',
            "prices": r'^(?:भाव|price|rate)\s+(.+)$',
            "scheme": r'^(?:योजना|scheme)\s+(.+)$',
            "emergency": r'^(?:आपात|emergency)$',
            "account": r'^(?:खाता|account)\s+(.+)$',
            "expense": r'^(?:खर्च|expense)\s+(.+)$',
            "calculator": r'^(?:गणना|calc)\s+(.+)$',
        }
    
    def load_config(self):
        """Load SMS configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if not self.api_key and "api_key" in config:
                        self.api_key = config["api_key"]
                    self.config = config
                    logger.info("Loaded SMS configuration")
            except json.JSONDecodeError:
                logger.error(f"Error decoding config file: {self.config_file}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self):
        """Get default SMS configuration"""
        return {
            "shortcode": "56677",
            "prefix": "VAANI",
            "max_sms_length": 160,
            "service_active": True,
            "reply_format": "VAANI: {message}",
            "help_message": "VAANI मदद: 'मौसम [शहर]', 'भाव [फसल]', 'योजना [नाम]', 'आपात', 'खाता [प्रश्न]', 'खर्च [विवरण]'",
            "sms_providers": {
                "default": {
                    "name": "Log Only (No SMS)",
                    "api_endpoint": None,
                    "method": "GET",
                    "active": True
                }
                # Add more providers as needed
            }
        }
    
    def save_config(self):
        """Save SMS configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info("Saved SMS configuration")
            return True
        except Exception as e:
            logger.error(f"Error saving SMS config: {str(e)}")
            return False
    
    def send_sms(self, phone_number, message):
        """Send SMS to a phone number"""
        if not self.config.get("service_active", False):
            logger.warning("SMS service is not active")
            return False
        
        # Format message according to configuration
        formatted_message = self.config["reply_format"].format(message=message)
        
        # Truncate message if too long
        max_length = self.config.get("max_sms_length", 160)
        if len(formatted_message) > max_length:
            formatted_message = formatted_message[:max_length-3] + "..."
        
        # Get default provider
        provider = self.config["sms_providers"]["default"]
        
        if not provider["active"]:
            logger.warning("Default SMS provider is not active")
            return False
        
        # If no API endpoint, just log the message (for testing)
        if not provider["api_endpoint"]:
            logger.info(f"SMS to {phone_number}: {formatted_message}")
            return True
        
        # Otherwise, attempt to send via API
        try:
            import requests
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "to": phone_number,
                "message": formatted_message,
                "sender": self.config.get("shortcode", "VAANI")
            }
            
            response = requests.post(
                provider["api_endpoint"],
                json=data,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully sent SMS to {phone_number}")
                return True
            else:
                logger.error(f"Failed to send SMS: {response.status_code}, {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False
    
    def process_incoming_sms(self, phone_number, message_body):
        """Process incoming SMS and determine appropriate response"""
        # Check for prefix if using shortcode
        prefix = self.config.get("prefix", "VAANI")
        if prefix and message_body.upper().startswith(prefix):
            # Remove prefix and any separators
            message_body = re.sub(r'^' + prefix + r'\s*[:\s]\s*', '', message_body, flags=re.IGNORECASE)
        
        # Trim message
        message_body = message_body.strip()
        
        # Default response if nothing matches
        response = "कृपया सही कमांड भेजें। मदद के लिए 'VAANI मदद' लिखें।"
        
        # Check for help command
        if re.match(self.command_patterns["help"], message_body, re.IGNORECASE):
            return self.config["help_message"]
        
        # Check for weather query
        weather_match = re.match(self.command_patterns["weather"], message_body, re.IGNORECASE)
        if weather_match:
            city = weather_match.group(1).strip()
            return self.get_weather_sms(city)
        
        # Check for price query
        price_match = re.match(self.command_patterns["prices"], message_body, re.IGNORECASE)
        if price_match:
            crop = price_match.group(1).strip()
            return self.get_crop_price_sms(crop)
        
        # Check for scheme query
        scheme_match = re.match(self.command_patterns["scheme"], message_body, re.IGNORECASE)
        if scheme_match:
            scheme = scheme_match.group(1).strip()
            return self.get_scheme_info_sms(scheme)
        
        # Check for emergency info
        if re.match(self.command_patterns["emergency"], message_body, re.IGNORECASE):
            return self.get_emergency_info_sms()
        
        # Check for account/banking info
        account_match = re.match(self.command_patterns["account"], message_body, re.IGNORECASE)
        if account_match:
            query = account_match.group(1).strip()
            return self.get_banking_info_sms(query)
        
        # Check for expense tracking
        expense_match = re.match(self.command_patterns["expense"], message_body, re.IGNORECASE)
        if expense_match:
            expense_details = expense_match.group(1).strip()
            return self.track_expense_sms(phone_number, expense_details)
        
        # Check for calculations
        calc_match = re.match(self.command_patterns["calculator"], message_body, re.IGNORECASE)
        if calc_match:
            calculation = calc_match.group(1).strip()
            return self.calculate_sms(calculation)
        
        return response
    
    def get_weather_sms(self, city):
        """Get weather information for SMS"""
        # This would integrate with your weather service
        # For now, return a placeholder message
        return f"आज {city} में मौसम: आंशिक बादल, तापमान 28°C, हवा 10km/h, बारिश की संभावना 20%"
    
    def get_crop_price_sms(self, crop):
        """Get crop price information for SMS"""
        # This would integrate with your agricultural price service
        # For now, return a placeholder message
        prices = {
            "गेहूं": "2015",
            "धान": "1868",
            "चावल": "1868", 
            "मक्का": "1850",
            "दाल": "6000",
            "आलू": "1200",
            "प्याज": "1400"
        }
        
        if crop.lower() in [k.lower() for k in prices.keys()]:
            for key in prices:
                if crop.lower() == key.lower():
                    return f"{key} का वर्तमान बाजार भाव: ₹{prices[key]} प्रति क्विंटल"
        
        return f"{crop} का भाव फिलहाल उपलब्ध नहीं है। कृपया अन्य फसल का नाम भेजें।"
    
    def get_scheme_info_sms(self, scheme):
        """Get scheme information for SMS"""
        # This would integrate with your scheme service
        # For now, include basic info about common schemes
        schemes = {
            "pm-kisan": "प्रधानमंत्री किसान सम्मान निधि: किसानों को ₹6000 सालाना 3 किश्तों में। पंजीकरण के लिए अपने ग्राम पंचायत जाएं।",
            "pmfby": "प्रधानमंत्री फसल बीमा योजना: फसल खराब होने पर मुआवजा। आवेदन फसल बुवाई के 15 दिन के भीतर करें।",
            "jandhan": "जन धन योजना: शून्य बैलेंस पर बैंक खाता, ₹2 लाख का दुर्घटना बीमा फ्री। नजदीकी बैंक में खोलें।",
            "ujjwala": "उज्ज्वला योजना: महिलाओं को मुफ्त गैस कनेक्शन। आवेदन के लिए आधार कार्ड और बैंक खाता जरूरी।"
        }
        
        # Check for matching schemes
        for key, info in schemes.items():
            if scheme.lower() in key.lower() or key.lower() in scheme.lower():
                return info
        
        return f"{scheme} योजना की जानकारी फिलहाल उपलब्ध नहीं है। अन्य योजना जैसे 'pm-kisan', 'jandhan' आदि के बारे में पूछें।"
    
    def get_emergency_info_sms(self):
        """Get emergency contact information for SMS"""
        return "आपातकालीन नंबर: पुलिस: 100, एम्बुलेंस: 108, फायर: 101, महिला हेल्पलाइन: 1091, बाल हेल्पलाइन: 1098, किसान: 1800-180-1551"
    
    def get_banking_info_sms(self, query):
        """Get banking information for SMS"""
        # Common banking queries
        banking_info = {
            "खाता": "बैंक खाता खोलने के लिए आधार कार्ड, फोटो और पते का प्रमाण लेकर नजदीकी बैंक शाखा जाएं।",
            "atm": "ATM से पैसे निकालने के लिए: 1) ATM कार्ड डालें 2) पिन डालें 3) राशि चुनें 4) पैसे और कार्ड वापस लें",
            "जनधन": "जन धन खाता खोलने के लिए आधार कार्ड और फोटो लेकर बैंक जाएं। इसमें कोई न्यूनतम बैलेंस नहीं रखना होता।",
            "लोन": "किसान क्रेडिट कार्ड के लिए जमीन दस्तावेज, आधार कार्ड और बैंक खाता विवरण लेकर बैंक जाएं। ब्याज दर 7% है।"
        }
        
        # Check for matching information
        for key, info in banking_info.items():
            if key.lower() in query.lower():
                return info
        
        return "बैंकिंग संबंधित जानकारी के लिए 'खाता', 'ATM', 'जनधन', या 'लोन' के बारे में पूछें।"
    
    def track_expense_sms(self, phone_number, details):
        """Track expense via SMS"""
        # Generate a user ID from the phone number
        user_id = hashlib.md5(phone_number.encode()).hexdigest()[:8]
        
        try:
            # Import the expense tracker module
            from vaani.services.finance.expense_tracker_service import ExpenseTracker
            
            tracker = ExpenseTracker()
            
            # Create user if not exists
            user_file = os.path.join("expense_data", f"{user_id}_expenses.json")
            if not os.path.exists(user_file):
                tracker.create_user(user_id)
            
            # Process the expense details
            result = tracker.handle_query(user_id, details)
            
            # Return a shortened version for SMS
            if isinstance(result, tuple):
                return result[0]  # Just the message part
            
            # If the result is too long, truncate it
            max_length = self.config.get("max_sms_length", 160)
            if len(result) > max_length:
                return result[:max_length-3] + "..."
                
            return result
            
        except Exception as e:
            logger.error(f"Error processing expense via SMS: {str(e)}")
            return "खर्च दर्ज करने में समस्या आई। कृपया इस प्रारूप का प्रयोग करें: 'खर्च 500 रुपये सब्जी'"
    
    def calculate_sms(self, calculation):
        """Perform calculation for SMS"""
        # Clean up the calculation string
        calculation = calculation.replace('x', '*').replace('÷', '/')
        
        # Check for common Hindi words for operations
        calculation = calculation.replace('गुना', '*').replace('जोड़', '+')
        calculation = calculation.replace('घटा', '-').replace('बांटा', '/')
        
        # Extract numbers and operation
        try:
            # Try using the safer eval approach for basic calculations
            # This is a simplified approach - for production, use a proper calculator library
            from simpleeval import simple_eval
            
            result = simple_eval(calculation)
            return f"गणना का परिणाम: {calculation} = {result}"
        except:
            try:
                # Fallback to regex pattern matching for simple operations
                pattern = r'(\d+)\s*([\+\-\*\/])\s*(\d+)'
                match = re.search(pattern, calculation)
                if match:
                    num1 = int(match.group(1))
                    operator = match.group(2)
                    num2 = int(match.group(3))
                    
                    if operator == '+':
                        result = num1 + num2
                    elif operator == '-':
                        result = num1 - num2
                    elif operator == '*':
                        result = num1 * num2
                    elif operator == '/':
                        if num2 == 0:
                            return "शून्य से विभाजित नहीं कर सकते"
                        result = num1 / num2
                    
                    return f"गणना का परिणाम: {calculation} = {result}"
            except:
                pass
            
            return "गणना समझ नहीं आई। कृपया इस प्रारूप का प्रयोग करें: 'गणना 100 + 50' या 'गणना 5 गुना 10'"

# Example for handling SMS in main.py
def process_sms_command(phone_number, message):
    """Process SMS commands from main.py"""
    sms = SMSIntegration()
    response = sms.process_incoming_sms(phone_number, message)
    
    # Send the SMS response
    sms.send_sms(phone_number, response)
    
    return response  # Return for logging

# USSD handler (for feature phones)
def process_ussd_command(phone_number, ussd_code):
    """Process USSD commands like *123# services"""
    # USSD codes typically start with * and end with #
    if not (ussd_code.startswith('*') and ussd_code.endswith('#')):
        return "Invalid USSD code"
    
    # Remove the * and # from the code
    code = ussd_code[1:-1]
    
    # Define USSD menu options
    menus = {
        "123": "1. Weather\n2. Crop Prices\n3. Emergency\n4. Schemes\n5. Bank Info",
        "123*1": "Enter city name:",
        "123*2": "Enter crop name:",
        "123*3": "1. Police\n2. Ambulance\n3. Fire\n4. Women Helpline\n5. Child Helpline",
        "123*4": "1. PM-KISAN\n2. Jan Dhan\n3. PMFBY\n4. Ujjwala",
        "123*5": "1. Account Opening\n2. ATM Usage\n3. Loan Info\n4. Jan Dhan"
    }
    
    # Check if the code exists in our menu system
    if code in menus:
        return menus[code]
    
    # Handle more complex interactions (would require session management in production)
    if code.startswith('123*1*'):
        # Weather for a city
        city = code[6:]
        sms = SMSIntegration()
        return sms.get_weather_sms(city)
    
    if code.startswith('123*2*'):
        # Crop price
        crop = code[6:]
        sms = SMSIntegration()
        return sms.get_crop_price_sms(crop)
    
    # Handle emergency number selection
    if code == "123*3*1":
        return "Police: 100"
    elif code == "123*3*2":
        return "Ambulance: 108"
    
    # Default response for unknown codes
    return "Unknown USSD code. Try *123#"

# Test function
if __name__ == "__main__":
    # Test SMS functionality
    sms = SMSIntegration()
    
    test_messages = [
        "VAANI मदद",
        "VAANI मौसम दिल्ली",
        "VAANI भाव गेहूं",
        "VAANI योजना pm-kisan",
        "VAANI आपात",
        "VAANI खाता ATM कैसे चलाते हैं",
        "VAANI खर्च 500 रुपये सब्जी खरीदी",
        "VAANI गणना 100 गुना 5"
    ]
    
    print("Testing SMS Integration")
    print("======================")
    
    for message in test_messages:
        print(f"\nInput: {message}")
        response = sms.process_incoming_sms("9876543210", message)
        print(f"Response: {response}")
    
    # Test USSD functionality
    ussd_codes = [
        "*123#",
        "*123*1#",
        "*123*1*Delhi#",
        "*123*3*1#"
    ]
    
    print("\n\nTesting USSD Integration")
    print("======================")
    
    for code in ussd_codes:
        print(f"\nUSSD: {code}")
        response = process_ussd_command("9876543210", code)
        print(f"Response: {response}")