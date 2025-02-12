from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    
    if request.method == "POST":
        prompt = request.form["prompt"]
        
        try:
            # Generate text response
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are an expert in Jungian dream analysis. Given the following dream description, provide a thoughtful interpretation based on Jungian archetypes, symbols, and the collective unconscious. Explain the possible meanings and psychological significance of the dream."}, 
                          {"role": "user", "content": prompt}],
                temperature=1.2,
                max_tokens=50
            )
            result = response.choices[0].message.content
            
            # Generate image from prompt using DALL·E
            image_response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,  # Using the user's prompt to generate the image
                size="1024x1024",
                n=1
            )
            image_url = image_response.data[0].url  # Extract the generated image URL

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
