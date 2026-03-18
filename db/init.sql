-- Salesforce CDC POC - Leads table
-- SQLite init script

CREATE TABLE IF NOT EXISTS leads (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sf_id               TEXT NOT NULL UNIQUE,       -- Salesforce Lead ID (18-char)
    first_name          TEXT,
    last_name           TEXT NOT NULL,
    email               TEXT,
    phone               TEXT,
    company             TEXT,
    status              TEXT,
    lead_source         TEXT,
    -- CDC metadata
    change_type         TEXT NOT NULL,              -- CREATED, UPDATED, DELETED, UNDELETED
    change_origin       TEXT,
    replay_id           TEXT,
    created_date        TEXT,                       -- ISO 8601
    last_modified_date  TEXT,                       -- ISO 8601
    synced_at           TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_leads_sf_id ON leads(sf_id);
CREATE INDEX IF NOT EXISTS idx_leads_change_type ON leads(change_type);
