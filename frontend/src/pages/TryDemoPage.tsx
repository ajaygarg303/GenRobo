import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import type { SessionLead } from "@/api";

const DEMO_LEAD_KEY = "mrc_demo_lead";

export type DemoLead = {
  email: string;
  phone: string;
  name: string;
  sendTranscript: boolean;
};

export function saveDemoLead(lead: DemoLead) {
  sessionStorage.setItem(DEMO_LEAD_KEY, JSON.stringify(lead));
}

export function loadDemoLead(): DemoLead | null {
  try {
    const raw = sessionStorage.getItem(DEMO_LEAD_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as DemoLead;
  } catch {
    return null;
  }
}

export function clearDemoLead() {
  sessionStorage.removeItem(DEMO_LEAD_KEY);
}

export function demoLeadToSessionLead(lead: DemoLead): SessionLead {
  return {
    visitor_email: lead.email,
    visitor_phone: lead.phone,
    visitor_name: lead.name || undefined,
  };
}

export default function TryDemoPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [name, setName] = useState("");
  const [consent, setConsent] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    const em = email.trim();
    const ph = phone.trim();
    if (!em || !em.includes("@")) {
      setErr("Please enter a valid email address.");
      return;
    }
    if (!ph || ph.length < 7) {
      setErr("Please enter a valid mobile number.");
      return;
    }
    if (!consent) {
      setErr("Please agree to receive the demo transcript by email.");
      return;
    }
    saveDemoLead({ email: em, phone: ph, name: name.trim(), sendTranscript: consent });
    navigate("/try/chat");
  }

  return (
    <div className="mrc-site">
      <header className="mrc-nav">
        <div className="mrc-nav-inner">
          <Link to="/" className="mrc-logo">
            MyRoboChat
          </Link>
          <Link to="/" className="mrc-link-back">
            ← Back to home
          </Link>
        </div>
      </header>

      <main className="mrc-container mrc-try-main">
        <div className="mrc-try-card">
          <p className="mrc-eyebrow">Free demo</p>
          <h1>Try the sample assistant</h1>
          <p className="mrc-section-lead">
            Chat with our sample Irish café knowledge base. When you end the chat, we'll email you the
            transcript so you can see how it works for your customers.
          </p>

          <form className="mrc-try-form" onSubmit={onSubmit}>
            <label>
              Email <span className="mrc-req">*</span>
              <input
                className="mrc-input"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
              />
            </label>
            <label>
              Mobile <span className="mrc-req">*</span>
              <input
                className="mrc-input"
                type="tel"
                autoComplete="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+353 87 123 4567"
                required
              />
            </label>
            <label>
              Name <span className="mrc-optional">(optional)</span>
              <input
                className="mrc-input"
                type="text"
                autoComplete="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
              />
            </label>
            <label className="mrc-checkbox">
              <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
              <span>
                Send me a copy of this demo chat by email. We use your details only for this demo and
                follow-up about MyRoboChat.
              </span>
            </label>
            {err ? <p className="mrc-error">{err}</p> : null}
            <button type="submit" className="mrc-btn mrc-btn-block">
              Start demo chat
            </button>
          </form>

          <p className="mrc-try-hint">
            Sample questions: &ldquo;What are your hours?&rdquo; · &ldquo;Do you deliver?&rdquo; ·
            &ldquo;How much is chicken tikka?&rdquo;
          </p>
        </div>
      </main>
    </div>
  );
}
