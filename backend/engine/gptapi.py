import openai
from django.conf import settings
import re
# Ensure that OPENAI_API_KEY is correctly configured in your Django settings

OPENAI_API_KEY = settings.OPENAI_API_KEY
UNREAL_ENGINE_ENDPOINT = settings.UNREAL_ENGINE_ENDPOINT
GPT_MODEL = "gpt-3.5-turbo-0613"

def generate_news_response(user_prompt):
    # Construct the conversation prompt
    prompt = f'''I am a newscaster from storyloomai, reporting on breaking news. 
            Your task is to provide the latest updates on the current situation: "{user_prompt}".
            Ensure to cover key developments, include relevant details, keep each sentence as short as possible, and maintain a professional tone in your script.
            Begin the news with "I am a newscaster from storyloomai.".
        '''
    # Generate response using GPT-3.5
    try:
        openai.api_key = OPENAI_API_KEY
        message = [{"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=message,
            max_tokens=150,
            temperature=1.0
        )
        generated_news = response.choices[0].message.content
        # Remove "\n" characters
        cleaned_text = generated_news.replace("\n", "")

        # Split the text into sentences based on common sentence-ending punctuation marks
        sentences = cleaned_text.split(". ")
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        updated_sentences = sentences[:-1]
        print(updated_sentences)
        # Add a closing sentence to the news
        updated_sentences.append("As soon as the latest news comes in, we will let you know. Here is Storyloomai broadcasting station. Thank you.")
        return updated_sentences
    except Exception as e:
        # Handle API request error here (e.g., log the error)
        print(f"Error generating news response: {str(e)}")
        return []
