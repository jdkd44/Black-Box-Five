/* Wipe all tables and rebuild database */

DROP TABLE IF EXISTS acc_data;
DROP TABLE IF EXISTS vel_data;
DROP TABLE IF EXISTS alt_data;
DROP TABLE IF EXISTS sensor_data;

VACUUM;