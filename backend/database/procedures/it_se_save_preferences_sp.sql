DROP PROCEDURE IF EXISTS it_se_save_preferences_sp;
CREATE OR REPLACE PROCEDURE it_se_save_preferences_sp(
    -- User Information
    p_user_id TEXT,
    
    -- General Settings
    p_debugger_mode BOOLEAN,
    p_log_level VARCHAR(10),
    p_reset_app BOOLEAN,
    p_prettier_print BOOLEAN,
    
    -- Trade Settings
    p_live_trade BOOLEAN,
    p_topic_type VARCHAR(10),
    p_queue_type VARCHAR(10),
    p_strategy VARCHAR(10),
    p_historical_data_subscription BOOLEAN,
    p_global_trade BOOLEAN,
    p_runtime_interval VARCHAR(20),
    
    -- System Settings
    p_secret_name VARCHAR(100),
    p_region_name VARCHAR(20),
    
    -- Audit Fields
    p_updated_by TEXT,
    
    -- Output Parameters
    INOUT p_success BOOLEAN DEFAULT FALSE,
    INOUT p_message VARCHAR DEFAULT '',
    INOUT p_data JSONB DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_existing_id BIGINT;
    v_created_by TEXT;
BEGIN
    -- Check if preferences already exist for the user
    SELECT id, created_by 
    INTO v_existing_id, v_created_by
    FROM preferences 
    WHERE user_id = p_user_id AND is_active = true;

    IF v_existing_id IS NULL THEN
        -- Insert new preferences
        INSERT INTO preferences (
            user_id,
            debugger_mode,
            log_level,
            reset_app,
            prettier_print,
            live_trade,
            topic_type,
            queue_type,
            strategy,
            historical_data_subscription,
            global_trade,
            runtime_interval,
            secret_name,
            region_name,
            created_by,
            updated_by
        )
        VALUES (
            p_user_id,
            p_debugger_mode,
            p_log_level,
            p_reset_app,
            p_prettier_print,
            p_live_trade,
            p_topic_type,
            p_queue_type,
            p_strategy,
            p_historical_data_subscription,
            p_global_trade,
            p_runtime_interval,
            p_secret_name,
            p_region_name,
            p_updated_by, -- First time creator
            p_updated_by
        )
        RETURNING jsonb_build_object(
            'id', id,
            'user_id', user_id,
            'debugger_mode', debugger_mode,
            'log_level', log_level,
            'reset_app', reset_app,
            'prettier_print', prettier_print,
            'live_trade', live_trade,
            'topic_type', topic_type,
            'queue_type', queue_type,
            'strategy', strategy,
            'historical_data_subscription', historical_data_subscription,
            'global_trade', global_trade,
            'runtime_interval', runtime_interval,
            'secret_name', secret_name,
            'region_name', region_name,
            'created_at', created_at,
            'updated_at', updated_at,
            'created_by', created_by,
            'updated_by', updated_by,
            'is_active', is_active
        ) INTO p_data;

        p_message := 'Preferences created successfully';
    ELSE
        -- Update existing preferences
        UPDATE preferences
        SET 
            debugger_mode = p_debugger_mode,
            log_level = p_log_level,
            reset_app = p_reset_app,
            prettier_print = p_prettier_print,
            live_trade = p_live_trade,
            topic_type = p_topic_type,
            queue_type = p_queue_type,
            strategy = p_strategy,
            historical_data_subscription = p_historical_data_subscription,
            global_trade = p_global_trade,
            runtime_interval = p_runtime_interval,
            secret_name = p_secret_name,
            region_name = p_region_name,
            updated_by = p_updated_by
        WHERE id = v_existing_id
        RETURNING jsonb_build_object(
            'id', id,
            'user_id', user_id,
            'debugger_mode', debugger_mode,
            'log_level', log_level,
            'reset_app', reset_app,
            'prettier_print', prettier_print,
            'live_trade', live_trade,
            'topic_type', topic_type,
            'queue_type', queue_type,
            'strategy', strategy,
            'historical_data_subscription', historical_data_subscription,
            'global_trade', global_trade,
            'runtime_interval', runtime_interval,
            'secret_name', secret_name,
            'region_name', region_name,
            'created_at', created_at,
            'updated_at', updated_at,
            'created_by', created_by,
            'updated_by', updated_by,
            'is_active', is_active
        ) INTO p_data;

        p_message := 'Preferences updated successfully';
    END IF;

    p_success := TRUE;

EXCEPTION WHEN OTHERS THEN
    p_success := FALSE;
    p_message := 'Error saving preferences: ' || SQLERRM;
    p_data := jsonb_build_object(
        'error', SQLERRM,
        'state', SQLSTATE
    );
END;
$$;

-- Add comment
COMMENT ON PROCEDURE it_se_save_preferences_sp IS 'Stored procedure to save or update user preferences';
