FROM python:3.12.6-slim

WORKDIR /app

COPY ./app /app

# 创建虚拟环境
RUN python -m venv .venv --prompt nonebot2
# 设置环境变量以使用虚拟环境
ENV PATH="/app/.venv/bin:$PATH"
ENV MEMOS_API="https://memos.ee/api/v1/memos"
# 激活虚拟环境并安装依赖
RUN . .venv/bin/activate && \
    pip install nonebot-adapter-console && \
    pip install --no-cache-dir "nonebot2[fastapi]" nb-cli && \
    pip install nonebot-adapter-onebot && \
    pip install httpx

# 暴露端口（如果需要的话）
EXPOSE 8080

# 设置启动命令，使用虚拟环境中的 Python
CMD ["nb","run"]
