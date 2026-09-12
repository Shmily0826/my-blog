import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rssPath = path.join(projectRoot, 'dist', 'rss.xml');
const blogDirectory = path.join(projectRoot, 'dist', 'blog');

assert(fs.existsSync(rssPath), 'dist/rss.xml does not exist');
const rss = fs.readFileSync(rssPath, 'utf8');

function readTag(item, tagName) {
	const match = item.match(new RegExp(`<${tagName}>([\\s\\S]*?)</${tagName}>`));
	assert(match, `RSS item is missing <${tagName}>`);
	return match[1].trim().replaceAll('&amp;', '&');
}
const items = [...rss.matchAll(/<item>([\s\S]*?)<\/item>/g)].map((match) => match[1]);

assert(fs.existsSync(blogDirectory), 'dist/blog does not exist');
assert(fs.existsSync(path.join(blogDirectory, 'index.html')), 'Blog index was not generated');

function collectBlogRoutes(directory, segments = []) {
	const routes = new Set();
	for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
		if (!entry.isDirectory()) continue;

		const entryPath = path.join(directory, entry.name);
		const nextSegments = [...segments, entry.name];
		if (fs.existsSync(path.join(entryPath, 'index.html'))) {
			routes.add(`/blog/${nextSegments.join('/')}/`);
		}
		for (const route of collectBlogRoutes(entryPath, nextSegments)) routes.add(route);
	}
	return routes;
}

const expectedPublicPaths = collectBlogRoutes(blogDirectory);
assert(expectedPublicPaths.size > 0, 'No public Blog post pages were generated');

const links = items.map((item) => readTag(item, 'link'));
const actualPublicPaths = new Set(links.map((link) => new URL(link).pathname));
assert.equal(items.length, expectedPublicPaths.size, 'published RSS item count differs from Blog output');
assert.equal(new Set(links).size, links.length, 'RSS contains duplicate item identities');
assert.deepEqual(actualPublicPaths, expectedPublicPaths, 'published RSS item set differs from Blog output');
assert(!rss.includes('debugging-youtube-caption-http-200'), 'private draft is present in RSS');

const dates = items.map((item) => Date.parse(readTag(item, 'pubDate')));
assert(dates.every(Number.isFinite), 'RSS contains an invalid publication date');
for (let index = 1; index < dates.length; index += 1) {
	assert(
		dates[index - 1] >= dates[index],
		'RSS publication dates are not monotonically non-increasing',
	);
}

console.log(`RSS regression check passed: ${items.length} published items, newest-first, draft excluded.`);
