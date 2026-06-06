# Siyu tenant assets

| File | S3 key | Purpose |
|------|--------|---------|
| `knowledge.md` | `tenants/siyu/knowledge.md` | **Static FAQ** — shop info, policies (small) |
| `inventory.csv` | `tenants/siyu/inventory.csv` | **Dynamic stock** — loaded only for stock/price intents |
| `images/*.jpg` | `tenants/siyu/images/` | **Product thumbnails** — optional; URL in `image_url` column |

## Regenerate

```bash
python scripts/generate_siyu_inventory.py   # optional: new SKUs
python scripts/merge_siyu_kb.py             # rebuild static knowledge.md (FAQ only)
```

## Deploy

1. Run **`scripts/insert-tenant-siyu.sql`** (sets `knowledge_s3_key` + `dynamic_data_s3_key`).
2. Upload **both** files to S3:
   ```bash
   aws s3 cp knowledge-base/tenants/siyu/knowledge.md s3://YOUR_BUCKET/tenants/siyu/knowledge.md
   aws s3 cp knowledge-base/tenants/siyu/inventory.csv s3://YOUR_BUCKET/tenants/siyu/inventory.csv
   aws s3 cp knowledge-base/tenants/siyu/images/SYU-1001.jpg s3://YOUR_BUCKET/tenants/siyu/images/SYU-1001.jpg
   ```

   Add **`image_url`** to `inventory.csv` (HTTPS URL per SKU). Chat shows thumbnails when the bot includes that URL.
3. ECS: `KNOWLEDGE_S3_BUCKET=YOUR_BUCKET`
4. Existing tenants: **`scripts/update-tenant-dual-kb.sql`**

## How the app uses them

- **Hi / hours / contact** → static FAQ or fast reply (no inventory file).
- **Stock / price questions** → static FAQ + **inventory.csv lookup** (top matching rows).
- **Unclear intent** → static FAQ + LLM only.
