import os
from flask import Flask, render_template, request, jsonify, session
from config import Config
from services.gemini_service import GeminiService
from services.search_service import SearchService
import secrets

app = Flask(__name__)
app.config.from_object(Config)

try:
    Config.validate()
    print("Configuration validated successfully")
except ValueError as e:
    print(f"Configuration error: {e}")
    print("\nPlease check your .env file and ensure all API keys are set.")
    exit(1)

conversations = {}

def get_or_create_conversation(session_id):
    if session_id not in conversations:
        conversations[session_id] = {
            'gemini': GeminiService(),
            'search': SearchService()
        }
    return conversations[session_id]

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Get conversation services
        session_id = session.get('session_id')
        conv = get_or_create_conversation(session_id)
        gemini = conv['gemini']
        search = conv['search']
        
        # Determine if we should search
        should_search = gemini.should_search(user_message)
        search_results = None
        
        if should_search:
            # Perform search
            search_query = search.extract_search_query(user_message)
            search_response = search.search(search_query, num_results=5)
            
            if search_response['success'] and search_response['results']:
                search_results = search_response['results']
        
        # Generate response with Gemini
        result = gemini.generate_response(user_message, search_results)
        
        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'used_search': result['used_search'],
                'search_results': search_results if search_results else [],
                'history_length': result['history_length']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        session_id = session.get('session_id')
        conv = get_or_create_conversation(session_id)
        gemini = conv['gemini']
        
        return jsonify(gemini.get_history())
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    try:
        session_id = session.get('session_id')
        conv = get_or_create_conversation(session_id)
        gemini = conv['gemini']
        
        return jsonify(gemini.clear_history())
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'gemini_configured': bool(Config.GEMINI_API_KEY),
        'search_configured': bool(Config.GOOGLE_SEARCH_API_KEY),
        'active_conversations': len(conversations)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("\n" + "=" * 50)
    print("Flask app starting")
    print(f"Listening on 0.0.0.0:{port}")
    print("=" * 50 + "\n")

    app.run(host="0.0.0.0", port=port)