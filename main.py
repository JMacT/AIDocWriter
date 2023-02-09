from flask import Flask, render_template, request, send_from_directory, url_for
import openai
import requests
import os
import concurrent.futures
import mimetypes
import textract
from werkzeug.utils import redirect

app = Flask(__name__)
app.debug == True
api_key = openai.api_key = "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"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload(rewritten_paragraphs=None):
    if request.method == "POST":
        file = request.files["file"]
        contents = file.read().decode("utf-8")
        paragraphs = contents.split("\n")

        def rewrite_paragraph(paragraph):
            prompt = f"Rewrite the following paragraph with a new purpose:\n{paragraph}"
            response = requests.post(
                "https://api.openai.com/v1/engines/davinci/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json={
                    "prompt": prompt,
                    "temperature": 0.5,
                    "max_tokens": 1024,
                    "stream":True
                }
            ).json()
            return response["choices"][0]["text"]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_paragraph = {executor.submit(rewrite_paragraph, paragraph): paragraph for paragraph in paragraphs}
            for future in concurrent.futures.as_completed(future_to_paragraph):
                rewritten_paragraph = future.result()
                rewritten_paragraphs.append(rewritten_paragraph)
        rewritten_text = "\n".join(rewritten_paragraphs)
        with open("output_document.txt", "w") as f:
            f.write(rewritten_text)
        return redirect(url_for('download', filename='output_document.txt'))
    return """
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    """

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(directory='', filename=filename, as_attachment=True)

@app.route("/response", methods=["POST"])
def response():
    prompt = request.form["prompt"]
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        stream=True
    )
    response = completions.choices[0].text
    return render_template("response.html", response=response)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
# Start ngrok tunnel
    os.system("ngrok http 5000 -authtoken 2KxzhjIYrFN5grFJdxteP47iBsP_679weeuxvWxX6cjau53n7")
