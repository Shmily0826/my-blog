# Zhenyu Luo — Personal Portfolio

This repository contains Zhenyu Luo's personal portfolio and technical blog. The site introduces the developer, presents selected software projects, and publishes notes from building and learning across web, Android, and AI-enabled applications.

## Stack

- [Astro](https://astro.build/) for the static site and page components
- Markdown and MDX content collections for the blog
- `@astrojs/rss` for the RSS feed
- `@astrojs/sitemap` for the generated sitemap
- `sharp` for Astro image processing

The main public areas are `/`, `/projects`, `/about`, and `/blog`. The blog also exposes `/rss.xml`; draft posts remain private by default until explicitly marked for publication.

## Local development

Install dependencies and start the local development server:

```sh
npm install
npm run dev
```

The development server runs on Astro's default local port. To build and preview the static site:

```sh
npm run build
npm run preview
```

Other Astro CLI commands can be run with:

```sh
npm run astro -- --help
```

The configured `site` URL in `astro.config.mjs` is used as the base for canonical metadata and generated sitemap URLs. No deployment provider configuration is stored in this repository.
