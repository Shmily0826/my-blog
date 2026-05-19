---
title: 'myproject1'
description: 'Prompt2Video(CS732)'
pubDate: 'May 14 2026'
heroImage: '../../assets/posts/blog-placeholder-3.jpg'

---

# Prompt2Video

## 仓库链接地址

https://github.com/Shmily0826/Prompt2Video.git

## 描述Description

本项目构建了一套完整的自动化视频生成流水线 (Automated Video Generation Pipeline)。

1. **AI 编排层**：利用 OpenAI SDK 调用 DeepSeek 大模型，将非结构化的用户 Prompt 转化为符合 Zod Schema 强校验的结构化分镜数据 (JSON)。
2. **程序化渲染层**：引入 Remotion 框架取代传统 GUI 剪辑软件，将视频帧映射为 React 组件，实现了基于数据的视频动态组装与服务端自动导出 (FFmpeg)

## 架构



视频渲染层：前端 (React + Remotion)

后端服务层： (Node.js + Express)

AI 大脑层 (DeepSeek V3 LLM)

底层导出引擎 (Remotion Renderer + FFmpeg)
