// サイトの分類体系（大元の性別軸 gender × ジャンル軸 category）。
// slug は scripts/config.py の CATEGORIES と一致させること（記事frontmatterの categorySlug と結合する）。

export type GenderSlug = 'men' | 'women' | 'unisex';

export interface Category {
  slug: string;
  label: string;
  gender: GenderSlug;
  emoji: string;
  blurb: string; // カテゴリページの説明・meta description に使う
}

export interface Gender {
  slug: GenderSlug;
  label: string;
  emoji: string;
  blurb: string;
}

export const GENDERS: Gender[] = [
  { slug: 'men',    label: 'メンズ系',       emoji: '🧔', blurb: '男性向けのファッション・アイテムをまとめてチェック。' },
  { slug: 'women',  label: 'レディース系',   emoji: '👩', blurb: '女性向けのファッション・アイテムをまとめてチェック。' },
  { slug: 'unisex', label: 'ユニセックス系', emoji: '🧑', blurb: '性別を問わず使える人気アイテムをまとめてチェック。' },
];

export const CATEGORIES: Category[] = [
  { slug: 'beauty',         label: '美容系',               gender: 'unisex', emoji: '💄', blurb: 'スキンケア・ヘアケアなど、毎日のキレイを支える人気アイテムを比較。' },
  { slug: 'daily',          label: '日常系',               gender: 'unisex', emoji: '☕', blurb: '家電・日用品など、毎日の暮らしを便利にするアイテムを比較。' },
  { slug: 'mens-fashion',   label: 'メンズファッション',   gender: 'men',    emoji: '👔', blurb: '男性向けの服・シューズ・定番アイテムをレビューと一緒に比較。' },
  { slug: 'ladies-fashion', label: 'レディースファッション', gender: 'women',  emoji: '👗', blurb: '女性向けの服・シューズ・バッグをレビューと一緒に比較。' },
  { slug: 'accessories',    label: '小物系',               gender: 'unisex', emoji: '⌚', blurb: '腕時計・財布・小物など、毎日の相棒になるアイテムを比較。' },
  { slug: 'outdoor',        label: 'アウトドア系',         gender: 'unisex', emoji: '⛺', blurb: 'キャンプ・アウトドアを楽しむための道具を比較。' },
  // Tier 1（高価値・低リスク）
  { slug: 'gourmet',        label: 'スイーツ・グルメ',     gender: 'unisex', emoji: '🍰', blurb: 'お取り寄せスイーツやご当地グルメなど、人気の食品・ギフトを比較。' },
  { slug: 'makeup',         label: 'メイクコスメ',         gender: 'women',  emoji: '💋', blurb: 'ファンデ・リップなど、口コミで人気のメイクアイテムを比較。' },
  { slug: 'fitness',        label: 'フィットネス',         gender: 'unisex', emoji: '🏋️', blurb: 'プロテイン・筋トレ器具・ヨガなど、自宅トレを支えるアイテムを比較。' },
  { slug: 'disaster',       label: '防災グッズ',           gender: 'unisex', emoji: '🧯', blurb: '防災セット・非常食など、いざという時の備えを比較。' },
  // Tier 2（様子見）
  { slug: 'pet',            label: 'ペット用品',           gender: 'unisex', emoji: '🐾', blurb: '犬・猫など、毎日使うペット用品を比較。' },
  { slug: 'interior',       label: 'インテリア・収納',     gender: 'unisex', emoji: '🛋️', blurb: '収納・家具など、暮らしを整えるアイテムを比較。' },
  { slug: 'kitchen',        label: 'キッチン用品',         gender: 'unisex', emoji: '🍳', blurb: '調理器具・キッチングッズを比較。' },
  { slug: 'seasonal',       label: '季節家電',             gender: 'unisex', emoji: '🌡️', blurb: '加湿器・扇風機など、季節の家電を比較。' },
];

export const categoryBySlug = (slug?: string | null): Category | undefined =>
  CATEGORIES.find((c) => c.slug === slug);

export const genderBySlug = (slug?: string | null): Gender | undefined =>
  GENDERS.find((g) => g.slug === slug);

export const categoriesOfGender = (gender: GenderSlug): Category[] =>
  CATEGORIES.filter((c) => c.gender === gender);
