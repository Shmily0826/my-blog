import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  // 使用 schema 来定义数据的结构
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    // 这行是关键：使用 image() 而不是 z.string()
    // 它会告诉 Astro 把 Markdown 里的路径字符串自动转换成导入对象
    heroImage: image(), 
    pubDate: z.coerce.date(),
  }),
});

export const collections = { blog };