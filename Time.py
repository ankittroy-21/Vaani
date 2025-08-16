import datetime
import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup 
import Config

def current_time(bolo_func):
    """Tells the current time with proper greetings."""
    now = datetime.datetime.now()
    hour = now.hour

    if 4 <= hour < 12:
        time_of_day = "सुबह"
    elif 12 <= hour < 16:
        time_of_day = "दोपहर"
    elif 16 <= hour < 20:
        time_of_day = "शाम"
    else:
        time_of_day = "रात"
        
    response = f"अभी {time_of_day} के {now.strftime('%I:%M')} बजे हैं।"
    bolo_func(response)

def get_date_of_day_in_week(command, bolo_func):
    """
    Tells the date for a specific day.
    """
    now = datetime.datetime.now()
    hindi_days = {
        "सोमवार": 0, "मंगलवार": 1, "बुधवार": 2, "गुरुवार": 3, "शुक्रवार": 4, "शनिवार": 5, "रविवार": 6
    }
    days_in_hindi = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
    months_in_hindi = [
        "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त",
        "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
    ]
    response = ""

    if "आने वाले कल" in command or "कल होगी" in command:
        target_date = now + datetime.timedelta(days=1)
        day_name = days_in_hindi[target_date.weekday()]
        response = f"कल {target_date.day} {months_in_hindi[target_date.month-1]}, {day_name} होगा।"
    elif "कल" in command:
        target_date = now - datetime.timedelta(days=1)
        day_name = days_in_hindi[target_date.weekday()]
        response = f"कल {target_date.day} {months_in_hindi[target_date.month-1]}, {day_name} था।"
    elif "परसों" in command:
        target_date = now + datetime.timedelta(days=2)
        day_name = days_in_hindi[target_date.weekday()]
        response = f"परसों {target_date.day} {months_in_hindi[target_date.month-1]}, {day_name} होगा।"
    elif "आज" in command:
        day_name = days_in_hindi[now.weekday()]
        response = f"आज {now.day} {months_in_hindi[now.month-1]}, {day_name} है।"
    else:
        found_weekday = False
        for day, index in hindi_days.items():
            if day in command:
                days_diff = index - now.weekday()
                if days_diff < 0:
                    days_diff += 7
                target_date = now + datetime.timedelta(days=days_diff)
                response = f"{day} को {target_date.day} {months_in_hindi[target_date.month-1]} तारीख है।"
                found_weekday = True
                break

        if not found_weekday:
            day_name = days_in_hindi[now.weekday()]
            response = f"आज {now.day} {months_in_hindi[now.month-1]}, {day_name} है।"
    bolo_func(response)


def get_day_summary(command, bolo_func):
    """
    Provides a simple summary about a specific date by searching and browsing the web.
    """
    hindi_month_to_num = {
        "जनवरी": 1, "फरवरी": 2, "मार्च": 3, "अप्रैल": 4, "मई": 5, "जून": 6,
        "जुलाई": 7, "अगस्त": 8, "सितंबर": 9, "अक्टूबर": 10, "नवंबर": 11, "दिसंबर": 12
    }
    
    clean_command = command
    for phrase in Config.historical_date_trigger:
        clean_command = clean_command.replace(phrase, "")
    clean_command = clean_command.strip()

    try:
        parts = clean_command.split()
        day = int(parts[0])
        month_hindi = parts[1]
        month = hindi_month_to_num[month_hindi]
        year = int(parts[2])

        target_date = datetime.date(year, month, day)
        days_in_hindi = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
        day_name = days_in_hindi[target_date.weekday()]

        query = f"{day} {month_hindi} {year} का भारत में ऐतिहासिक महत्व"
        
        search_results_urls = list(search(query, num_results=1))
        
        if search_results_urls:
            first_url = search_results_urls[0]
            summary = f"{day} {month_hindi} {year} को {day_name} था। "
            
            try:
                page = requests.get(first_url, timeout=5)
                soup = BeautifulSoup(page.content, 'html.parser')
                
                paragraphs = soup.find_all('p')
                first_meaningful_paragraph = ""
                for p in paragraphs:
                    if len(p.get_text().strip()) > 100:
                        first_meaningful_paragraph = p.get_text().strip()
                        break
                
                if first_meaningful_paragraph:
                    summary += f"इंटरनेट पर मिली जानकारी के अनुसार, {first_meaningful_paragraph}"
                else:
                    summary += "मुझे इस दिन के बारे में कोई विस्तृत जानकारी नहीं मिली।"

            except Exception as browse_error:
                print(f"Error browsing URL {first_url}: {browse_error}")
                summary += "इंटरनेट से जानकारी निकालते समय एक त्रुटि हुई।"

            print(summary)
            bolo_func(summary)
        else:
            bolo_func("माफ़ कीजिए, मुझे इस दिन के बारे में कोई खास जानकारी नहीं मिली।")
            return

    except Exception as e:
        print(f"Error in get_day_summary: {e}")
        bolo_func("मैं इस तारीख को समझ नहीं पायी। कृपया 'दिन महीना साल' के रूप में कहें, जैसे '15 अगस्त 1947'।" )