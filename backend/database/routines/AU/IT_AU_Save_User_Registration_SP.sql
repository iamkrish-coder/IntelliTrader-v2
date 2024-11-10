/*
    IT_AU_Save_User_Registration_SP: 
    This stored procedure handles the registration of a new user in the database.
    
    Parameters:
    - param_user_full_name: The full name of the user.
    - param_user_email: The email address of the user (must be unique).
    - param_user_hashed_password: The hashed password for the user.
    - param_user_password_salt: The salt used for hashing the password.
    
    Exceptions:
    - Raises 'DB_USER_ALREADY_EXISTS' if the email is already registered.
*/
DROP PROCEDURE IF EXISTS IT_AU_Save_User_Registration_SP;

CREATE OR REPLACE PROCEDURE IT_AU_Save_User_Registration_SP (
    IN param_user_full_name VARCHAR(50),
    IN param_user_email VARCHAR(50),
    IN param_user_hashed_password VARCHAR(100),
    IN param_user_password_salt VARCHAR(100)
)
AS $$
DECLARE 
    user_exists INT;
BEGIN
    -- Check if the user already exists
    SELECT COUNT(*) INTO user_exists
    FROM users
    WHERE user_email = param_user_email;

    IF user_exists > 0 THEN
        RAISE EXCEPTION 'DB_USER_ALREADY_EXISTS'; 
    ELSE
        -- Insert new user into the database
        INSERT INTO users (
            user_full_name, 
            user_email, 
            user_password, 
            user_password_salt
        )
        VALUES (
            param_user_full_name, 
            param_user_email, 
            param_user_hashed_password, 
            param_user_password_salt
        );
    END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE;  
END
$$ LANGUAGE plpgsql;
