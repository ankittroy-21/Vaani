import wikipedia
import random
import Config

def search_wikipedia(command, bolo_func):
    query = command
    for phrase in Config.wikipedia_junk:
        query = query.replace(phrase, "")
    query = query.strip()
    
    if not query:
        bolo_func("आप विकिपीडिया पर क्या खोजना चाहते हैं?")
        return

    # Randomized acknowledgement before starting the search
    search_message = random.choice(Config.wikipedia_search_responses).format(query)
    bolo_func(search_message)

    try:
        wikipedia.set_lang("hi")
        
        # Get the default summary and take only the first paragraph
        full_summary = wikipedia.summary(query)
        first_paragraph = full_summary.split('\n')[0]

        # Randomized introduction before giving the summary
        summary_intro = random.choice(Config.wikipedia_summary_responses)
        print(summary_intro)
        bolo_func(summary_intro)
        
        # Print and speak only the concise, first-paragraph summary
        print(first_paragraph)
        bolo_func(first_paragraph)

    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:3])
        bolo_func(f"इस विषय पर एक से ज़्यादा परिणाम हैं। आप इनमें से क्या मतलब रखते हैं? {options}")
    except wikipedia.exceptions.PageError:
        bolo_func(f"माफ़ कीजिए, मुझे '{query}' के लिए कोई विकिपीडिया पेज नहीं मिला।")
    except Exception as e:
        print(f"An unexpected Wikipedia error occurred: {e}")
        bolo_func("माफ़ कीजिए, विकिपीडिया पर खोजते समय एक त्रुटि हुई।")