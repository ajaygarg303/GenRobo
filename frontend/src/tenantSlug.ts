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

/**
 * Base domain for tenant subdomains, e.g. myrobochat.com → siyu.myrobochat.com
 * Set VITE_TENANT_BASE_DOMAIN at build time (ECS/Docker build arg or .env).
 */
export function tenantBaseDomain(): string | null {
  const raw = (import.meta.env.VITE_TENANT_BASE_DOMAIN as string | undefined)?.trim().toLowerCase();
  if (!raw) return null;
  return raw.replace(/^\.+/, "").replace(/\.+$/, "");
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
  if (pathSlug?.trim()) return pathSlug.trim();
  const base = tenantBaseDomain();
  if (base && typeof window !== "undefined") {
    const fromHost = slugFromHostname(window.location.hostname, base);
    if (fromHost) return fromHost;
  }
  return "demo";
}
