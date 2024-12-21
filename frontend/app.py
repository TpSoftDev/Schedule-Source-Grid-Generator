from flask import Flask, render_template, request

app = Flask(__name__)

# Global variable to store the employee ID
employee_external_id = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global employee_external_id
    
    if request.method == 'POST':
        employee_external_id = request.form.get('employee_id')
        print(f"Received Employee ID: {employee_external_id}")
        # You can now use this ID in your existing API code
        return f"Received Employee ID: {employee_external_id}"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
