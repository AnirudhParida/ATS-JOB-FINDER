from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import io
import google.generativeai as genai
import fitz
from docx import Document


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')


app = Flask(__name__)

#extract text from pdf
def extract_text_from_pdf(pdf_file_stream):
    text = ""
    pdf_document = fitz.open(stream=pdf_file_stream, filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

#extract tezt from docx
def extract_text_from_docx(docx_file_stream):
    document = Document(docx_file_stream)
    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    return text

def extract_skills_section(data):
    prompt = f"Extract the skills section from the following text and provide it in a list format: {data}"
    response = model.generate_content(prompt)
    # Assuming the response object has an attribute `text` or a similar method to access the generated content
    return response.text if hasattr(response, 'text') else response.generate()  # Adjust according to actual method

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/api/resume', methods=['POST'])
def resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.lower().endswith('.pdf') or file.filename.lower().endswith('.docx')):
        try:
            file_stream = io.BytesIO(file.read())
            if file.filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_stream)
            else:
                text = extract_text_from_docx(file_stream)

            response = extract_skills_section(text)
            return jsonify({"response": response.strip().split('\n')})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unsupported file format"}), 400


@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello, World!'})

@app.route('/api', methods=['POST'])
def post():
    data = request.json
    return jsonify({'msg': f'Hello, {data["name"]}!'})

if __name__=="__main__":
    app.run()