-- Run on RDS after deploy (Phase 1). Seeds plans if missing and wires india-gate to Premium.

INSERT INTO plans (id, code, display_name, max_sessions_per_month, entitlements_json)
VALUES
  (gen_random_uuid(), 'basic', 'Basic', 200, '{"images":false,"appointments":false,"orders":false,"kb_suggestions":false}'),
  (gen_random_uuid(), 'advanced', 'Advanced', 2000, '{"images":true,"appointments":false,"orders":false,"kb_suggestions":true}'),
  (gen_random_uuid(), 'premium', 'Premium', 20000, '{"images":true,"appointments":true,"orders":true,"kb_suggestions":true}')
ON CONFLICT (code) DO NOTHING;

UPDATE tenants
SET
  status = 'active',
  plan_id = (SELECT id FROM plans WHERE code = 'premium' LIMIT 1)
WHERE slug = 'india-gate';

-- Optional: assign demo to Basic
UPDATE tenants
SET
  status = 'active',
  plan_id = (SELECT id FROM plans WHERE code = 'basic' LIMIT 1)
WHERE slug = 'demo' AND plan_id IS NULL;
