/* Table setup for database */

CREATE TABLE IF NOT EXISTS acc_data (
    time INTEGER PRIMARY KEY,
    lateral_acc REAL NOT NULL,
    vertical_acc REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS vel_data (
    time INTEGER PRIMARY KEY,
    vel REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS alt_data (
    time INTEGER PRIMARY KEY,
    height REAL NOT NULL
);