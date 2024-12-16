-- Procedure: IT_AU_Create_User_Account_SP
-- Module: AU (Authentication)
-- Description: Save or update user registration information
-- Last Modified: 2024-01-21

-- Drop existing procedure if it exists
DROP PROCEDURE IF EXISTS IT_AU_Create_User_Account_SP CASCADE;

CREATE OR REPLACE PROCEDURE IT_AU_Create_User_Account_SP(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_picture VARCHAR(255),
    IN p_provider_id VARCHAR(255),
    IN p_oauth_provider VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_salt VARCHAR(255),
    OUT p_status INTEGER,
    OUT p_message VARCHAR(255),
    OUT p_data JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
    v_existing_user_id INTEGER;
BEGIN
    -- Initialize output parameters
    p_status := 0;
    p_message := '';

    -- Check if user already exists with the same email
    SELECT id INTO v_existing_user_id
    FROM users
    WHERE email = p_email;

    IF v_existing_user_id IS NOT NULL THEN
        -- Update existing user
        UPDATE users
        SET name = COALESCE(p_name, name),
            picture = COALESCE(p_picture, picture),
            provider_id = COALESCE(p_provider_id, provider_id),
            oauth_provider = COALESCE(p_oauth_provider, oauth_provider),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = v_existing_user_id
        RETURNING id INTO v_user_id;

        p_status := 1;
        p_message := 'User information updated successfully';
    ELSE
        -- Insert new user
        INSERT INTO users (
            email,
            name,
            picture,
            provider_id,
            oauth_provider,
            created_at,
            updated_at
        )
        VALUES (
            p_email,
            p_name,
            p_picture,
            p_provider_id,
            p_oauth_provider,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
        RETURNING id INTO v_user_id;

        p_status := 1;
        p_message := 'User registered successfully';
    END IF;

    -- Get updated user data
    p_data := (
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
        WHERE id = v_user_id
    );

EXCEPTION
    WHEN OTHERS THEN
        p_status := -1;
        p_message := 'Error saving user: ' || SQLERRM;
        p_data := NULL;
END;
$$;