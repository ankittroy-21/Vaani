import datetime

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