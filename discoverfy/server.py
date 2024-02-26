from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form

        
       

        print("Received form data:", data)
        return "Form submitted successfully"
    else:
        return "Method not allowed"

if __name__ == '__main__':
    app.run(debug=True)
