import ascii_magic

def generate_ascii_art(text):
    try:
        return ascii_magic.from_text(text, columns=80)
    except Exception as e:
        return f"Error generating ASCII Art: {str(e)}"

def process_query(query):
    return f"Manus AI Agent Response: {query}"
