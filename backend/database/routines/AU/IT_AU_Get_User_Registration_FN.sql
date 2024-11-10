/*
    IT_AU_Get_User_Registration_FN: 
    This function retrieves the user registration details for the given email.

    Parameters:
    - param_user_email: The email address of the user.

    Exceptions:
    - Raises 'DB_USER_NOT_FOUND' if the email is not registered.
*/
DROP FUNCTION IF EXISTS IT_AU_Get_User_Registration_FN;

CREATE OR REPLACE FUNCTION IT_AU_Get_User_Registration_FN(
    IN param_user_email VARCHAR(50)
)
RETURNS TABLE (
    user_id INT,
    user_full_name VARCHAR,
    user_email VARCHAR,
    user_password VARCHAR,
    user_password_salt VARCHAR,
    user_created_at TIMESTAMP
) AS $$
BEGIN
    -- Attempt to retrieve the user by email
    RETURN QUERY
    SELECT 
        u.user_id, 
        u.user_full_name, 
        u.user_email, 
        u.user_password, 
        u.user_password_salt, 
        u.user_created_at
    FROM 
        users u
    WHERE 
        u.user_email = param_user_email;
    
    -- Raise an exception if no user is found
    IF NOT FOUND THEN
        RAISE EXCEPTION 'DB_USER_NOT_FOUND';
    END IF;
END;
$$ LANGUAGE plpgsql;

