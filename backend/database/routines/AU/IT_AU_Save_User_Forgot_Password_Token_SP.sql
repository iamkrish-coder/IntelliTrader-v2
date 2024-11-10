/*
    IT_AU_Save_User_Forgot_Password_Token_SP: 
    This stored procedure handles the saving of the forgot password token for a user.

    Parameters: 
    - param_user_email: The email address of the user.
    - param_forgot_password_token: The forgot password token for the user.
*/
DROP PROCEDURE IF EXISTS IT_AU_Save_User_Forgot_Password_Token_SP;

CREATE OR REPLACE PROCEDURE IT_AU_Save_User_Forgot_Password_Token_SP (
    IN param_user_email VARCHAR(50),
    IN param_forgot_password_token VARCHAR(255)
)
AS $$
BEGIN
    -- Logic to save the forgot password token
    UPDATE users
    SET user_password_reset_token = param_forgot_password_token
    WHERE user_email = param_user_email;
END;
$$ LANGUAGE plpgsql;
