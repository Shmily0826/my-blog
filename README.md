# Shmily0826 — Projects & Engineering Notes

This repository contains Shmily0826's project showcase and technical blog. The site presents software projects, implementation decisions, and notes from building and learning across web, Android, and AI-enabled applications. Public identity uses the GitHub handle; personal background, CV, and contact details are omitted.

## Stack

- [Astro](https://astro.build/) for the static site and page components
- Markdown and MDX content collections for the blog
- `@astrojs/rss` for the RSS feed
- `@astrojs/sitemap` for the generated sitemap
- `sharp` for Astro image processing

The main public areas are `/`, `/projects`, `/about`, and `/blog`. The `/about` page explains the site and its engineering approach. The blog also exposes `/rss.xml`; draft posts are excluded from generated pages and RSS until explicitly marked for publication. This filtering does not make source files private in a public repository.

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

## Project content maintenance

Project copy, status, technologies, and links live in `src/data/projects.ts`. Appause is the homepage spotlight, with Sky Scout and Ripple Cart Rescue also shown visually. `/projects` is the browseable index; `/projects/[id]/` holds the experience, contribution, decisions, and current limits for each project. Existing `/projects#id` links still land on the corresponding index entry. Prompt2Video and EchoLearn sit under earlier experiments; EchoLearn is labelled as not actively maintained. Add future AI-video work when a finished example is available.

Keep team contributions distinct from solo work, identify AI-assisted development, and separate screenshots or diagrams from evidence of live behavior. Image provenance and content evidence are recorded in `src/assets/projects/SOURCES.md`. Only add source or demo links that visitors can access.

Before release, run `npm run build` and `npm run check:rss`, then inspect the homepage and project sections at desktop and mobile sizes. Review pending content explicitly before publishing; draft posts remain excluded.
