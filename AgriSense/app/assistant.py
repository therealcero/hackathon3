import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', '')
    text = text.replace('*', '')
    text = text.replace('#', '')
    return text

def generate_response(user_input):
    API_KEY = 'AIzaSyDAx6nGn63u-geHv5T-cCqdLIRqfEz1zaA'
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(user_input)
    return to_markdown(response.text)

if __name__ =="__main__":
    print(generate_response('What is gdp of india in 2003'))