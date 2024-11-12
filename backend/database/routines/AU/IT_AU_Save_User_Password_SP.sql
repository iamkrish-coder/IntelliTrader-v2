/*
    IT_AU_Save_User_Password_SP: 
    This stored procedure handles the saving of the user password.

    Parameters: 
    - param_user_email: The email address of the user.
    - param_user_hashed_password: The hashed password of the user.
    - param_user_password_salt: The salt of the user password.
*/
DROP PROCEDURE IF EXISTS IT_AU_Save_User_Password_SP;

CREATE OR REPLACE PROCEDURE IT_AU_Save_User_Password_SP (
    IN param_user_email VARCHAR(50),
    IN param_user_hashed_password VARCHAR(255),
    IN param_user_password_salt VARCHAR(255)
)
AS $$
BEGIN
    -- Logic to save the user password
    UPDATE users
    SET user_password = param_user_hashed_password, user_password_salt = param_user_password_salt
    WHERE user_email = param_user_email;
END;
$$ LANGUAGE plpgsql;

