CREATE TABLE IF NOT EXISTS users
(
    id SERIAL,
    name VARCHAR(255),
    email VARCHAR(255),
    "emailVerified" TIMESTAMPTZ,
    image TEXT,

    PRIMARY KEY (id)
); 