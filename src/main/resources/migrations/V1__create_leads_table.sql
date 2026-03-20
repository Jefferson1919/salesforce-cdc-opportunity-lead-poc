-- Migration V1: Create leads table
-- Apply: sqlite3 src/main/resources/leads.db < src/main/resources/migrations/V1__create_leads_table.sql

CREATE TABLE IF NOT EXISTS leads (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sf_id               TEXT NOT NULL UNIQUE,
    first_name          TEXT,
    last_name           TEXT,
    email               TEXT,
    phone               TEXT,
    company             TEXT,
    status              TEXT,
    lead_source         TEXT,
    change_type         TEXT,
    change_origin       TEXT,
    replay_id           TEXT,
    created_date        TEXT,
    last_modified_date  TEXT,
    synced_at           TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_leads_sf_id       ON leads(sf_id);
CREATE INDEX IF NOT EXISTS idx_leads_change_type  ON leads(change_type);
