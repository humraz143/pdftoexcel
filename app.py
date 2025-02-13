from flask import Flask, render_template, request, send_file
import pdfplumber
import pandas as pd
import os

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle file upload and conversion
@app.route('/convert', methods=['POST'])
def convert():
    # Get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Save the file temporarily
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        # Extract text from PDF
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text())

        # Convert text to Excel
        df = pd.DataFrame(text, columns=['Text'])
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)

        # Send the Excel file to the user
        return send_file(excel_file, as_attachment=True)

    return "No file uploaded!"

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Get the port from the environment variable (provided by Render)
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 for local development

    # Run the app on 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=port)
