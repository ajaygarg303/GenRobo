const base = (import.meta.env.VITE_API_BASE as string | undefined) ?? "";

export function apiUrl(path: string): string {
  if (path.startsWith("/")) return `${base}${path}`;
  return `${base}/${path}`;
}

export type TenantConfig = {
  slug: string;
  display_name: string;
  timezone: string;
  primary_color: string;
  background_color: string;
  text_color: string;
  logo_url: string | null;
  welcome_message: string;
  business_hours_text: string;
  contact_phone: string | null;
  contact_email_public: string | null;
};

export type ChatSettings = {
  idle_reminder_seconds: number;
  idle_end_after_reminder_seconds: number;
  idle_reminder_message: string;
};

export async function fetchChatSettings(): Promise<ChatSettings> {
  const r = await fetch(apiUrl("/api/public/chat-settings"));
  if (!r.ok) {
    return {
      idle_reminder_seconds: 30,
      idle_end_after_reminder_seconds: 30,
      idle_reminder_message: "Are you still there? Send a message to keep this chat open.",
    };
  }
  return r.json() as Promise<ChatSettings>;
}

export async function fetchTenant(slug: string): Promise<TenantConfig> {
  const r = await fetch(apiUrl(`/api/tenants/by-slug/${encodeURIComponent(slug)}`));
  if (r.status === 403) throw new Error("business_unavailable");
  if (!r.ok) throw new Error("Business not found");
  return r.json() as Promise<TenantConfig>;
}

export async function createSession(
  tenantSlug: string,
): Promise<{ id: string; tenant_slug: string; opening_message: string | null }> {
  const r = await fetch(apiUrl("/api/sessions"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tenant_slug: tenantSlug }),
  });
  if (r.status === 429) throw new Error("session_quota");
  if (!r.ok) throw new Error("Could not start chat");
  return r.json() as Promise<{ id: string; tenant_slug: string; opening_message: string | null }>;
}

export async function sendMessage(
  sessionId: string,
  content: string,
): Promise<{ assistant_message: { role: string; content: string } }> {
  const r = await fetch(apiUrl(`/api/sessions/${sessionId}/message`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (r.status === 410) throw new Error("session_expired");
  if (!r.ok) throw new Error("Send failed");
  return r.json() as Promise<{ assistant_message: { role: string; content: string } }>;
}

export async function endSession(
  sessionId: string,
  reason: "user" | "timeout" | "idle" = "user",
): Promise<void> {
  await fetch(apiUrl(`/api/sessions/${sessionId}/end`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reason }),
  });
}
