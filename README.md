使用docker compose 部署
docker-compose.yaml 配置文件
```
services:
  memos:
    container_name: memos
    environment:
      - MEMOS_API=https://memos.imsun.org/api/v1/memo #Memos的API地址,自行修改
    image: jkjoy/qq2memos:latest  
    volumes:  
      - "./data:/app/data"  
    restart: always
    ports:
      - 8080:8080
```
使用环境变量的方式设置memos端点的位置


** 此处的MEMOS_API支持memos v0.15.0以上使用token认证的版本,端口地址根据版本情况自行更改 **

例如 

v0.18.1版本 使用/api/v1/memo

v0.20.0版本以上使用/api/v1/memos

## 部署QQ机器人

此处以docker-compose的方式部署

```
services:
  napcat:
    environment:
      - ACCOUNT=10000 #QQ机器人号码,自行修改
      - WS_ENABLE=true
      - NAPCAT_UID=0
      - NAPCAT_GID=0
    ports:
      - 3001:3001 
      - 6099:6099
      - 3000:3000
    restart: always
    image: mlikiowa/napcat-docker:latest
    volumes:
      - "./QQ:/app/.config/QQ"
      - "./config:/app/napcat/config"
```