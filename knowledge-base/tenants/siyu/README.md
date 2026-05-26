# Siyu tenant assets

| File | Purpose |
|------|---------|
| `knowledge.md` | **Merged** KB: business info + full inventory table (~200 SKUs) |
| `inventory.csv` | Source data for stock/prices — re-merge into `knowledge.md` after edits |

## Regenerate inventory + merged KB

```bash
python scripts/generate_siyu_inventory.py   # optional: new random SKUs
python scripts/merge_siyu_kb.py             # append CSV into knowledge.md
python scripts/generate_siyu_faq_sql.py     # optional: DB-only faq_text UPDATE
```

## Deploy (production, no plans)

1. Run **`scripts/insert-tenant-siyu.sql`** on RDS.  
   Phase 1 schema: **`scripts/insert-tenant-siyu-phase1.sql`**
2. **Knowledge for the chatbot** (pick one):
   - **S3 (recommended):** upload merged `knowledge.md` only:
     ```bash
     aws s3 cp knowledge-base/tenants/siyu/knowledge.md s3://YOUR_BUCKET/tenants/siyu/knowledge.md
     ```
     ECS: `KNOWLEDGE_S3_BUCKET=YOUR_BUCKET`, tenant `knowledge_s3_key = tenants/siyu/knowledge.md`
   - **No S3:** after merge, run generated **`scripts/update-siyu-faq-from-kb.sql`** (sets full KB on `faq_text`)
3. Chat: `https://YOUR-ALB/b/siyu`

`inventory.csv` is **not** loaded separately by the app — stock answers come from the CSV block inside `knowledge.md`.
