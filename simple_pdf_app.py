from flask import Flask, request, make_response, jsonify
from weasyprint import HTML

app = Flask(__name__)

# This is the health check endpoint Render uses
@app.route('/')
def health_check():
    return "WeasyPrint service is running."

# This is the main PDF conversion endpoint
@app.route('/convert', methods=['POST'])
def convert():
    # 1. Ensure the request has JSON data
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 400

    data = request.get_json()

    # 2. Check for the 'html' key in the JSON
    if 'html' not in data or not data['html']:
        return jsonify({'error': 'Missing or empty "html" key in JSON payload'}), 400

    html_content = data['html']

    # 3. Try to render the HTML into a PDF
    try:
        # This is the core logic: it tells WeasyPrint to parse the incoming string as HTML
        pdf_bytes = HTML(string=html_content).write_pdf()

        # 4. Create a valid PDF response to send back
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response

    except Exception as e:
        # 5. If WeasyPrint fails, return a detailed error
        print(f"Error generating PDF: {e}") # This will show up in your Render logs
        return jsonify({'error': 'Failed to generate PDF', 'details': str(e)}), 500

# This makes the app runnable for Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
