import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// content/articles/*.md を記事コレクションとして読む（生成物はこのディレクトリに出力される）
const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/articles' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional(),
    noindex: z.boolean().optional(),
  }),
});

export const collections = { articles };
