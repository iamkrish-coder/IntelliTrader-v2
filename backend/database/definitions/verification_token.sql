CREATE TABLE IF NOT EXISTS verification_token
(
    identifier TEXT NOT NULL,
    expires TIMESTAMPTZ NOT NULL,
    token TEXT NOT NULL,

    PRIMARY KEY (identifier, token)
); 