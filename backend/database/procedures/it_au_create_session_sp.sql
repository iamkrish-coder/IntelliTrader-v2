DROP PROCEDURE IF EXISTS it_au_create_session_sp;
CREATE OR REPLACE PROCEDURE it_au_create_session_sp(
    p_session_token VARCHAR,
    p_user_id VARCHAR,
    p_expires TIMESTAMP WITH TIME ZONE,
    INOUT p_success BOOLEAN DEFAULT FALSE,
    INOUT p_data JSONB DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insert new session and return data in a single operation
    INSERT INTO sessions (
        sessionToken,
        userId,
        expires
    )
    VALUES (
        p_session_token,
        p_user_id,
        p_expires
    )
    RETURNING jsonb_build_object(
        'id', id,
        'sessionToken', session_token,
        'userId', user_id,
        'expires', expires
    ) INTO p_data;

    -- If we reach here, insertion was successful
    p_success := TRUE;

EXCEPTION  
    WHEN OTHERS THEN
        p_success := FALSE;
        p_data := jsonb_build_object(
            'error', SQLERRM,
            'state', SQLSTATE
        );
END;
$$;