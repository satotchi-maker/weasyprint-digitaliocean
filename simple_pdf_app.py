from flask import Flask, request, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
import re

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        html = data.get('html', '<h1>Hello World</h1>')
        
        # Create PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Simple HTML to text conversion
        text = re.sub(r'<[^>]+>', '', html)
        text = text.strip()
        
        # Write text to PDF
        y = height - 100
        for line in text.split('\n'):
            if line.strip():
                p.drawString(50, y, line[:80])  # Max 80 chars per line
                y -= 20
                if y < 50:  # Start new page if needed
                    p.showPage()
                    y = height - 100
        
        p.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='document.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting simple PDF service on http://localhost:5000")
    app.run(host='0.0.0.0', port=8080)
