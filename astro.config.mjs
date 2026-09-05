import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// 独自ドメイン picknavi.net のルートで配信（base無し）。SEO・sitemap・OGP・canonical で使用

// sitemap の <lastmod> 用に、記事の frontmatter から日付だけを拾う（2026-09-06）。
// Astro の Content Collections は設定ファイルからは読めないので、ここでは frontmatter を直接読む。
// lastmod が無いと、更新した記事も新規記事と同じ扱いで再クロールが遅れる。
// .md と .mdx の両方を拾う（AFFILIATE.md のハマりどころ16番）。
const ARTICLES_DIR = new URL('./content/articles/', import.meta.url);
function articleLastmod() {
  const map = new Map();
  if (!fs.existsSync(ARTICLES_DIR)) return map;
  for (const file of fs.readdirSync(ARTICLES_DIR)) {
    if (!/\.mdx?$/.test(file)) continue;
    const raw = fs.readFileSync(new URL(file, ARTICLES_DIR), 'utf-8');
    const fm = raw.split('---')[1] ?? '';
    const pick = (key) => {
      const m = fm.match(new RegExp(`^${key}:\\s*['"]?(\\d{4}-\\d{2}-\\d{2})`, 'm'));
      return m ? m[1] : null;
    };
    const date = pick('updated') ?? pick('date');
    // Astro は slug を小文字化する（`キャンプ用LEDランタン…` → `キャンプ用ledランタン…`）ので、
    // キーも小文字に揃える。揃えないと大文字を含むファイル名の記事だけ lastmod が落ちる。
    const slug = file.replace(/\.mdx?$/, '').toLowerCase();
    if (date) map.set(`/articles/${slug}/`, new Date(`${date}T00:00:00+09:00`));
  }
  return map;
}
const LASTMOD = articleLastmod();

export default defineConfig({
  site: 'https://picknavi.net',
  integrations: [
    sitemap({
      // 404 はインデックス対象ではないので sitemap から外す。
      filter: (page) => !page.includes('/404'),
      changefreq: 'weekly',
      priority: 0.7,
      serialize(item) {
        // picknavi の記事 slug は大半が日本語なので、sitemap の URL はパーセントエンコードされている。
        // ファイル名から作った LASTMOD のキーと突き合わせるためにデコードして比較する。
        const path = decodeURIComponent(new URL(item.url).pathname).toLowerCase();
        if (path === '/') {
          return { ...item, changefreq: 'daily', priority: 1.0 };
        }
        if (path.startsWith('/articles/')) {
          const lastmod = LASTMOD.get(path);
          return {
            ...item,
            changefreq: 'monthly',
            priority: 0.8,
            ...(lastmod ? { lastmod: lastmod.toISOString() } : {}),
          };
        }
        // カテゴリ一覧・性別一覧・ランキングは記事が増えるたびに中身が変わる。
        if (path.startsWith('/categories/') || path.startsWith('/ranking')
          || ['/men/', '/women/', '/unisex/'].includes(path)) {
          return { ...item, changefreq: 'weekly', priority: 0.6 };
        }
        // about / privacy などの固定ページ。
        return { ...item, changefreq: 'yearly', priority: 0.3 };
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
