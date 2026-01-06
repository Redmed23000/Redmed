CREATE TABLE IF NOT EXISTS codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    time_unit_minutes INTEGER NOT NULL,
    source_version TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT
);

CREATE TABLE IF NOT EXISTS exclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_id INTEGER NOT NULL,
    excluded_code TEXT NOT NULL,
    reason TEXT,
    source_version TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT,
    FOREIGN KEY (code_id) REFERENCES codes(id)
);

CREATE TABLE IF NOT EXISTS incompatibilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_id_a INTEGER NOT NULL,
    code_id_b INTEGER NOT NULL,
    reason TEXT,
    source_version TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT,
    FOREIGN KEY (code_id_a) REFERENCES codes(id),
    FOREIGN KEY (code_id_b) REFERENCES codes(id)
);

CREATE TABLE IF NOT EXISTS conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_id INTEGER NOT NULL,
    expression TEXT NOT NULL,
    message TEXT,
    source_version TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT,
    FOREIGN KEY (code_id) REFERENCES codes(id)
);

CREATE TABLE IF NOT EXISTS limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_id INTEGER NOT NULL,
    limit_type TEXT NOT NULL,
    value INTEGER NOT NULL,
    period TEXT NOT NULL,
    message TEXT,
    source_version TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT,
    FOREIGN KEY (code_id) REFERENCES codes(id)
);

CREATE TABLE IF NOT EXISTS tardoc_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_version TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    summary TEXT NOT NULL
);
