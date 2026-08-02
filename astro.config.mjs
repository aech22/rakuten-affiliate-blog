import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// site は GitHub Pages 公開後に自分のドメイン/URLへ変更する（SEO・sitemap・OGPで使用）
export default defineConfig({
  site: 'https://example.com',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
