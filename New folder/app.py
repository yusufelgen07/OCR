from flask import Flask, request, render_template, send_file
from paddleocr import PaddleOCR, draw_ocr
import os
from fpdf import FPDF

ocr = PaddleOCR(lang='en')

app = Flask(__name__)

def text(path):
    result = ocr.ocr(path, cls=False)
    sorted_text = sorted(result[0], key=lambda x: x[0][0][1])
    page = []
    for line in sorted_text:
        page.append(line[1][0])
    page_text = '\n'.join(page)
    return page_text

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route("/submit2", methods=['GET', 'POST'])
def preview():
    global text1
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = img.filename
        img.save(img_path)

        text1 = text(img_path)
    return (render_template("index.html",  prediction = text1, img_path = img_path),text1)
@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    global text1
    if request.method == 'POST':
        file_name = "output.txt"
        file_path = os.path.abspath(file_name)
        with open(file_path, "w") as file:
            file.write(text1)
        return send_file(file_path, as_attachment=True, download_name=file_name)

    return render_template("index.html")

@app.route("/submit1", methods=['GET', 'POST'])
def get_output1():
    if request.method == 'POST':
        pdf = FPDF()

        uploaded_files = request.files.getlist('my_images')
        for img in uploaded_files:
            img_path = img.filename
            img.save(img_path)
            text1 = text(img_path)
            pdf.add_page()
            pdf.set_font("Arial", size=8)
            pdf.multi_cell(w=0, h=5, txt=text1, align="L")

        file_name = "output.pdf"
        file_path = os.path.abspath(file_name)
        pdf.output(file_path)
        return send_file(file_path, as_attachment=True, download_name=file_name)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False)
