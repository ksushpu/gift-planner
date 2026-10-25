-- =============================================
-- Gift Planner: структура базы данных
-- =============================================

CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS gifts (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    idea TEXT NOT NULL,
    is_done INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (person_id) REFERENCES people(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
