/** Subdomains that are not tenant chat hosts (marketing, API gateway, etc.). */
const RESERVED_SUBDOMAINS = new Set([
  "www",
  "api",
  "app",
  "admin",
  "mail",
  "smtp",
  "ftp",
  "staging",
  "dev",
]);

/** Production default when VITE_TENANT_BASE_DOMAIN is not passed at Docker build. */
const DEFAULT_TENANT_BASE_DOMAIN = "myrobochat.com";

/**
 * Base domain for tenant subdomains, e.g. myrobochat.com → siyu.myrobochat.com
 * Set VITE_TENANT_BASE_DOMAIN at build time (ECS/Docker build arg or .env).
 */
export function tenantBaseDomain(): string | null {
  const raw = (import.meta.env.VITE_TENANT_BASE_DOMAIN as string | undefined)?.trim().toLowerCase();
  const configured = raw ? raw.replace(/^\.+/, "").replace(/\.+$/, "") : "";
  if (configured) return configured;
  if (typeof window === "undefined") return DEFAULT_TENANT_BASE_DOMAIN;
  const host = window.location.hostname.trim().toLowerCase().split(":")[0];
  if (host === DEFAULT_TENANT_BASE_DOMAIN || host.endsWith(`.${DEFAULT_TENANT_BASE_DOMAIN}`)) {
    return DEFAULT_TENANT_BASE_DOMAIN;
  }
  return null;
}

/** Slug from Host header when on {slug}.{baseDomain}; null if not a tenant host. */
export function slugFromHostname(hostname: string, baseDomain: string): string | null {
  const host = hostname.trim().toLowerCase().split(":")[0];
  const base = baseDomain.trim().toLowerCase();
  if (!host.endsWith(base)) return null;
  const prefix = host.slice(0, -(base.length + 1));
  if (!prefix || prefix.includes(".")) return null;
  if (RESERVED_SUBDOMAINS.has(prefix)) return null;
  return prefix;
}

export function resolveTenantSlug(pathSlug: string | undefined): string {
  const base = tenantBaseDomain();
  if (base && typeof window !== "undefined") {
    const fromHost = slugFromHostname(window.location.hostname, base);
    if (fromHost) return fromHost;
  }
  if (pathSlug?.trim()) return pathSlug.trim();
  return "demo";
}
