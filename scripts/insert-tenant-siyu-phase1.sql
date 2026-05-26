-- Siyu Tech tenant — Phase 1 schema (plans, status, plan_id)
-- Use only after deploying code with entitlements / plans tables.

INSERT INTO plans (id, code, display_name, max_sessions_per_month, entitlements_json)
VALUES
  (gen_random_uuid(), 'basic', 'Basic', 200, '{"images":false,"appointments":false,"orders":false,"kb_suggestions":false}'),
  (gen_random_uuid(), 'advanced', 'Advanced', 2000, '{"images":true,"appointments":false,"orders":false,"kb_suggestions":true}'),
  (gen_random_uuid(), 'premium', 'Premium', 20000, '{"images":true,"appointments":true,"orders":true,"kb_suggestions":true}')
ON CONFLICT (code) DO NOTHING;

INSERT INTO tenants (
    id,
    slug,
    display_name,
    timezone,
    status,
    plan_id,
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
    'active',
    (SELECT id FROM plans WHERE code = 'premium' LIMIT 1),
    '#1e40af',
    '#fffbf0',
    '#1e3a5f',
    NULL,
    'Welcome to Siyu Tech — ask about phones, smartwatches, accessories, prices, or stock.',
    $faq$
Siyu Tech (siyu.ie) — Irish retailer: refurbished & new phones (Apple, Samsung, etc.), Garett smartwatches, robot vacuums, chargers, cases, earbuds, repairs.
Shop: 1st Floor, 113 Rear Longmile Business Center, Long Mile Road, Dublin 12.
Phone: +353 85 232 4484. Email: sales@siyu.ie.

For exact SKU stock quantity and price, the assistant must use inventory.csv (S3 key: tenants/siyu/inventory.csv) — match brand, product name, colour, storage; report stock_qty and price_eur. If stock_qty=0, say out of stock. If no match, ask for details or refer to the shop.

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
    status = EXCLUDED.status,
    plan_id = EXCLUDED.plan_id,
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

SELECT slug, display_name, status, plan_id, primary_color, background_color
FROM tenants WHERE slug = 'siyu';
