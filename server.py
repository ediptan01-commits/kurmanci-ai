from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# GitHub Pages gibi farklı bir adresten gelen istekleri kabul et
CORS(app)

# OpenAI API anahtarını Render Environment Variables'dan al
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY bulunamadı.")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
Sen Kurmancî AI adlı gelişmiş bir yapay zekâ asistanısın.

Ana dilin Kurmancîdir.

Kurallar:
- Kullanıcı Kurmancî yazarsa doğal ve anlaşılır Kurmancî cevap ver.
- Kullanıcı Türkçe yazarsa Türkçe cevap verebilirsin.
- Kullanıcı başka bir dil kullanırsa o dilde cevap verebilirsin.
- Kurmancî kullanırken mümkün olduğunca doğru ve doğal dil kullan.
- Bilmediğin bilgileri uydurma.
- Kullanıcıya açık, faydalı ve anlaşılır cevaplar ver.
- Gerektiğinde örnekler ve adım adım açıklamalar sun.
- Kullanıcının sorusunun bağlamını dikkate al.
"""

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "name": "Kurmancî AI"
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
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
    app.logger.exception("CHAT HATASI")
    return jsonify({
        "error": str(e)
    }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )
