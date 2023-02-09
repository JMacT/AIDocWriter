from typing import io

from flask import Flask, request, render_template
import openai
import pandas as pd

app = Flask(__name__)

def read_file(filename):
    # Check the file extension
    if filename.endswith(".pdf"):
        # Read the PDF file using the read_pdf function
        data = pd.read_pdf(filename)
    elif filename.endswith(".docx"):
        # Read the Word file using the read_docx function
        data = pd.read_docx(filename)
    elif filename.endswith(".xlsx"):
        data = pd.read_excel(io.BytesIO(filename.read()))
    else:
        # Assume the file is a plain text file and read it using the read_csv function
        data = pd.read_csv(filename)

    return data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            try:
                file_contents = file.read().decode('utf-8', errors='replace')
            except UnicodeDecodeError as e:
                return "Error decoding file: " + str(e)
            except MemoryError as e:
                return "Error reading file into memory: " + str(e)

        openai.api_key = "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"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Rewrite this a-player agreement for a design engineer: " + file_contents,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.5,
        )

        rewritten_text = response["choices"][0]["text"]

        return render_template("rewritten_document.html", content=rewritten_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
