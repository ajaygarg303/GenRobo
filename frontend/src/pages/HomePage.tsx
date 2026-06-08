import { Link } from "react-router-dom";

const CONTACT_EMAIL = "hello@myrobochat.com";

const BENEFITS = [
  {
    title: "Works 24/7 — especially after hours",
    body: "Capture questions when you're on a job, in the kitchen, or closed for the day.",
  },
  {
    title: "Your link, your look",
    body: "A dedicated chat link plus your logo, colour theme, and welcome message — on-brand for your business.",
  },
  {
    title: "Trained on your business",
    body: "Answers come from your FAQs, menu, services, or product list — not guesswork.",
  },
  {
    title: "Transcript by email",
    body: "When a chat ends, you get a summary and full transcript — so you can follow up on leads.",
  },
  {
    title: "Fast to go live",
    body: "Many businesses are live the same day once your content is ready. We help with setup and tweaks.",
  },
  {
    title: "Built for small budgets",
    body: "Simple monthly plans. For many shops and trades, one extra lead a month can cover the cost.",
  },
];

const USE_CASES = [
  {
    title: "Retail & electronics",
    body: "Stock, prices, and product questions — with optional product photos.",
  },
  {
    title: "Takeaway & cloud kitchen",
    body: "Menu, delivery, fees, hours, and allergens — fewer repeat calls at rush hour.",
  },
  {
    title: "Trades",
    body: "Services, areas, rates, and hours — capture name and number while you're on site.",
  },
  {
    title: "Local services",
    body: "Hours, location, and what you offer — hand complex cases to phone or email.",
  },
];

const PLANS = [
  {
    name: "Starter",
    price: "from €29",
    period: "/ month (ex VAT)",
    for: "Solo trades, light traffic",
    sessions: "~200 chats / month",
    features: ["FAQ & hours", "Lead capture", "Email transcript", "Your branding"],
    highlighted: false,
  },
  {
    name: "Growth",
    price: "from €59",
    period: "/ month (ex VAT)",
    for: "Shops, busy takeaways",
    sessions: "~2,000 chats / month",
    features: ["Everything in Starter", "Menu or inventory lookup", "Product images", "Priority setup help"],
    highlighted: true,
  },
];

const FAQ = [
  {
    q: "Will it make up prices or stock?",
    a: "It's instructed to use your knowledge and say when it doesn't know. You control what goes in the knowledge base.",
  },
  {
    q: "How fast can we go live?",
    a: "Often the same day once we have your FAQs, menu, or product list. We'll work with you on wording and branding.",
  },
  {
    q: "Do I need a full website?",
    a: "No. Many customers use their chat link on Google, WhatsApp, or social. Already have a site? Link or embed the same assistant.",
  },
  {
    q: "Do I need technical skills?",
    a: "No — we help with setup, colours, welcome message, and knowledge base.",
  },
];

