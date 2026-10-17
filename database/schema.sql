-- YoruTerminal database schema

PRAGMA foreign_keys = ON;

-- 1. User accounts
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 2. Player progression
CREATE TABLE IF NOT EXISTS player_progress (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER NOT NULL DEFAULT 0 CHECK (xp >= 0),
    rank TEXT NOT NULL DEFAULT 'Novice',
    missions_completed INTEGER NOT NULL DEFAULT 0
        CHECK (missions_completed >= 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Mission definitions
CREATE TABLE IF NOT EXISTS missions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL
        CHECK (difficulty IN ('Beginner', 'Intermediate', 'Advanced'))
);

-- 4. Individual mission attempts
CREATE TABLE IF NOT EXISTS mission_results (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    mission_id TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0),
    completed INTEGER NOT NULL CHECK (completed IN (0, 1)),
    xp_awarded INTEGER NOT NULL DEFAULT 0 CHECK (xp_awarded >= 0),
    attempted_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(id)
);

-- 5. First-completion reward tracking
CREATE TABLE IF NOT EXISTS mission_completions (
    user_id INTEGER NOT NULL,
    mission_id TEXT NOT NULL,
    first_completed_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, mission_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(id)
);

-- Indexes for common account history queries
CREATE INDEX IF NOT EXISTS idx_results_user_attempted
    ON mission_results(user_id, attempted_at);

CREATE INDEX IF NOT EXISTS idx_results_user_mission
    ON mission_results(user_id, mission_id);
