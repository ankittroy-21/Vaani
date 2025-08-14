# wikipedia_feature.py
import wikipedia

def search_wikipedia(command, bolo_func):
    """Searches Wikipedia for a query."""
    query = command.replace("विकिपीडिया पर", "").replace("खोजो", "").strip()
    
    if not query:
        bolo_func("आप विकिपीडिया पर क्या खोजना चाहते हैं?")
        return

    bolo_func(f"ठीक है, विकिपीडिया पर {query} खोज रहा हूँ...")

    try:
        wikipedia.set_lang("hi")
        full_summary = wikipedia.summary(query, sentences=3)
        print("विकिपीडिया के अनुसार,")
        bolo_func("विकिपीडिया के अनुसार,")
        print(full_summary)
        bolo_func(full_summary)

    except wikipedia.exceptions.DisambiguationError as e:
        bolo_func(f"इस विषय पर एक से ज़्यादा परिणाम हैं। आप इनमें से क्या मतलब रखते हैं? {', '.join(e.options[:3])}")
    except wikipedia.exceptions.PageError:
        bolo_func(f"माफ़ कीजिए, मुझे '{query}' के लिए कोई विकिपीडिया पेज नहीं मिला।")
    except Exception as e:
        print(f"An unexpected Wikipedia error occurred: {e}")
        bolo_func("माफ़ कीजिए, विकिपीडिया पर खोजते समय एक त्रुटि हुई।")
    