DROP FUNCTION IF EXISTS it_au_get_user_by_account_fn;
CREATE OR REPLACE FUNCTION it_au_get_user_by_account_fn(
    p_provider VARCHAR,
    p_provider_account_id VARCHAR
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    "emailVerified" TIMESTAMPTZ,
    image TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.name,
        u.email,
        u."emailVerified",
        u.image
    FROM users u
    INNER JOIN accounts a ON u.id = a."userId"
    WHERE a.provider = p_provider 
    AND a."providerAccountId" = p_provider_account_id;
END;
$$; 