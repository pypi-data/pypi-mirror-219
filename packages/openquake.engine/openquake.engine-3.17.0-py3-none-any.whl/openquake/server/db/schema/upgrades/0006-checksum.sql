CREATE TABLE checksum(
     job_id INTEGER PRIMARY KEY REFERENCES job (id) ON DELETE CASCADE,
     hazard_checksum INTEGER NOT NULL UNIQUE);
