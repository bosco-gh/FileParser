from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from controllers.log_controller import LogController
import os
import requests
from helpers.log_db_helper import count_info_logs, count_logs_by_level, get_log_level_counts, get_log_level_heatmap, get_log_trendline

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
UPLOAD_FOLDER = r'C:\Bosco\Work\Visual Studio\FileParser\uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_log():
    if request.method == 'POST':
        if 'logfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['logfile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            controller = LogController()
            controller.process_log_file(filepath)
            flash('Log file processed and data inserted into SQLite database.')
            return redirect(url_for('upload_log'))
    return render_template('upload_log.html')

@app.route('/log-level-counts')
def log_level_counts():
    data = get_log_level_counts()
    return jsonify(data)

@app.route('/log-level-heatmap')
def log_level_heatmap():
    data = get_log_level_heatmap()
    return jsonify(data)

@app.route('/log-trendline')
def log_trendline():
    data = get_log_trendline()
    return jsonify(data)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    ai_response = get_mercury_response(user_message)
    return jsonify({'response': ai_response})

def get_mercury_response(message):
    print("Received message:", message)
    # Custom responses for specific text
    if message and "hello" in message.lower():
        return "Hi! How can I help you today?"
    if message and "log file" in message.lower():
        return "You can upload your log file using the form above."
    if message and "how many info logs" in message.lower():
        count = count_logs_by_level('INFO')
        sql = "SELECT COUNT(*) FROM log_entries WHERE level = 'INFO';"
        return f"There are {count} INFO logs in the database.\n\nSQL Suggestion:\n{sql}"
    if message and "how many error logs" in message.lower():
        count = count_logs_by_level('ERROR')
        sql = "SELECT COUNT(*) FROM log_entries WHERE level = 'ERROR';"
        return f"There are {count} ERROR logs in the database.\n\nSQL Suggestion:\n{sql}"
    # Mercury LLM fallback
    api_key = 'sk_d71015630edd56f887cf3c6aebfc1a0a'  # Replace with your real API key
    endpoint = 'https://api.inceptionlabs.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'messages': [
            {'role': 'user', 'content': message}
        ],
        'model': 'mercury-2'
    }
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('choices', [{}])[0].get('message', {}).get('content', 'No response from AI.')
    except Exception as e:
        return f'Error contacting Mercury LLM: {e}'

if __name__ == '__main__':
    app.run(debug=True)
