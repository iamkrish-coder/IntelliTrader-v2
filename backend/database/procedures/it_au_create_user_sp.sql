CREATE OR REPLACE PROCEDURE it_au_create_user_sp(
    p_email VARCHAR,
    p_name VARCHAR,
    INOUT p_success BOOLEAN DEFAULT FALSE,
    INOUT p_data JSONB DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insert operation here...
    p_success := TRUE;

EXCEPTION
    WHEN unique_violation THEN
        p_success := FALSE;
        p_data := handle_sp_exception(
            'unique_violation',
            SQLERRM,
            SQLSTATE,
            jsonb_build_object('email', p_email)
        );
    WHEN OTHERS THEN
        p_success := FALSE;
        p_data := handle_sp_exception(
            'others',
            SQLERRM,
            SQLSTATE,
            jsonb_build_object(
                'email', p_email,
                'hint', 'Unexpected database error occurred'
            )
        );
END;
$$; 