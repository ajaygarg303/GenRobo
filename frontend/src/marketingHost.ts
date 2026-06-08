import { slugFromHostname, tenantBaseDomain } from "@/tenantSlug";

/** True on apex marketing host (myrobochat.com / www), not on {tenant}.myrobochat.com */
export function isMarketingHost(): boolean {
  if (typeof window === "undefined") return true;
  const base = tenantBaseDomain();
  if (!base) return true;
  const host = window.location.hostname.trim().toLowerCase().split(":")[0];
  if (host === base || host === `www.${base}`) return true;
  return slugFromHostname(host, base) === null;
}
