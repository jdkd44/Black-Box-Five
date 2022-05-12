/* Table setup for database */

CREATE TABLE IF NOT EXISTS sensor_data (
    entryID INTEGER PRIMARY KEY,
    entry_time TEXT NOT NULL,
    x_acceleration REAL,
    y_acceleration REAL,
    z_acceleration REAL,
    velocity REAL,
    height REAL,
    longitude REAL,
    latitude REAL
);
