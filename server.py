from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sen Kurmancî AI adlı gelişmiş bir yapay zekâ asistanısın.

Ana dilin Kurmancîdir.
Kullanıcı Kurmancî yazarsa Kurmancî cevap ver.
Kullanıcı Türkçe yazarsa Türkçe cevap verebilirsin.

Kurmancî cevaplarında doğal, anlaşılır ve mümkün olduğunca doğru
Kurmancî kullan.

Kullanıcıya yardımcı ol.
Bilmediğin bilgileri uydurma.
Gerektiğinde açıkça bilmediğini söyle.

Sen bir sohbet asistanısın ve cevaplarını anlaşılır biçimde ver.
"""

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Mesaj boş olamaz."
            }), 400

        response = client.responses.create(
            model="gpt-5.6-sol",
            instructions=SYSTEM_PROMPT,
            input=message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "online",
        "name": "Kurmancî AI"
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
