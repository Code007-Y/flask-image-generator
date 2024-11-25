from flask import Flask, request, jsonify, send_file, render_template
import requests

app = Flask(__name__)

def generate_image(prompt):
    url = "https://api.fireworks.ai/inference/v1/workflows/accounts/fireworks/models/stable-diffusion-3p5-large/text_to_image"
    headers = {
        "Content-Type": "application/json",
        "Accept": "image/jpeg",
        "Authorization": "Bearer fw_3ZnYq1TzXfoPWEB3y8ChYtVr"
    }
    data = {
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "guidance_scale": 4.5,
        "num_inference_steps": 28
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        image_filename = "generated_image.jpg"
        with open(image_filename, "wb") as f:
            f.write(response.content)
        return image_filename
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    image_filename = generate_image(prompt)
    if image_filename:
        return send_file(image_filename, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == '__main__':
    app.run(debug=True)
