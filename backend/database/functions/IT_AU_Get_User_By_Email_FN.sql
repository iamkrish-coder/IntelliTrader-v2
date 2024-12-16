-- Function: IT_AU_Get_User_By_Email_FN
-- Module: AU (Authentication)
-- Description: Get user information by email
-- Last Modified: 2024-01-21

-- Drop existing function if it exists
DROP FUNCTION IF EXISTS IT_AU_Get_User_By_Email_FN CASCADE;

CREATE OR REPLACE FUNCTION IT_AU_Get_User_By_Email_FN(
    p_email VARCHAR(255)
)
RETURNS TABLE (
    status INTEGER,
    message VARCHAR(255),
    data JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_status INTEGER;
    v_message VARCHAR(255);
    v_data JSONB;
BEGIN
    -- Initialize variables
    v_status := 0;
    v_message := '';
    v_data := NULL;

    -- Get user data by email
    v_data := (
        SELECT jsonb_build_object(
            'id', id,
            'email', email,
            'name', name,
            'picture', picture,
            'provider_id', provider_id,
            'oauth_provider', oauth_provider,
            'created_at', created_at,
            'updated_at', updated_at
        )
        FROM users
        WHERE email = p_email
    );

    IF v_data IS NOT NULL THEN
        v_status := 1;
        v_message := 'User found successfully';
    ELSE
        v_status := 0;
        v_message := 'User not found';
    END IF;

    RETURN QUERY SELECT v_status, v_message, v_data;

EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY SELECT -1, 'Error getting User: ' || SQLERRM, NULL::jsonb;
END;
$$;
