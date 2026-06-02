-- Set business_type for intent templates (run after deploy with new columns).
-- Safe if columns missing: run after app startup once (ensure_phase1_schema adds them).

UPDATE tenants SET business_type = 'retail_electronics' WHERE slug = 'siyu';
UPDATE tenants SET business_type = 'restaurant' WHERE slug = 'india-gate';
UPDATE tenants SET business_type = 'general' WHERE slug = 'demo' AND (business_type IS NULL OR business_type = '');
