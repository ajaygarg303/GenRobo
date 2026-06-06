import { useMemo } from "react";

const MD_IMAGE_RE = /!\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/gi;
const IMAGE_EXT_RE =
  /https?:\/\/[^\s<>"']+\.(?:jpg|jpeg|png|webp|gif)(?:\?[^\s<>"')]*)?/gi;
const S3_IMAGE_RE =
  /https?:\/\/[^\s<>"']+\.amazonaws\.com\/[^\s<>"')]+/gi;
const HTTPS_RE = /https?:\/\/[^\s<>"']+/gi;

function isSafeUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

function isLikelyImageUrl(url: string): boolean {
  if (!isSafeUrl(url)) return false;
  const low = url.toLowerCase().split("?")[0];
  if (/\.(jpg|jpeg|png|webp|gif)$/.test(low)) return true;
  if (low.includes(".amazonaws.com/") && (low.includes("/images/") || low.includes("/image/"))) {
    return true;
  }
  return false;
}

function normalizeContent(raw: string): string {
  return raw
    .replace(/[`']/g, "")
    .replace(/\r\n/g, "\n");
}

function collectImages(content: string): { text: string; images: { url: string; alt: string }[] } {
  const images: { url: string; alt: string }[] = [];
  const seen = new Set<string>();

  const add = (url: string, alt: string) => {
    const u = url.replace(/[.,;:!?)]+$/, "");
    if (!isLikelyImageUrl(u) || seen.has(u)) return;
    seen.add(u);
    images.push({ url: u, alt });
  };

  let text = content.replace(MD_IMAGE_RE, (_, alt: string, url: string) => {
    add(url, alt || "Product image");
    return "";
  });

  for (const re of [IMAGE_EXT_RE, S3_IMAGE_RE]) {
    for (const m of text.matchAll(re)) {
      add(m[0], "Product image");
    }
  }

  for (const img of images) {
    text = text.split(img.url).join("");
  }
  text = text.replace(/\n{3,}/g, "\n\n").trim();

  return { text, images };
}

function renderTextWithLinks(text: string) {
  const nodes: (string | JSX.Element)[] = [];
  let last = 0;
  let linkIdx = 0;
  for (const m of text.matchAll(HTTPS_RE)) {
    const idx = m.index ?? 0;
    if (idx > last) nodes.push(text.slice(last, idx));
    const url = m[0].replace(/[.,;:!?)]+$/, "");
    if (isSafeUrl(url)) {
      nodes.push(
        <a key={`${url}-${linkIdx++}`} href={url} target="_blank" rel="noopener noreferrer">
          {url}
        </a>,
      );
    } else {
      nodes.push(url);
    }
    last = idx + m[0].length;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes.length ? nodes : text;
}

export default function MessageContent({ content }: { content: string }) {
  const normalized = useMemo(() => normalizeContent(content), [content]);
  const { text, images } = useMemo(() => collectImages(normalized), [normalized]);

  return (
    <div className="bc-msg-body">
      {text ? <span>{renderTextWithLinks(text)}</span> : null}
      {images.length > 0 ? (
        <div className="bc-msg-images">
          {images.map((img) => (
            <a
              key={img.url}
              className="bc-thumb-link"
              href={img.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="bc-thumb"
                src={img.url}
                alt={img.alt}
                loading="lazy"
                decoding="async"
              />
            </a>
          ))}
        </div>
      ) : null}
    </div>
  );
}
