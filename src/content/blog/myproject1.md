---
title: 'Prompt2Video: From a Prompt to a Rendered Video'
description: 'A course project exploring how structured LLM output can drive a React and Remotion video-rendering pipeline.'
pubDate: 'May 14 2026'
updatedDate: '2026-09-14'
heroImage: '../../assets/posts/blog-placeholder-3.jpg'
draft: false
lang: 'en'

---

Prompt2Video was a course experiment in turning a natural-language request into a small programmatically rendered video. The useful part of the project was the boundary between free-form model output and a rendering system that needs predictable data.

## What I built

The application takes a prompt, asks a DeepSeek model for a structured scene description, validates that output against a Zod schema, and passes the resulting data into React components rendered with Remotion.

The pipeline has four main pieces:

1. **Prompt-to-structure:** the model converts free-form input into a constrained JSON scene description.
2. **Validation:** Zod checks the generated data before it reaches the renderer.
3. **Composition:** React and Remotion turn the validated scene data into video frames.
4. **Rendering:** the server-side renderer exports the composition as an MP4 using Remotion and FFmpeg.

## Why the structure matters

A language model can produce many plausible answers to the same prompt, while a renderer expects a stable shape. Treating the model output as untrusted structured input made the handoff easier to reason about and kept rendering logic separate from prompt generation.

## Stack

- React and TypeScript for the video composition
- Node.js and Express for the service layer
- DeepSeek for prompt-to-structure generation
- Zod for generated-data validation
- Remotion and FFmpeg for rendering and export

This was a course project and demo rather than a production video platform. The code is available on [GitHub](https://github.com/Shmily0826/Prompt2Video).
