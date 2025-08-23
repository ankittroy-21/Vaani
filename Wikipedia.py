import wikipedia
import random
import Config
from Voice_tool import bolo_stream

def search_wikipedia(command, bolo_func):
    query = command
    for phrase in Config.wikipedia_junk:
        query = query.replace(phrase, "")
    query = query.strip()
    
    if not query:
        bolo_func("आप विकिपीडिया पर क्या खोजना चाहते हैं?")
        return

    search_message = random.choice(Config.wikipedia_search_responses).format(query)
    bolo_func(search_message)

    try:
        wikipedia.set_lang("hi")
        full_summary = wikipedia.summary(query, sentences=10)

        summary_intro = random.choice(Config.wikipedia_summary_responses)
        print(summary_intro)
        bolo_func(summary_intro)
        print(full_summary)
        bolo_stream(full_summary)

    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:3])
        bolo_func(f"इस विषय पर एक से ज़्यादा परिणाम हैं। आप इनमें से क्या मतलब रखते हैं? {options}")
    except wikipedia.exceptions.PageError:
        bolo_func(f"माफ़ कीजिए, मुझे '{query}' के लिए कोई विकिपीडिया पेज नहीं मिला।")
    except Exception as e:
        print(f"An unexpected Wikipedia error occurred: {e}")
        bolo_func("माफ़ कीजिए, विकिपीडिया पर खोजते समय एक त्रुटि हुई।")