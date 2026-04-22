import { useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import {
  createSession,
  endSession,
  fetchTenant,
  sendMessage,
  type TenantConfig,
} from "@/api";

type Msg = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const { slug = "demo" } = useParams();
  const [cfg, setCfg] = useState<TenantConfig | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const listRef = useRef<HTMLDivElement | null>(null);

  const vars = useMemo(() => {
    if (!cfg) return {};
    return {
      "--bc-primary": cfg.primary_color,
      "--bc-bg": cfg.background_color,
      "--bc-text": cfg.text_color,
    } as React.CSSProperties;
  }, [cfg]);

  useEffect(() => {
    if (!slug) return;
    let cancelled = false;
    (async () => {
      try {
        const t = await fetchTenant(slug);
        if (cancelled) return;
        setCfg(t);
        const s = await createSession(slug);
        if (cancelled) return;
        setSessionId(s.id);
      } catch {
        setErr("We could not load this business. Check the link or try again later.");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function onSend(e: React.FormEvent) {
    e.preventDefault();
    if (!sessionId || !input.trim() || busy) return;
    const text = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setBusy(true);
    try {
      const res = await sendMessage(sessionId, text);
      setMessages((m) => [...m, { role: "assistant", content: res.assistant_message.content }]);
    } catch (e) {
      if (e instanceof Error && e.message === "session_expired") {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: "This chat timed out. Please refresh the page to start again.",
          },
        ]);
        setSessionId(null);
      } else {
        setMessages((m) => [
          ...m,
          { role: "assistant", content: "Something went wrong. Please try again in a moment." },
        ]);
      }
    } finally {
      setBusy(false);
    }
  }

  async function onEnd() {
    if (!sessionId) return;
    setBusy(true);
    try {
      await endSession(sessionId, "user");
      setMessages((m) => [
        ...m,
        { role: "assistant", content: "Thanks — this chat is closed. The business may follow up using the contact details shown above." },
      ]);
      setSessionId(null);
    } finally {
      setBusy(false);
    }
  }

  if (err) {
    return (
      <div className="bc-shell" style={vars}>
        <div className="bc-card">
          <p className="bc-muted">{err}</p>
        </div>
      </div>
    );
  }

  if (!cfg || !sessionId) {
    return (
      <div className="bc-shell" style={vars}>
        <div className="bc-card">
          <p className="bc-muted">Loading…</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bc-shell" style={vars}>
      <div className="bc-card">
        <header className="bc-header">
          {cfg.logo_url ? (
            <img className="bc-logo" src={cfg.logo_url} alt="" />
          ) : (
            <div className="bc-logo-placeholder" aria-hidden />
          )}
          <div>
            <h1 className="bc-title">{cfg.display_name}</h1>
            <p className="bc-sub">{cfg.welcome_message}</p>
          </div>
        </header>

        <section className="bc-meta">
          <div>
            <span className="bc-label">Hours</span>
            <p>{cfg.business_hours_text || "—"}</p>
          </div>
          <div>
            <span className="bc-label">Contact</span>
            <p>
              {cfg.contact_phone && <span>{cfg.contact_phone}</span>}
              {cfg.contact_phone && cfg.contact_email_public && <span> · </span>}
              {cfg.contact_email_public && <span>{cfg.contact_email_public}</span>}
              {!cfg.contact_phone && !cfg.contact_email_public && "—"}
            </p>
          </div>
        </section>

        <div className="bc-messages" ref={listRef}>
          {messages.map((m, i) => (
            <div key={i} className={`bc-msg bc-msg-${m.role}`}>
              {m.content}
            </div>
          ))}
        </div>

        <form className="bc-form" onSubmit={onSend}>
          <input
            className="bc-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message…"
            disabled={busy}
            autoComplete="off"
          />
          <button className="bc-btn" type="submit" disabled={busy || !input.trim()}>
            Send
          </button>
          <button className="bc-btn bc-btn-secondary" type="button" disabled={busy} onClick={onEnd}>
            End chat
          </button>
        </form>
      </div>
    </div>
  );
}
