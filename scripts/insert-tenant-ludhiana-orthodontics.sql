-- Ludhiana Orthodontic & Dental Clinic — PRODUCTION schema
-- KB source: https://ludhianaorthodontics.in/ (Home, About Us, Services, Contact)
-- Run on Postgres used by ECS, then upload knowledge.md to S3.
-- Chat URL: https://ludhiana-orthodontics.myrobochat.com

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
    dynamic_data_s3_key,
    dynamic_data_kind,
    business_hours_text,
    contact_phone,
    contact_email_public,
    transcript_email
) VALUES (
    gen_random_uuid(),
    'ludhiana-orthodontics',
    'Ludhiana Orthodontic & Dental Clinic',
    'Asia/Kolkata',
    '#0d9488',
    '#f0fdfa',
    '#134e4a',
    NULL,
    'Welcome to Ludhiana Orthodontic & Dental Clinic! Please share your name and phone number, then ask about braces, clear aligners, appointments, hours, or location.',
    'services',
    '{"keywords":{"hours_location":["clinic","appointment","visit","book"],"general":["braces","invisalign","aligner","orthodont","retainer","root canal","whitening","implant","crown","laminate","smile","teeth","dental","co smart","clear ortho"]}}',
    $faq$
Ludhiana Orthodontic & Dental Clinic — Dr. Shammi Garg, Orthodontist.
Address: Near Marryland Palace, Model Town Extension, D Block, Dugri Road, Ludhiana 141003.
Phone: +91-98724-21252 · +91-98725-41930. Email: drshammigarg@gmail.com · info@ludhianaorthodontics.in
Braces: metal, ceramic, lingual, i-Braces; Invisalign and CLEAR ORTHO aligners; microimplants; indirect bonding.
Also: RCT (incl. single sitting), implants, metal-free crowns, whitening, smile design, children's dentistry, oral surgery.
Call or use website contact form to book. Hours and fees — phone for current details.
$faq$,
    'tenants/ludhiana-orthodontics/knowledge.md',
    NULL,
    'none',
    'Call +91-98724-21252 for clinic hours (not published on main website pages).',
    '+919872421252',
    'info@ludhianaorthodontics.in',
    'drshammigarg@gmail.com'
)
ON CONFLICT (slug) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    timezone = EXCLUDED.timezone,
    primary_color = EXCLUDED.primary_color,
    background_color = EXCLUDED.background_color,
    text_color = EXCLUDED.text_color,
    welcome_message = EXCLUDED.welcome_message,
    business_type = EXCLUDED.business_type,
    intent_config_json = EXCLUDED.intent_config_json,
    faq_text = EXCLUDED.faq_text,
    knowledge_s3_key = EXCLUDED.knowledge_s3_key,
    dynamic_data_s3_key = EXCLUDED.dynamic_data_s3_key,
    dynamic_data_kind = EXCLUDED.dynamic_data_kind,
    business_hours_text = EXCLUDED.business_hours_text,
    contact_phone = EXCLUDED.contact_phone,
    contact_email_public = EXCLUDED.contact_email_public,
    transcript_email = EXCLUDED.transcript_email;

SELECT slug, display_name, business_type, knowledge_s3_key, contact_phone
FROM tenants WHERE slug = 'ludhiana-orthodontics';
