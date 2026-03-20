-- Migration V2: Create opportunities table
-- Apply: sqlite3 src/main/resources/leads.db < src/main/resources/migrations/V2__create_opportunities_table.sql

CREATE TABLE IF NOT EXISTS opportunities (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sf_id               TEXT NOT NULL UNIQUE,
    opportunity_name    TEXT,
    amount              REAL,
    stage_name          TEXT,
    close_date          TEXT,
    probability         REAL,
    account_id          TEXT,
    owner_id            TEXT,
    type                TEXT,
    lead_source         TEXT,
    currency_iso_code   TEXT,
    description         TEXT,
    change_type         TEXT,
    change_origin       TEXT,
    replay_id           TEXT,
    created_date        TEXT,
    last_modified_date  TEXT,
    synced_at           TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_opportunities_sf_id       ON opportunities(sf_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_change_type  ON opportunities(change_type);
