-- Get User Preferences Function
/*
Description:
This function retrieves the active preferences for a given user from the preferences table.

Parameters:
- p_user_id TEXT: The unique identifier of the user whose preferences are being retrieved.

Returns:
SETOF preferences: Returns a set of rows from the preferences table matching the user_id and is_active conditions.

Usage:
SELECT * FROM it_se_get_preferences_fn('user123');

Notes:
- Only active preferences (is_active = true) are returned.
- The function returns at most one row, as enforced by the LIMIT 1 clause.
- If no matching preferences are found, an empty set is returned.
*/

DROP FUNCTION IF EXISTS it_se_get_preferences_fn(TEXT);
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
