# Siyu Tech — Knowledge base

Source: [siyu.ie](https://siyu.ie/) (Siyu Tech / SIYU RETAIL LTD), Ireland.  
Prices on the website are in **EUR (€)**. Confirm final price and stock at checkout or with the shop.

## Business overview

Siyu Tech is an Irish retailer selling **refurbished and new mobile phones**, **smartwatches** (notably **Garett**), **robot vacuum cleaners**, **tablets**, **chargers**, **cables**, **audio**, and related accessories. The business also offers **phone repair** services. Online shop: **siyu.ie**.

## Location & contact

- **Address:** 1st Floor, 113 Rear of Longmile Business Center, Long Mile Road, Dublin 12, Ireland  
- **Phone:** +353 85 232 4484  
- **Email:** sales@siyu.ie  
- **Website:** https://siyu.ie/

## What we sell (categories)

- **Mobile phones:** Apple iPhone (including recent lines such as iPhone 17 / 17 Pro / 17 Pro Max), Samsung Galaxy (e.g. S25), other brands as listed online  
- **Smartwatches:** Garett range (e.g. Kids Twin 2 4G, Atom, Verona 2 Glow, Rose Gold) — often around **€119–€149** on the site  
- **Robot vacuum cleaners**  
- **Accessories:** cases, chargers, cables, screen protectors, earbuds, mounts, etc.  
- **Phone repairs:** yes — Siyu offers **phone repair** services (screens, faults, etc.). Quote and turnaround depend on the device; ask the customer to call **+353 85 232 4484** or email **sales@siyu.ie** for a specific repair price or booking.  

## Example featured prices (from website — verify live)

| Product | Indicative price |
|---------|------------------|
| iPhone 17 Pro Max 256GB | €1,479 |
| iPhone 17 Pro 256GB | ~€1,299–€1,339 |
| iPhone 17 256GB | ~€949–€979 |
| Samsung S25 | ~€1,499 |
| Garett smartwatches (various) | ~€119–€149 |

Website shows filters by **brand, colour, category, type, network**. Many iPhones list colours such as Deep Blue, Silver, Cosmic Orange, Sage, Lavender, Mist Blue.

## Ordering & delivery

- Customers can **order online** at siyu.ie (account registration available).  
- Trustpilot reviews mention **fast delivery** (including next-day in some cases) and strong service — do not guarantee delivery times unless confirmed with the shop.  
- For **returns, warranties, and payment methods**, direct customers to sales@siyu.ie or the website policies.
## Product stock and prices

Stock and prices are loaded from the separate inventory file (`inventory.csv` on S3).
For availability questions, the assistant uses live lookup results — do not guess stock or price.

## Product photos (thumbnails in chat)

- Optional column **`image_url`** on each `inventory.csv` row (HTTPS URL to a thumbnail on S3 or CloudFront).
- Suggested S3 path: `tenants/siyu/images/{sku}.jpg` (public read or CloudFront).
- When the customer asks for a photo/picture of a product, include the matching **image_url** on its own line in the reply; the chat UI renders it as a clickable thumbnail.
- Do not invent image URLs — only use `image_url` from inventory lookup results.

## Assistant rules

- Be helpful, professional, and concise.
- Do not invent products, prices, or stock not returned by inventory lookup.
- For **whether repairs are offered**, answer **yes** from this KB; for exact repair quotes or booking, give shop phone/email.
- For carrier contracts or legal advice, refer to the shop.
