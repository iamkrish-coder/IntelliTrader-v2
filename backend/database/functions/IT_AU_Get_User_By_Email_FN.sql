DROP FUNCTION IF EXISTS it_au_get_user_by_email_fn;
CREATE OR REPLACE FUNCTION it_au_get_user_by_email_fn(p_user_email VARCHAR)
RETURNS SETOF users
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id, 
        name, 
        email, 
        "emailVerified", 
        image
    FROM 
        users
    WHERE 
        email = p_user_email;
END;
$$;
