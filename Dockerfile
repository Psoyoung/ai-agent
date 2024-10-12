# 베이스 이미지 선택
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN pip install --no-cache-dir --upgrade pip

# 요구사항 파일 복사 및 패키지 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# 환경 변수 설정 (필요한 경우)
ENV PORT=5000

# 컨테이너 실행 시 실행할 명령어
CMD ["python", "app.py"]
