from flask import Flask, render_template, request
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_network_ip', methods=['GET', 'POST'])
def select_network_ip():
    if request.method == 'POST':
        target_ip = request.form['network_ip']
        return f"Selected network IP: {target_ip}"
    return render_template('select_network_ip.html')

@app.route('/select_machine_ip', methods=['GET', 'POST'])
def select_machine_ip():
    if request.method == 'POST':
        target_ip = request.form['machine_ip']
        return f"Selected machine IP: {target_ip}"
    return render_template('select_machine_ip.html')

# Define other routes and logic similarly

def start_flask():
    app.run(debug=True)

def main():
    # Check if the user wants to run the Flask application
    if len(sys.argv) > 1 and sys.argv[1] == 'flask':
        start_flask()
    else:
        print("Flask application not started. Use 'flask' as a command-line argument to start the Flask app.")

if __name__ == "__main__":
    main()
