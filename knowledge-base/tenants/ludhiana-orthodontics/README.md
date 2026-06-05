# Ludhiana Orthodontics tenant assets

| File | S3 key | Purpose |
|------|--------|---------|
| `knowledge.md` | `tenants/ludhiana-orthodontics/knowledge.md` | Static FAQ / clinic info |

## Deploy

1. Run **`scripts/insert-tenant-ludhiana-orthodontics.sql`** on production RDS.
2. Upload KB to S3:

   ```bash
   aws s3 cp knowledge-base/tenants/ludhiana-orthodontics/knowledge.md s3://YOUR_BUCKET/tenants/ludhiana-orthodontics/knowledge.md
   ```

3. Chat: `https://ludhiana-orthodontics.myrobochat.com`

## Website note

KB rebuilt from official pages (Home, About, Services, Contact). The WordPress footer may contain injected spam links — the KB excludes those; clean the site with your host if needed.
