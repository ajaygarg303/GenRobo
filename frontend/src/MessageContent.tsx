import { useMemo } from "react";

const IMAGE_URL_RE =
  /https?:\/\/[^\s<>"']+\.(?:jpg|jpeg|png|webp|gif)(?:\?[^\s<>"')]*)?/gi;
const MD_IMAGE_RE = /!\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/gi;

function isImageUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

function parseMessage(content: string): { text: string; images: { url: string; alt: string }[] } {
  const images: { url: string; alt: string }[] = [];
  const seen = new Set<string>();

  const addImage = (url: string, alt: string) => {
    if (!isImageUrl(url) || seen.has(url)) return;
    seen.add(url);
    images.push({ url, alt });
  };

  let text = content.replace(MD_IMAGE_RE, (_, alt: string, url: string) => {
    addImage(url, alt || "Product image");
    return "";
  });

  for (const m of text.matchAll(IMAGE_URL_RE)) {
    addImage(m[0], "Image");
  }

  text = text
    .replace(IMAGE_URL_RE, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  return { text, images };
}

export default function MessageContent({ content }: { content: string }) {
  const { text, images } = useMemo(() => parseMessage(content), [content]);

  return (
    <div className="bc-msg-body">
      {text ? <span>{text}</span> : null}
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
