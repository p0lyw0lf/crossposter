import { rehypeShiki } from "@astrojs/markdown-remark";
import rehypeRaw from "rehype-raw";
import rehypeStringify from "rehype-stringify";
import remarkGfm from "remark-gfm";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import { unified } from "unified";

const renderer = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeShiki, {
    langs: [],
    theme: "github-dark",
    themes: {},
    wrap: false,
    transformers: [],
    langAlias: {},
  })
  .use(rehypeRaw)
  .use(rehypeStringify);

export const render = async (markdown: string): Promise<string> => {
  return String(await renderer.process(markdown));
};
