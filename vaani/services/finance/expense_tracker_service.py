"""
Voice-based Expense Tracker for Illiterate Users
Allows users to track their daily expenses and income without reading/writing
SDG Goal 1: No Poverty
"""

import os
import json
from datetime import datetime, timedelta
import logging
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='expense_tracker.log'
)

logger = logging.getLogger('expense_tracker')

class ExpenseTracker:
    def __init__(self, data_dir="expense_data"):
        """Initialize the expense tracker with data directory"""
        self.data_dir = data_dir
        self.ensure_data_dir()
        self.categories = {
            "खाना": ["खाना", "भोजन", "राशन", "सब्जी", "फल", "दूध", "चावल", "गेहूं", "आटा"],
            "किराना": ["किराना", "साबुन", "तेल", "मसाला", "चीनी", "नमक"],
            "यातायात": ["बस", "ऑटो", "रिक्शा", "ट्रेन", "पेट्रोल", "डीजल", "किराया"],
            "शिक्षा": ["स्कूल", "किताब", "कॉपी", "पेंसिल", "फीस"],
            "स्वास्थ्य": ["दवाई", "डॉक्टर", "अस्पताल", "इलाज", "बीमारी"],
            "बिजली": ["बिजली", "बिल", "लाइट"],
            "फोन": ["मोबाइल", "रिचार्ज", "फोन", "सिम"],
            "कपड़े": ["कपड़े", "जूते", "चप्पल"],
            "घर": ["किराया", "मरम्मत", "घर"],
            "खेती": ["बीज", "खाद", "कीटनाशक", "ट्रैक्टर", "सिंचाई"],
            "आमदनी": ["कमाई", "सैलरी", "वेतन", "पगार", "मजदूरी", "बेचा", "फसल"]
        }
        
    def ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
    
    def get_user_data_path(self, user_id):
        """Get the user data file path"""
        return os.path.join(self.data_dir, f"{user_id}_expenses.json")
    
    def load_user_data(self, user_id):
        """Load user's expense data"""
        data_path = self.get_user_data_path(user_id)
        if os.path.exists(data_path):
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding data file: {data_path}")
                return self.initialize_user_data()
        return self.initialize_user_data()
    
    def initialize_user_data(self):
        """Create a new user data structure"""
        return {
            "transactions": [],
            "monthly_summary": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_user_data(self, user_id, data):
        """Save user's expense data"""
        data_path = self.get_user_data_path(user_id)
        try:
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Updated data for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving data for user {user_id}: {str(e)}")
            return False
    
    def create_user(self, name=None):
        """Create a new user"""
        user_id = str(uuid.uuid4())[:8]
        data = self.initialize_user_data()
        if name:
            data["name"] = name
        self.save_user_data(user_id, data)
        return user_id
    
    def detect_transaction_type(self, command):
        """Determine if the transaction is income or expense"""
        income_keywords = ["मिला", "कमाए", "कमाया", "आया", "आमदनी", "मिली", "पाया", "वेतन", "सैलरी", "पगार", "बेचा"]
        
        for keyword in income_keywords:
            if keyword in command.lower():
                return "income"
        
        return "expense"  # Default to expense
    
    def parse_amount(self, command):
        """Extract amount from the command"""
        import re
        
        # Look for patterns like "500 रुपये", "रुपये 500", "500 Rs", etc.
        amount_patterns = [
            r'(\d+)\s*(?:रुपये|रुपया|रूपये|रूपया|Rs|₹)',
            r'(?:रुपये|रुपया|रूपये|रूपया|Rs|₹)\s*(\d+)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, command)
            if match:
                return int(match.group(1))
        
        # Look for just numbers
        number_match = re.search(r'\b(\d+)\b', command)
        if number_match:
            return int(number_match.group(1))
        
        return None
    
    def detect_category(self, command):
        """Detect expense category from command"""
        command_lower = command.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in command_lower:
                    return category
        
        return "अन्य"  # Miscellaneous/Other
        
    def add_transaction(self, user_id, command):
        """Add a new transaction based on voice command"""
        # Parse the command to extract information
        transaction_type = self.detect_transaction_type(command)
        amount = self.parse_amount(command)
        category = self.detect_category(command)
        
        if not amount:
            return "मुझे राशि समझ नहीं आई। कृपया फिर से बताएं, जैसे '500 रुपये सब्जी खरीदी'", None
        
        # Load user data
        user_data = self.load_user_data(user_id)
        
        # Create transaction
        transaction = {
            "id": str(uuid.uuid4())[:8],
            "date": datetime.now().isoformat(),
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "description": command,
            "month_year": datetime.now().strftime("%Y-%m")
        }
        
        # Add to transactions
        user_data["transactions"].append(transaction)
        
        # Update monthly summary
        month_year = transaction["month_year"]
        if month_year not in user_data["monthly_summary"]:
            user_data["monthly_summary"][month_year] = {
                "income": 0,
                "expense": 0,
                "balance": 0,
                "categories": {}
            }
        
        # Update the amounts
        if transaction_type == "income":
            user_data["monthly_summary"][month_year]["income"] += amount
        else:
            user_data["monthly_summary"][month_year]["expense"] += amount
            
            # Update category amount
            if category not in user_data["monthly_summary"][month_year]["categories"]:
                user_data["monthly_summary"][month_year]["categories"][category] = 0
                
            user_data["monthly_summary"][month_year]["categories"][category] += amount
        
        # Calculate balance
        user_data["monthly_summary"][month_year]["balance"] = (
            user_data["monthly_summary"][month_year]["income"] - 
            user_data["monthly_summary"][month_year]["expense"]
        )
        
        # Save user data
        if self.save_user_data(user_id, user_data):
            if transaction_type == "income":
                return f"आमदनी जोड़ दी गई: {amount} रुपये", transaction
            else:
                return f"खर्चा जोड़ दिया गया: {amount} रुपये, श्रेणी: {category}", transaction
        else:
            return "खर्चा जोड़ने में समस्या आई, कृपया फिर से कोशिश करें", None

    def get_today_summary(self, user_id):
        """Get summary of today's transactions"""
        user_data = self.load_user_data(user_id)
        today = datetime.now().date().isoformat()
        
        today_income = 0
        today_expense = 0
        transactions = []
        
        for transaction in user_data["transactions"]:
            trans_date = datetime.fromisoformat(transaction["date"]).date().isoformat()
            if trans_date == today:
                transactions.append(transaction)
                if transaction["type"] == "income":
                    today_income += transaction["amount"]
                else:
                    today_expense += transaction["amount"]
        
        if not transactions:
            return "आज कोई लेनदेन नहीं किया गया है।"
        
        response = f"आज का हिसाब: आमदनी {today_income} रुपये, खर्च {today_expense} रुपये, बचत {today_income - today_expense} रुपये।\n\n"
        
        for i, t in enumerate(transactions, 1):
            type_str = "आमदनी" if t["type"] == "income" else "खर्च"
            response += f"{i}. {type_str}: {t['amount']} रुपये - {t['category']}\n"
            
        return response

    def get_monthly_summary(self, user_id, month_offset=0):
        """Get monthly summary with optional offset (0=current month, -1=last month)"""
        user_data = self.load_user_data(user_id)
        
        target_date = datetime.now() - timedelta(days=30 * month_offset)
        month_year = target_date.strftime("%Y-%m")
        
        month_name = self.get_hindi_month_name(target_date.month)
        
        if month_year not in user_data["monthly_summary"]:
            return f"{month_name} {target_date.year} का कोई हिसाब नहीं मिला।"
        
        monthly_data = user_data["monthly_summary"][month_year]
        
        response = f"{month_name} {target_date.year} का मासिक हिसाब:\n\n"
        response += f"कुल आमदनी: {monthly_data['income']} रुपये\n"
        response += f"कुल खर्च: {monthly_data['expense']} रुपये\n"
        response += f"बचत: {monthly_data['balance']} रुपये\n\n"
        
        if monthly_data["categories"]:
            response += "श्रेणी अनुसार खर्च:\n"
            for category, amount in monthly_data["categories"].items():
                response += f"- {category}: {amount} रुपये\n"
            
        return response
    
    def get_hindi_month_name(self, month_number):
        """Convert month number to Hindi month name"""
        hindi_months = [
            "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", 
            "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
        ]
        return hindi_months[month_number - 1]

    def handle_query(self, user_id, query):
        """Handle natural language queries about expenses"""
        query_lower = query.lower()
        
        # Check for summary requests
        if any(keyword in query_lower for keyword in ["आज का हिसाब", "आज का खर्च", "आज कितना"]):
            return self.get_today_summary(user_id)
            
        # Check for monthly summary
        if any(keyword in query_lower for keyword in ["महीने का हिसाब", "महीने का खर्च", "इस महीने"]):
            return self.get_monthly_summary(user_id)
            
        # Check for previous month
        if any(keyword in query_lower for keyword in ["पिछले महीने", "पिछला महीना"]):
            return self.get_monthly_summary(user_id, 1)
            
        # General query - try to parse as a transaction
        return self.add_transaction(user_id, query)

# Example usage
def handle_expense_command(command, user_id="demo_user"):
    """Process expense tracking command"""
    if not os.path.exists("expense_data"):
        os.makedirs("expense_data")
        
    tracker = ExpenseTracker()
    
    # Create user if not exists
    user_file = os.path.join("expense_data", f"{user_id}_expenses.json")
    if not os.path.exists(user_file):
        tracker.create_user(user_id)
    
    return tracker.handle_query(user_id, command)

# Integration function for main.py
def process_expense_command(command, user_id="default_user"):
    """Process expense command from main"""
    try:
        response = handle_expense_command(command, user_id)
        if isinstance(response, tuple):
            return response[0]  # Return just the message
        return response
    except Exception as e:
        logger.error(f"Error processing expense command: {str(e)}")
        return "खर्चा जोड़ने में समस्या आई, कृपया फिर से कोशिश करें"