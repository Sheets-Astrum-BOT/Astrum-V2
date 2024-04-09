import re
import aiohttp

from flask import Flask, request, jsonify

import google.generativeai as genai

genai.configure(api_key='AIzaSyDbd7pQNZRnbG7dbmEIGLhgOrDszwQ6Ctw')

text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}

safety_settings = [{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
}]

text_model = genai.GenerativeModel(model_name="gemini-pro",
                                   generation_config=text_generation_config,
                                   safety_settings=safety_settings)

image_model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                    generation_config=image_generation_config,
                                    safety_settings=safety_settings)

message_history = {}

app = Flask(__name__)

@app.route('/generate-response', methods=['POST'])
async def generate_response():
    data = request.json

    if 'channel_id' not in data or 'input_text' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    channel_id = data['channel_id']
    input_text = data['input_text']
    image_data = data.get('image_data')

    try:
        if image_data:
            response_text = await generate_response_with_image_and_text(image_data, input_text)
        else:
            response_text = await generate_response_with_text(channel_id, input_text)

        return jsonify({'response': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


async def generate_response_with_text(channel_id, input_text):
    cleaned_text = clean_discord_message(input_text)

    if not (channel_id in message_history):
        message_history[channel_id] = text_model.start_chat(history=[])
    response = message_history[channel_id].send_message(cleaned_text)
    return response.text

async def generate_response_with_image_and_text(image_data, text):
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    prompt_parts = [
        image_parts[0], f"\n{text if text else 'What is this a picture of?'}"
    ]

    response = image_model.generate_content(prompt_parts)
    if (response._error):
        return "❌" + str(response._error)
    return response.text

def clean_discord_message(input_string):
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8885',debug=True)
