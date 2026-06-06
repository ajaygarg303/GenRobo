import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import {
  createSession,
  endSession,
  fetchChatSettings,
  fetchTenant,
  sendMessage,
  type ChatSettings,
  type TenantConfig,
} from "@/api";
import MessageContent from "@/MessageContent";
import { resolveTenantSlug } from "@/tenantSlug";

type Msg = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const { slug: pathSlug } = useParams();
  const slug = resolveTenantSlug(pathSlug);
  const [cfg, setCfg] = useState<TenantConfig | null>(null);
  const [chatSettings, setChatSettings] = useState<ChatSettings | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [chatClosed, setChatClosed] = useState(false);
  const listRef = useRef<HTMLDivElement | null>(null);
  const reminderTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const endTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const vars = useMemo(() => {
    if (!cfg) return {};
    return {
      "--bc-primary": cfg.primary_color,
      "--bc-bg": cfg.background_color,
      "--bc-text": cfg.text_color,
    } as React.CSSProperties;
  }, [cfg]);

  const clearIdleTimers = useCallback(() => {
    if (reminderTimerRef.current) clearTimeout(reminderTimerRef.current);
    if (endTimerRef.current) clearTimeout(endTimerRef.current);
    reminderTimerRef.current = null;
    endTimerRef.current = null;
  }, []);

  const closeChatDueToIdle = useCallback(async () => {
    if (!sessionId || chatClosed) return;
    clearIdleTimers();
    setChatClosed(true);
    const sid = sessionId;
    setSessionId(null);
    try {
      await endSession(sid, "idle");
    } catch {
      /* session may already be ended */
    }
    setMessages((m) => [
      ...m,
      {
        role: "assistant",
        content: "This chat closed due to inactivity. Refresh the page to start again.",
      },
    ]);
  }, [sessionId, chatClosed, clearIdleTimers]);

  const scheduleIdleTimers = useCallback(() => {
    if (!chatSettings || !sessionId || chatClosed) return;
    clearIdleTimers();

    reminderTimerRef.current = setTimeout(() => {
      setMessages((m) => [...m, { role: "assistant", content: chatSettings.idle_reminder_message }]);
      endTimerRef.current = setTimeout(() => {
        void closeChatDueToIdle();
      }, chatSettings.idle_end_after_reminder_seconds * 1000);
    }, chatSettings.idle_reminder_seconds * 1000);
  }, [chatSettings, sessionId, chatClosed, clearIdleTimers, closeChatDueToIdle]);

  const onActivity = useCallback(() => {
    scheduleIdleTimers();
  }, [scheduleIdleTimers]);

  useEffect(() => {
    if (!slug) return;
    let cancelled = false;
    (async () => {
      try {
        const [t, settings] = await Promise.all([fetchTenant(slug), fetchChatSettings()]);
        if (cancelled) return;
        setCfg(t);
        setChatSettings(settings);
        const s = await createSession(slug);
        if (cancelled) return;
        setSessionId(s.id);
        if (s.opening_message?.trim()) {
          setMessages([{ role: "assistant", content: s.opening_message.trim() }]);
        }
      } catch (e) {
        if (e instanceof Error && e.message === "session_quota") {
          setErr("This business has reached its monthly chat limit. Please try again later.");
        } else if (e instanceof Error && e.message === "business_unavailable") {
          setErr("This business chat is not available right now.");
        } else {
          setErr("We could not load this business. Check the link or try again later.");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  useEffect(() => {
    scheduleIdleTimers();
    return () => clearIdleTimers();
  }, [scheduleIdleTimers, clearIdleTimers]);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function onSend(e: React.FormEvent) {
    e.preventDefault();
    if (!sessionId || !input.trim() || busy || chatClosed) return;
    const text = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    onActivity();
    setBusy(true);
    try {
      const res = await sendMessage(sessionId, text);
      setMessages((m) => [...m, { role: "assistant", content: res.assistant_message.content }]);
      onActivity();
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
        setChatClosed(true);
        clearIdleTimers();
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
    if (!sessionId || chatClosed) return;
    setBusy(true);
    clearIdleTimers();
    try {
      await endSession(sessionId, "user");
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content:
            "Thanks — this chat is closed. The business may follow up using the contact details shown above.",
        },
      ]);
      setSessionId(null);
      setChatClosed(true);
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

  if (!cfg || (!sessionId && !chatClosed)) {
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
              <MessageContent content={m.content} />
            </div>
          ))}
        </div>

        <form className="bc-form" onSubmit={onSend}>
          <input
            className="bc-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message…"
            disabled={busy || chatClosed}
            autoComplete="off"
          />
          <button className="bc-btn" type="submit" disabled={busy || chatClosed || !input.trim()}>
            Send
          </button>
          <button
            className="bc-btn bc-btn-secondary"
            type="button"
            disabled={busy || chatClosed}
            onClick={onEnd}
          >
            End chat
          </button>
        </form>
      </div>
    </div>
  );
}
