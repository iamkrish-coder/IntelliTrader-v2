-- Table: verification_token
-- Module: (Authentication) AU
-- Description: User authentication and profile data
-- Last Modified: 2024-12-26

CREATE TABLE IF NOT EXISTS verification_token (
    identifier TEXT NOT NULL,
    expires TIMESTAMPTZ NOT NULL,
    token TEXT NOT NULL,

    PRIMARY KEY (identifier, token)
);