export default function HomePage() {
  return (
    <div className="mrc-site">
      <header className="mrc-nav">
        <div className="mrc-nav-inner">
          <Link to="/" className="mrc-logo">
            MyRoboChat
          </Link>
          <nav className="mrc-nav-links">
            <a href="#benefits">Benefits</a>
            <a href="#use-cases">Use cases</a>
            <a href="#plans">Plans</a>
            <a href="#demo">Try demo</a>
          </nav>
          <Link to="/try" className="mrc-btn mrc-btn-sm">
            Try free demo
          </Link>
        </div>
      </header>

      <section className="mrc-hero">
        <div className="mrc-container mrc-hero-grid">
          <div>
            <p className="mrc-eyebrow">AI chat for Irish small business</p>
            <h1>Answer customers 24/7 — with your brand, your knowledge</h1>
            <p className="mrc-lead">
              MyRoboChat turns your FAQs, menu, prices, and services into a branded chat assistant.
              Share a link on your website, Google listing, or social — no big IT project.
            </p>
            <div className="mrc-hero-cta">
              <Link to="/try" className="mrc-btn">
                Try free demo
              </Link>
              <a href="#plans" className="mrc-btn mrc-btn-outline">
                See plans
              </a>
            </div>
            <p className="mrc-trust">
              Your logo, colours, and welcome message · Answers from <strong>your</strong> knowledge ·
              Transcript emailed when a chat ends
            </p>
          </div>
          <div className="mrc-hero-card">
            <div className="mrc-mock-chat">
              <div className="mrc-mock-header">
                <span className="mrc-mock-logo" />
                <div>
                  <strong>Your Business</strong>
                  <span>yourbusiness.myrobochat.com</span>
                </div>
              </div>
              <div className="mrc-mock-msgs">
                <div className="mrc-mock-msg mrc-mock-bot">
                  Hi! Ask about our hours, menu, or services.
                </div>
                <div className="mrc-mock-msg mrc-mock-user">Are you open Sunday evening?</div>
                <div className="mrc-mock-msg mrc-mock-bot">
                  We're closed Sundays. Mon–Sat 9am–9pm. Can I help with anything else?
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="benefits" className="mrc-section">
        <div className="mrc-container">
          <h2>Why small businesses choose MyRoboChat</h2>
          <p className="mrc-section-lead">Powerful enough to help customers — simple enough for a busy owner.</p>
          <div className="mrc-grid mrc-grid-3">
            {BENEFITS.map((b) => (
              <article key={b.title} className="mrc-card">
                <h3>{b.title}</h3>
                <p>{b.body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mrc-section mrc-section-alt">
        <div className="mrc-container mrc-split">
          <div>
            <h2>Your brand, not ours</h2>
            <p className="mrc-section-lead">
              Every business gets a dedicated chat link <em>and</em> their own look and feel.
            </p>
            <ul className="mrc-checklist">
              <li>Your chat link — e.g. <code>yourbusiness.myrobochat.com</code></li>
              <li>Your logo and colour theme</li>
              <li>Your welcome message and business name</li>
              <li>Your hours and contact details in the chat</li>
            </ul>
          </div>
          <div className="mrc-card mrc-card-accent">
            <h3>No full website? No problem.</h3>
            <p>
              Use MyRoboChat as your smart contact link on Google Business, Instagram, WhatsApp, or a
              simple link page. Already have a website? Add the same branded assistant without a redesign.
            </p>
          </div>
        </div>
      </section>

      <section id="use-cases" className="mrc-section">
        <div className="mrc-container">
          <h2>Use cases</h2>
          <p className="mrc-section-lead">
            Retail, takeaway, or trades — same platform, each business with its own branded chat.
          </p>
          <div className="mrc-grid mrc-grid-2">
            {USE_CASES.map((u) => (
              <article key={u.title} className="mrc-card">
                <h3>{u.title}</h3>
                <p>{u.body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mrc-section mrc-section-alt">
        <div className="mrc-container">
          <h2>How it works</h2>
          <ol className="mrc-steps">
            <li>
              <strong>Share your info</strong> — FAQs, menu, product list, or a short call with us.
            </li>
            <li>
              <strong>We configure your assistant</strong> — branding (logo, colours, welcome text),
              knowledge base, and chat link.
            </li>
            <li>
              <strong>Go live</strong> — share your link on web, Google, WhatsApp, or social.
            </li>
          </ol>
          <p className="mrc-muted-center">
            Open to customize: wording, colours, and what the bot should (and shouldn't) answer.
          </p>
        </div>
      </section>

      <section id="plans" className="mrc-section">
        <div className="mrc-container">
          <h2>Simple plans</h2>
          <p className="mrc-section-lead">VAT (23%) applies. No long contract for early customers.</p>
          <div className="mrc-grid mrc-grid-2 mrc-plans">
            {PLANS.map((p) => (
              <article
                key={p.name}
                className={`mrc-card mrc-plan${p.highlighted ? " mrc-plan-featured" : ""}`}
              >
                {p.highlighted ? <span className="mrc-badge">Popular</span> : null}
                <h3>{p.name}</h3>
                <p className="mrc-plan-for">{p.for}</p>
                <p className="mrc-plan-price">
                  {p.price}
                  <span>{p.period}</span>
                </p>
                <p className="mrc-plan-sessions">{p.sessions}</p>
                <ul>
                  {p.features.map((f) => (
                    <li key={f}>{f}</li>
                  ))}
                </ul>
                <a href={`mailto:${CONTACT_EMAIL}?subject=MyRoboChat%20${p.name}%20plan`} className="mrc-btn mrc-btn-block">
                  Contact us
                </a>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="demo" className="mrc-section mrc-section-cta">
        <div className="mrc-container mrc-cta-box">
          <h2>Try it yourself</h2>
          <p>
            Enter your email and mobile, chat with our sample business knowledge base, and receive the
            transcript by email when you finish — see exactly what your customers would get.
          </p>
          <Link to="/try" className="mrc-btn mrc-btn-lg">
            Start free demo
          </Link>
        </div>
      </section>

      <section className="mrc-section mrc-section-alt">
        <div className="mrc-container mrc-faq">
          <h2>Common questions</h2>
          {FAQ.map((item) => (
            <details key={item.q} className="mrc-faq-item">
              <summary>{item.q}</summary>
              <p>{item.a}</p>
            </details>
          ))}
        </div>
      </section>

      <footer className="mrc-footer">
        <div className="mrc-container mrc-footer-inner">
          <div>
            <strong>MyRoboChat</strong>
            <p>AI chat for Irish small business</p>
          </div>
          <div className="mrc-footer-links">
            <Link to="/try">Try demo</Link>
            <a href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
