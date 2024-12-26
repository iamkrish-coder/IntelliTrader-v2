-- Table: users
-- Module: (Authentication) AU
-- Description: User authentication and profile data
-- Last Modified: 2024-12-26

CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    name VARCHAR(255),
    email VARCHAR(255),
    "emailVerified" TIMESTAMPTZ,
    image TEXT,

    PRIMARY KEY (id)
);
