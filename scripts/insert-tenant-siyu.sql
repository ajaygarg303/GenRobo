-- Siyu Tech tenant — PRODUCTION schema (no plans / plan_id / status columns)
-- Run on the Postgres database your ECS app uses.
-- Chat URL: https://YOUR-ALB/b/siyu

INSERT INTO tenants (
    id,
    slug,
    display_name,
    timezone,
    primary_color,
    background_color,
    text_color,
    logo_url,
    welcome_message,
    faq_text,
    knowledge_s3_key,
    business_hours_text,
    contact_phone,
    contact_email_public,
    transcript_email
) VALUES (
    gen_random_uuid(),
    'siyu',
    'Siyu Tech',
    'Europe/Dublin',
    '#1e40af',
    '#fffbf0',
    '#1e3a5f',
    NULL,
    'Welcome to Siyu Tech — ask about phones, smartwatches, accessories, prices, or stock.',
    $faq$
Siyu Tech (siyu.ie) — Irish retailer: refurbished & new phones (Apple, Samsung, etc.), Garett smartwatches, robot vacuums, chargers, cases, earbuds, repairs.
Shop: 1st Floor, 113 Rear Longmile Business Center, Long Mile Road, Dublin 12.
Phone: +353 85 232 4484. Email: sales@siyu.ie.

For exact SKU stock and price, use the inventory table in tenants/siyu/knowledge.md on S3 (or run scripts/update-siyu-faq-from-kb.sql for full KB in faq_text). Match brand, product name, colour, storage; use stock_qty and price_eur. If stock_qty=0, say out of stock.

Featured web prices (verify live): iPhone 17 Pro Max 256GB ~€1479; iPhone 17 Pro 256GB ~€1299; iPhone 17 256GB ~€949; Samsung S25 ~€1499; Garett watches ~€119–€149.
$faq$,
    'tenants/siyu/knowledge.md',
    'Mon–Sat 10:00–18:00 (confirm with shop).',
    '+353852324484',
    'sales@siyu.ie',
    'sales@siyu.ie'
)
ON CONFLICT (slug) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    primary_color = EXCLUDED.primary_color,
    background_color = EXCLUDED.background_color,
    text_color = EXCLUDED.text_color,
    welcome_message = EXCLUDED.welcome_message,
    faq_text = EXCLUDED.faq_text,
    knowledge_s3_key = EXCLUDED.knowledge_s3_key,
    business_hours_text = EXCLUDED.business_hours_text,
    contact_phone = EXCLUDED.contact_phone,
    contact_email_public = EXCLUDED.contact_email_public,
    transcript_email = EXCLUDED.transcript_email;

SELECT slug, display_name, primary_color, background_color, knowledge_s3_key
FROM tenants WHERE slug = 'siyu';
