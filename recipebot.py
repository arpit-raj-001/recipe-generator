from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from groq import Groq
import os
import json
import traceback
import time

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Check for API tokens
hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACEHUB_API_TOKEN')
groq_token = os.getenv('GROQ_API_KEY')

if not hf_token:
    print("WARNING: HF_TOKEN not found in .env file!")
if not groq_token:
    print("WARNING: GROQ_API_KEY not found in .env file!")

# Initialize HuggingFace model
llm_hf = HuggingFaceEndpoint(
    repo_id="HuggingFaceTB/SmolLM3-3B",
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.7,
)
model_hf = ChatHuggingFace(llm=llm_hf)

# Initialize Groq client
groq_client = Groq(api_key=groq_token) if groq_token else None


@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    try:
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        model_choice = data.get('model', 'huggingface').lower()

        if not dish_name:
            return jsonify({'error': 'Dish name is required'}), 400

        prompt = f"""Generate a detailed recipe in JSON format for {dish_name}.
Return only valid JSON with fields:
- name
- description
- ingredients (array of strings)
- instructions (array of strings)
- prep_time
- cook_time
- servings
- difficulty
Do not include any extra text, only the JSON object."""

        # Track generation time
        start_time = time.time()
        
        # Select and call the model
        if model_choice == 'groq':
            if not groq_client:
                return jsonify({'error': 'Groq API key not configured'}), 400
            
            chat_completion = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            generated_text = chat_completion.choices[0].message.content
            model_name = "Groq OpenAI GPT-OSS-20B"
            
        else:  # huggingface
            result = model_hf.invoke(prompt)
            generated_text = result.content
            model_name = "HuggingFace SmolLM3-3B"
        
        end_time = time.time()
        generation_time = round(end_time - start_time, 2)

        # Try to parse JSON
        try:
            # Try to extract JSON from the response
            json_start = generated_text.find('{')
            json_end = generated_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = generated_text[json_start:json_end]
                recipe_json = json.loads(json_str)
            else:
                recipe_json = json.loads(generated_text)
                
        except json.JSONDecodeError:
            # If parsing fails, fallback to raw response
            recipe_json = {
                "name": dish_name,
                "description": "Recipe generated",
                "ingredients": ["See raw response below"],
                "instructions": ["See raw response below"],
                "prep_time": "Varies",
                "cook_time": "Varies",
                "servings": "4",
                "difficulty": "medium",
                "raw_response": generated_text,
                "note": "The model response could not be parsed as JSON"
            }

        # Add metadata
        recipe_json['model_used'] = model_name
        recipe_json['generation_time'] = f"{generation_time}s"

        return jsonify({
            'recipe': recipe_json,
            'generation_time': generation_time,
            'model_used': model_name
        }), 200

    except Exception as e:
        print(f"\nERROR: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'hf_token_present': bool(hf_token),
        'groq_token_present': bool(groq_token),
        'models_available': {
            'huggingface': bool(hf_token),
            'groq': bool(groq_token)
        },
        'hf_model': "HuggingFaceTB/SmolLM3-3B",
        'groq_model': "openai/gpt-oss-20b"
    })


@app.route('/')
def home():
    return send_from_directory('.', 'recipebot.html')
    
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Flask Server with Multi-Model Support")
    print("="*60)
    print(f"✅ HuggingFace Model: {'Available' if hf_token else 'NOT CONFIGURED'}")
    print(f"✅ Groq Model: {'Available' if groq_token else 'NOT CONFIGURED'}")
    print("="*60 + "\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
