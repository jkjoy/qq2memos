FROM python:3.12.6-slim

WORKDIR /app

COPY ./ /app

RUN rm -rf /app/.venv
# 创建虚拟环境
RUN python -m venv .venv --prompt nonebot2
# 设置环境变量以使用虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 激活虚拟环境并安装依赖
RUN . .venv/bin/activate && \
    pip install nonebot-adapter-console && \
    pip install --no-cache-dir "nonebot2[fastapi]" nb-cli && \
    pip install nonebot-adapter-onebot && \
    pip install httpx

# 暴露端口（如果需要的话）
EXPOSE 8080

# 设置启动命令，使用虚拟环境中的 Python
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8080"]