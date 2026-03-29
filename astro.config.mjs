// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://shmily-blog.vercel.app/',
	integrations: [mdx(), sitemap()],
	
	markdown: {
	shikiConfig: {
		// 换一个主题，比如 'github-light' (白底) 或 'tokyo-night' (深蓝)
		theme: 'github-dark',
		// 或者干脆禁用默认背景，全靠你自己写的 CSS 控制
		// wrap: true,
	},
	},
});
