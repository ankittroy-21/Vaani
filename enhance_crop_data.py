"""
Automated Crop Data Enhancement Tool
Enhances all crop JSON files to be suitable for illiterate farmers
Adds simple language, voice-friendly content, and practical guidance
"""

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CropDataEnhancer:
    def __init__(self):
        """Initialize the enhancer with Gemini API"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found")
    
    def generate_simple_guide(self, crop_name, original_data):
        """Generate simple farmer's guide using Gemini"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            तुम एक अनुभवी कृषि सलाहकार हो जो अनपढ़ किसानों को सरल हिंदी में समझाता है।
            
            फसल: {crop_name}
            मूल जानकारी: {json.dumps(original_data, ensure_ascii=False)[:1000]}
            
            कृपया निम्नलिखित सेक्शन बनाओ (बहुत ही आसान हिंदी में):
            
            1. सरल_परिचय (3-4 वाक्य - क्या है, क्यों उगाएं, क्या फायदा)
            2. कब_लगाएं (कौन सा महीना सबसे अच्छा)
            3. कैसे_लगाएं (step by step - बीज, दूरी, गहराई)
            4. पानी_कब_दें (कितने दिन में, कितना पानी)
            5. खाद_कब_दें (कौन सी खाद, कब दें)
            6. फसल_कब_तैयार (कितने दिन बाद, कैसे पता चलेगा)
            7. आम_समस्याएं (3 problems और solutions)
            8. कमाई_कितनी (प्रति बीघा खर्च और कमाई)
            
            JSON format में return करो। बहुत ही सरल भाषा जो एक अनपढ़ किसान समझ सके।
            
            Response:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Extract JSON from response
                text = response.text.strip()
                # Remove markdown code blocks if present
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                text = text.strip()
                
                try:
                    return json.loads(text)
                except:
                    print(f"Could not parse JSON for {crop_name}")
                    return None
            
            return None
            
        except Exception as e:
            print(f"Error generating guide for {crop_name}: {e}")
            return None
    
    def create_monthly_calendar(self, crop_name):
        """Generate month-wise farming calendar"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            {crop_name} फसल के लिए 12 महीनों का कैलेंडर बनाओ।
            
            हर महीने के लिए बताओ:
            - इस महीने क्या करें (1 line)
            
            बहुत सरल हिंदी में, जैसे किसान को बोलकर समझा रहे हो।
            
            JSON format:
            {{
                "जनवरी": "...",
                "फरवरी": "...",
                ...
            }}
            
            Response:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                text = response.text.strip()
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                text = text.strip()
                
                try:
                    return json.loads(text)
                except:
                    return None
            
            return None
            
        except Exception as e:
            print(f"Error generating calendar for {crop_name}: {e}")
            return None
    
    def create_problem_solutions(self, crop_name):
        """Generate common problems and solutions"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            {crop_name} फसल में आने वाली 5 आम समस्याएं और उनके आसान समाधान बताओ।
            
            हर समस्या के लिए:
            - क्या_हुआ: समस्या का विवरण (1 line)
            - क्यों_हुआ: कारण (1 line)
            - क्या_करें: समाधान (2-3 lines, step by step)
            
            बहुत सरल हिंदी में।
            
            JSON format:
            {{
                "समस्या_1": {{
                    "क्या_हुआ": "...",
                    "क्यों_हुआ": "...",
                    "क्या_करें": "..."
                }},
                ...
            }}
            
            Response:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                text = response.text.strip()
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                text = text.strip()
                
                try:
                    return json.loads(text)
                except:
                    return None
            
            return None
            
        except Exception as e:
            print(f"Error generating problems for {crop_name}: {e}")
            return None
    
    def create_earnings_guide(self, crop_name):
        """Generate earnings and market information"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            {crop_name} की खेती से कमाई के बारे में बताओ:
            
            1. कुल_खर्च: प्रति बीघा खर्च (बीज, खाद, मजदूरी)
            2. कुल_उपज: प्रति बीघा कितना मिलेगा
            3. बाजार_भाव: औसत भाव
            4. कुल_कमाई: खर्च घटाकर बचत
            5. कहाँ_बेचें: मंडी, व्यापारी, या सीधे बाजार
            6. ज़्यादा_कमाई_के_लिए: tips
            
            बहुत सरल हिंदी में, रुपयों में।
            
            JSON format में return करो।
            
            Response:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                text = response.text.strip()
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                text = text.strip()
                
                try:
                    return json.loads(text)
                except:
                    return None
            
            return None
            
        except Exception as e:
            print(f"Error generating earnings for {crop_name}: {e}")
            return None
    
    def create_practical_tips(self, crop_name):
        """Generate practical tips for farmers"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            {crop_name} की खेती के लिए 7 ज़रूरी टिप्स बताओ।
            
            हर tip 1 line में, बहुत practical और useful।
            
            JSON format:
            {{
                "टिप_1": "...",
                "टिप_2": "...",
                ...
                "टिप_7": "..."
            }}
            
            Response:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                text = response.text.strip()
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                text = text.strip()
                
                try:
                    return json.loads(text)
                except:
                    return None
            
            return None
            
        except Exception as e:
            print(f"Error generating tips for {crop_name}: {e}")
            return None
    
    def enhance_crop_file(self, crop_file_path):
        """Enhance a single crop file"""
        crop_name = os.path.basename(crop_file_path).replace('.json', '')
        print(f"\n{'='*70}")
        print(f"Enhancing: {crop_name}")
        print(f"{'='*70}")
        
        # Read original data
        try:
            with open(crop_file_path, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
        except Exception as e:
            print(f"Error reading {crop_file_path}: {e}")
            return False
        
        # Generate enhanced sections
        print("Generating simple guide...")
        simple_guide = self.generate_simple_guide(crop_name, original_data)
        
        print("Generating monthly calendar...")
        monthly_calendar = self.create_monthly_calendar(crop_name)
        
        print("Generating problem solutions...")
        problems = self.create_problem_solutions(crop_name)
        
        print("Generating earnings guide...")
        earnings = self.create_earnings_guide(crop_name)
        
        print("Generating practical tips...")
        tips = self.create_practical_tips(crop_name)
        
        # Merge with original data
        enhanced_data = {
            "फसल_का_नाम": crop_name,
            **original_data
        }
        
        # Add enhanced sections at the beginning
        if simple_guide:
            enhanced_data = {**simple_guide, **enhanced_data}
        
        if monthly_calendar:
            enhanced_data["महीने_के_हिसाब_से_काम"] = monthly_calendar
        
        if problems:
            enhanced_data["आम_समस्याएं_और_समाधान"] = problems
        
        if earnings:
            enhanced_data["कमाई_और_बाजार"] = earnings
        
        if tips:
            enhanced_data["याद_रखने_योग्य_बातें"] = tips
        
        # Save enhanced data
        try:
            with open(crop_file_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, ensure_ascii=False, indent=4)
            print(f"✅ Successfully enhanced {crop_name}")
            return True
        except Exception as e:
            print(f"❌ Error saving {crop_file_path}: {e}")
            return False
    
    def enhance_all_crops(self, crop_data_dir):
        """Enhance all crop files in the directory"""
        if not self.model:
            print("❌ Gemini API not configured. Please add GEMINI_API_KEY to .env file")
            return
        
        print("=" * 70)
        print("🌾 Starting Crop Data Enhancement for Illiterate Farmers")
        print("=" * 70)
        
        crop_files = [f for f in os.listdir(crop_data_dir) if f.endswith('.json')]
        total = len(crop_files)
        
        print(f"\nFound {total} crop files to enhance")
        print("This will take some time...\n")
        
        success_count = 0
        for i, crop_file in enumerate(crop_files, 1):
            print(f"\nProgress: {i}/{total}")
            crop_path = os.path.join(crop_data_dir, crop_file)
            
            if self.enhance_crop_file(crop_path):
                success_count += 1
            
            # Small delay to avoid API rate limits
            import time
            time.sleep(2)
        
        print("\n" + "=" * 70)
        print(f"✅ Enhancement Complete!")
        print(f"Successfully enhanced: {success_count}/{total} files")
        print("=" * 70)


if __name__ == "__main__":
    enhancer = CropDataEnhancer()
    
    # Get crop_data directory path
    crop_data_dir = os.path.join(os.path.dirname(__file__), 'crop_data')
    
    if not os.path.exists(crop_data_dir):
        print(f"Error: {crop_data_dir} not found")
        exit(1)
    
    # Enhance all crops
    enhancer.enhance_all_crops(crop_data_dir)
    
    print("\n🎉 All crop data enhanced for illiterate farmers!")
    print("Now farmers can get voice guidance in simple Hindi!")
