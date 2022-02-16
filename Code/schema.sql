/* Table setup for database */

CREATE TABLE IF NOT EXISTS sensor_data (
    entryID = INTEGER PRIMARY KEY,
    entry_time TEXT NOT NULL,
    lateral_acceleration REAL,
    vertical_acceleration REAL,
    velocity REAL,
    height REAL 
);
