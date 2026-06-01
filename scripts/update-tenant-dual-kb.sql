-- Dual KB: static FAQ (knowledge_s3_key) + dynamic data (dynamic_data_s3_key)
-- Run after deploy with new columns. Requires KNOWLEDGE_S3_BUCKET on ECS.

UPDATE tenants
SET
  knowledge_s3_key = 'tenants/siyu/knowledge.md',
  dynamic_data_s3_key = 'tenants/siyu/inventory.csv',
  dynamic_data_kind = 'inventory_csv',
  business_type = 'retail_electronics'
WHERE slug = 'siyu';

UPDATE tenants
SET
  knowledge_s3_key = 'tenants/india-gate/knowledge.md',
  dynamic_data_s3_key = NULL,
  dynamic_data_kind = 'none',
  business_type = 'restaurant'
WHERE slug = 'india-gate';

SELECT slug, knowledge_s3_key, dynamic_data_s3_key, dynamic_data_kind, business_type
FROM tenants
WHERE slug IN ('siyu', 'india-gate');
