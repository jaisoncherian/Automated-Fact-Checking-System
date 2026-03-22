from flask import Flask, render_template
import os

app = Flask(__name__, 
    static_folder=os.path.join(os.path.dirname(__file__), ''),
    template_folder=os.path.join(os.path.dirname(__file__), '')
)

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("🚀 VeriNews AI Landing Page")
    print("📍 Open: http://localhost:5000")
    app.run(debug=True, port=5000)
