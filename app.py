from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from flasgger import Swagger

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Flasgger 설정 추가
swagger = Swagger(app)

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate_text():
    """
    텍스트 생성 API
    ---
    tags:
      - Text Generation
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - prompt
          properties:
            prompt:
              type: string
              description: 텍스트 생성을 위한 프롬프트
            max_tokens:
              type: integer
              description: 생성할 최대 토큰 수
              default: 150
            temperature:
              type: number
              format: float
              description: 생성의 창의성 정도 (0.0 ~ 1.0)
              default: 0.7
    responses:
      200:
        description: 생성된 텍스트 반환
        schema:
          type: object
          properties:
            generated_text:
              type: string
              description: 생성된 텍스트
      400:
        description: 잘못된 요청
      500:
        description: 서버 에러
    """
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 150)
    temperature = data.get('temperature', 0.7)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        generated_text = response.choices[0].message.content
        return jsonify({"generatedText": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True)