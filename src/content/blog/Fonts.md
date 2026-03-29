---
title: '修改CSS样式'
description: '了解如何更改代码区块'
pubDate: 'Mar 29 2026'
heroImage: '../../assets/posts/blog-placeholder-1.jpg'

---



常用代码字体：

**JetBrains Mono** 

**Fira Code**

**Cascadia Code**

**Monaspace** 

1. **行内代码** (`code`)

```javascript
code {
	padding: 2px 6px;                     /* 内边距 */
	background-color: rgba(var(--gray-light), 0.5); /* 浅灰色背景，50%透明度 */
	border-radius: 2px;                   /* 小圆角 */
	font-family: 'Cascadia Code', monospace;  /* 等宽字体，适合代码 */
	font-size: 1em;                       /* 与周围文字相同大小 */
}
```

之后再研究一下字体

2. **代码块** (`pre`)

```javascript
pre {
	padding: 2rem;                       /* 大内边距，让代码不贴边 */
	border-radius: 24px;                 /* 大圆角，现代感设计 */
	margin: 1rem 0;                      /* 上下外边距，与段落分隔 */
	background-color: #1e1e2e !important; /* 深色背景，!important确保优先级 */
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* 柔和阴影，增加层次感 */
	border: 1px solid rgba(0, 0, 0, 0.1); /* 细边框 */
	overflow-x: auto;                    /* 水平滚动条（当代码过长时） */
}
```

3.**代码块内部的代码** (`pre > code`)

```javascript
pre > code {
	padding: 0;                          /* 去掉行内代码的内边距 */
	background-color: transparent;        /* 透明背景，不叠加颜色 */
	border-radius: 0;                     /* 去掉圆角 */
	font-size: 1.3rem;                   /* 增大字体（代码块内通常更大） */
	line-height: 1.6;                    /* 行高，增强可读性 */
	color: inherit;                      /* 继承颜色（让语法高亮器控制） */
}
```

