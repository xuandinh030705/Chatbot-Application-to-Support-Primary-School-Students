# 1. Chọn base image Python
FROM python:3.11-slim

# 2. Set working directory trong container
WORKDIR /app

# 3. Copy requirements vào container
COPY requirements.txt .

# 4. Cài đặt dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ code backend vào container
COPY . ./

# 6. Expose port mà Uvicorn chạy
EXPOSE 8000

# 7. Command để chạy FastAPI với Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
