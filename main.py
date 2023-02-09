from flask import Flask, request, render_template
import openai

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        contents = file.read().decode("utf-8")

        openai.api_key = "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"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Rewrite this a-player agreement for a design engineer: " + contents,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )

        rewritten_text = response["choices"][0]["text"]

        return render_template("rewritten_document.html", content=rewritten_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
