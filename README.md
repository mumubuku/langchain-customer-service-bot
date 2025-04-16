# LangChain Customer Service Bot

一个基于 LangChain + FastAPI 构建的企业级本地客服问答系统，支持多轮对话、文档上传、智能问答、上下文记忆和知识库刷新。

---

## 🚀 快速启动

### ✅ 安装依赖
```bash
pip install -r requirements.txt
```

### ▶️ 启动服务
```bash
python main.py
```

服务将启动在 `http://localhost:8000`

---

## 📦 API 接口一览

### 1. 提问问答
```
POST /ask
```
请求体：
```json
{
  "user_id": "u123",
  "question": "如何申请退款？"
}
```

### 2. 获取历史记录
```
GET /history/{user_id}
```
返回该用户所有历史问答。

### 3. 上传 PDF 文档
```
POST /upload
```
表单字段：`file`

### 4. 获取上传的所有文档
```
GET /docs
```

### 5. 删除指定 PDF 文件
```
POST /docs/delete
```
表单字段：`filename`

### 6. 重建向量索引
```
POST /refresh
```
用于新增文档后手动刷新向量库。

### 7. 查看系统状态
```
GET /status
```
返回文档数量、最近更新时间戳等。

### 8. 重置用户上下文记忆
```
POST /user/reset
```
表单字段：`user_id`

---

## 🧠 技术选型
- **LangChain**：智能问答、检索增强生成（RAG）
- **FastAPI**：高性能异步 API 服务
- **FAISS**：本地向量数据库
- **PDFMiner**：PDF 文档解析
- **HuggingFace Embeddings**：文本向量嵌入模型（`BAAI/bge-small-zh-v1.5`）
- **DeepSeek Chat API**：大模型问答（兼容 OpenAI 接口）

---

## 📁 项目结构
```
├── main.py                    # 启动入口
├── app/
│   ├── api.py                # API 接口
│   ├── config.py             # 配置项
│   ├── langchain_pipeline.py# QA 主流程
│   ├── knowledge_loader.py   # 文档加载器
├── data/docs/                # PDF 文件存放目录
├── data/vectorstore/         # FAISS 向量库文件
├── data/logs/                # 用户历史日志
├── requirements.txt
```

---

## 🛡️ 注意事项
- 默认文档只支持 PDF
- `DEEPSEEK_API_KEY` 可写入 `.env` 或系统环境变量
- 默认模型为 DeepSeek Chat，如需替换支持 OpenAI 格式的其他模型

---

## 🧩 TODO（可扩展方向）
- [ ] Web 可视化前端（上传 + 聊天 + 历史）
- [ ] 支持更多文档类型（txt、docx）
- [ ] 多人协作权限控制
- [ ] 向量库热更新 / 增量更新
- [ ] Docker 部署打包

---

欢迎使用本地私有化智能客服机器人！

