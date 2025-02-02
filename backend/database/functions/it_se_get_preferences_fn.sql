DROP FUNCTION IF EXISTS it_se_get_preferences_fn(p_user_id TEXT);

CREATE OR REPLACE FUNCTION it_se_get_preferences_fn(
    p_user_id TEXT
)
RETURNS SETOF preferences AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM preferences p
    WHERE p.user_id = p_user_id
    AND p.is_active = true
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
