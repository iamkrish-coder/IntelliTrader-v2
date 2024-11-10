/*
    IT_AU_Verify_User_Registration_FN: 
    This function retrieves the user registration details for the given email.
    
    Parameters:
    - param_user_email: The email address of the user.

    Exceptions:
    - Raises 'DB_USER_NOT_FOUND' if the email is not registered.
*/
DROP FUNCTION IF EXISTS IT_AU_Verify_User_Registration_FN;

CREATE OR REPLACE FUNCTION IT_AU_Verify_User_Registration_FN(
    IN param_user_email TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
    user_exists INT;
BEGIN
    -- Check if the user is registered
    SELECT COUNT(*) INTO user_exists
    FROM users 
    WHERE user_email = param_user_email;

    -- Raise an exception if no user is found
    IF user_exists = 0 THEN
        RAISE EXCEPTION 'DB_USER_NOT_FOUND';
    END IF;

    RETURN TRUE; -- Return true if user exists
END;
$$ LANGUAGE plpgsql;

