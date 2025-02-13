from flask import Flask, render_template, request, send_file
import pdfplumber
import pandas as pd
import os
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        return {'error': 'No file uploaded'}, 400

    pdf_file = request.files['pdf']
    if not pdf_file.filename.lower().endswith('.pdf'):
        return {'error': 'Invalid file type'}, 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save PDF
            pdf_path = os.path.join(temp_dir, 'input.pdf')
            pdf_file.save(pdf_path)
            
            # Extract text from PDF
            data = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        data.append(text.split('\n'))
            
            # Create Excel file
            df = pd.DataFrame(data)
            excel_path = os.path.join(temp_dir, 'output.xlsx')
            df.to_excel(excel_path, index=False)
            
            return send_file(excel_path, as_attachment=True, download_name='converted.xlsx')

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)