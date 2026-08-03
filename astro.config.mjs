import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// 独自ドメイン picknavi.net のルートで配信（base無し）。SEO・sitemap・OGP・canonical で使用
export default defineConfig({
  site: 'https://picknavi.net',
  integrations: [sitemap({ changefreq: 'weekly', priority: 0.7 })],
  vite: {
    plugins: [tailwindcss()],
  },
});
