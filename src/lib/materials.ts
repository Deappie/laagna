import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';
import { z } from 'astro/zod';
// Imported through Vite (not fs) so `npm run dev` reloads when the file is edited.
import contentYaml from '../content/materials.yaml?raw';

const FILES_DIR = path.join(process.cwd(), 'public/files');

const fileName = z
  .string()
  .min(1)
  .refine((f) => !f.includes('..') && !f.startsWith('/') && !f.includes('://'), {
    message: 'faili nimi peab olema kaustas public/files (nt "konspekt.pdf"), mitte link',
  });

const url = z.string().url({ message: 'peab olema täielik link, nt https://...' });

const itemSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('link'), url, label: z.string().optional() }),
  z.object({ type: z.literal('video'), url, label: z.string().optional() }),
  z.object({ type: z.literal('form'), url, label: z.string().optional() }),
  z.object({ type: z.literal('pdf'), file: fileName, label: z.string().optional() }),
  z.object({ type: z.literal('file'), file: fileName, label: z.string().optional() }),
]);

const schema = z.object({
  site: z.object({
    title: z.string(),
    teacher: z.string().nullish(),
  }),
  courses: z
    .array(
      z.object({
        id: z.coerce.string().regex(/^[a-z0-9-]+$/, {
          message: 'id võib sisaldada ainult väiketähti, numbreid ja sidekriipsu',
        }),
        title: z.string(),
        description: z.string().nullish(),
      }),
    )
    .min(1),
  posts: z
    .array(
      z.object({
        title: z.string(),
        course: z.coerce.string(),
        date: z.coerce.date(),
        text: z.string().nullish(),
        items: z.array(itemSchema).default([]),
      }),
    )
    .nullish()
    .transform((p) => p ?? []),
});

export type Item = z.infer<typeof itemSchema>;
export type Data = z.infer<typeof schema>;
export type Course = Data['courses'][number];
export type Post = Data['posts'][number];

function fail(message: string): never {
  throw new Error(`\n\nViga failis src/content/materials.yaml:\n  ${message}\n`);
}

function load(): Data {
  let raw: unknown;
  try {
    raw = parse(contentYaml);
  } catch (e) {
    fail(`YAML-i ei õnnestunud lugeda (kontrolli taandeid ja jutumärke).\n  ${(e as Error).message}`);
  }

  const result = schema.safeParse(raw);
  if (!result.success) {
    fail(
      result.error.issues
        .map((i) => `${i.path.join(' → ') || '(juur)'}: ${i.message}`)
        .join('\n  '),
    );
  }
  const data = result.data;

  const ids = new Set<string>();
  for (const c of data.courses) {
    if (ids.has(c.id)) fail(`kursuse id "${c.id}" on kaks korda`);
    ids.add(c.id);
  }
  data.posts.forEach((post, i) => {
    if (!ids.has(post.course)) {
      fail(`posts → ${i} ("${post.title}"): kursust "${post.course}" ei ole. Olemas: ${[...ids].join(', ')}`);
    }
    for (const item of post.items) {
      if ('file' in item && !fs.existsSync(path.join(FILES_DIR, item.file))) {
        fail(`posts → ${i} ("${post.title}"): faili "${item.file}" ei ole kaustas public/files`);
      }
    }
  });

  return data;
}

const data = load();
const byNewest = (a: Post, b: Post) => b.date.getTime() - a.date.getTime();

export const site = data.site;

export function getCourses(): Course[] {
  return data.courses;
}

export function getCourse(id: string): Course | undefined {
  return data.courses.find((c) => c.id === id);
}

export function getPostsForCourse(id: string): Post[] {
  return data.posts.filter((p) => p.course === id).sort(byNewest);
}

export function getLatestPosts(n: number): Post[] {
  return [...data.posts].sort(byNewest).slice(0, n);
}

export function fileSize(file: string): string {
  const bytes = fs.statSync(path.join(FILES_DIR, file)).size;
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1).replace('.', ',')} MB`;
}

export function youtubeId(link: string): string | null {
  try {
    const u = new URL(link);
    const host = u.hostname.replace(/^(www\.|m\.)/, '');
    if (host === 'youtu.be') return u.pathname.slice(1) || null;
    if (host === 'youtube.com' || host === 'youtube-nocookie.com') {
      if (u.searchParams.get('v')) return u.searchParams.get('v');
      const m = u.pathname.match(/^\/(shorts|embed|live)\/([\w-]+)/);
      return m ? m[2] : null;
    }
  } catch {}
  return null;
}
