-- Table: sessions
-- Module: (Authentication) AU
-- Description: User authentication and profile data
-- Last Modified: 2024-12-26

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL,
    "userId" INTEGER NOT NULL,
    expires TIMESTAMPTZ NOT NULL,
    "sessionToken" VARCHAR(255) NOT NULL,

    PRIMARY KEY (id)
);
