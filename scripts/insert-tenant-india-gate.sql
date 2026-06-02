-- India Gate tenant — PRODUCTION schema (no plans / plan_id / status columns)
-- Run on the Postgres database your ECS app uses.
-- Chat URL: https://YOUR-ALB/b/india-gate

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
    business_type,
    intent_config_json,
    faq_text,
    knowledge_s3_key,
    business_hours_text,
    contact_phone,
    contact_email_public,
    transcript_email
) VALUES (
    gen_random_uuid(),
    'india-gate',
    'India Gate',
    'Europe/Dublin',
    '#b91c1c',
    '#fff7ed',
    '#111827',
    NULL,
    'Welcome to India Gate! Please share your name and phone or email, then ask about the menu, prices, delivery, or order totals.',
    'restaurant',
    '{}',
    $faq$
India Gate (indiagate.ie) — Indian restaurant & takeaway.
Address: Belgard Road, Tallaght, Dublin 24 (beside Windsor Motors).
Hours: Mon–Sun 4:00 pm – 10:30 pm.
Phone: 01 462 2704 / 01 462 2705. Email: ranbir.indiagate@gmail.com.

Menu pricing: Oct 2024 menu (EUR). Delivery local areas €3.50 per order.
For order totals use knowledge.md menu tables. Curries 17–31: chicken €12, lamb €13, veg €10, paneer €11, prawn €14.
Allergens: advise customers to contact the restaurant for full allergen information.
$faq$,
    'tenants/india-gate/knowledge.md',
    'Mon–Sun 16:00–22:30',
    '014622704',
    'ranbir.indiagate@gmail.com',
    'ranbir.indiagate@gmail.com'
)
ON CONFLICT (slug) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    primary_color = EXCLUDED.primary_color,
    background_color = EXCLUDED.background_color,
    text_color = EXCLUDED.text_color,
    welcome_message = EXCLUDED.welcome_message,
    business_type = EXCLUDED.business_type,
    intent_config_json = EXCLUDED.intent_config_json,
    faq_text = EXCLUDED.faq_text,
    knowledge_s3_key = EXCLUDED.knowledge_s3_key,
    business_hours_text = EXCLUDED.business_hours_text,
    contact_phone = EXCLUDED.contact_phone,
    contact_email_public = EXCLUDED.contact_email_public,
    transcript_email = EXCLUDED.transcript_email;

SELECT slug, display_name, primary_color, background_color, knowledge_s3_key
FROM tenants WHERE slug = 'india-gate';
