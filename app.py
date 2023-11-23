from flask import Flask, render_template, request, jsonify
import openai
import uuid

app = Flask(__name__)

# Set your OpenAI API key
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Set your OpenAI API key
openai.api_key = get_api_key('API_KEY')

# In-memory storage for conversation states
conversations = {}

@app.route('/')
def index():
    # Generate a unique session ID for each user
    session_id = str(uuid.uuid4())
    return render_template('index.html', session_id=session_id)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    session_id = data['session_id']
    user_input = data['user_input']

    if session_id not in conversations:
        conversations[session_id] = []

    # Append user message to the conversation
    conversations[session_id].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # or any other model version you're using
            messages=conversations[session_id]
        )
        gpt_response = response.choices[0].message['content']
        conversations[session_id].append({"role": "assistant", "content": gpt_response})

        return jsonify({"response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
