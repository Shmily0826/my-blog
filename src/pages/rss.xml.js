import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';

export async function GET(context) {
	const posts = await getCollection('blog', ({ data }) => data.draft === false);
	const newestFirstPosts = posts.toSorted(
		(a, b) => {
			const dateDifference = b.data.pubDate.getTime() - a.data.pubDate.getTime();
			return dateDifference || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
		},
	);
	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: newestFirstPosts.map((post) => ({
			...post.data,
			link: `/blog/${post.id}/`,
		})),
	});
}
