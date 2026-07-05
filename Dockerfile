FROM python:3.11-slim

WORKDIR /app

# 先复制依赖文件（缓存优化）
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# 再复制全部代码
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
