BEGIN;

-- Drop objects if they exist (for clean rollback/rerun)
DROP TABLE IF EXISTS preferences CASCADE;

-- Create role if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_user') THEN
        CREATE ROLE app_user;
    END IF;
END
$$;

-- Create the preferences table
CREATE TABLE preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES "User"(id),
    
    -- General Settings
    debugger_mode BOOLEAN DEFAULT false,
    log_level VARCHAR(10) DEFAULT 'DEBUG',
    reset_app BOOLEAN DEFAULT false,
    prettier_print BOOLEAN DEFAULT false,
    
    -- Trade Settings
    live_trade BOOLEAN DEFAULT false,
    topic_type VARCHAR(10) DEFAULT 'FIFO',
    queue_type VARCHAR(10) DEFAULT 'FIFO',
    strategy VARCHAR(10) DEFAULT '001',
    historical_data_subscription BOOLEAN DEFAULT true,
    global_trade BOOLEAN DEFAULT true,
    runtime_interval VARCHAR(20) DEFAULT '5MINUTE',
    
    -- System Settings
    secret_name VARCHAR(100) DEFAULT 'IntelliTrader',
    region_name VARCHAR(20) DEFAULT 'ap-south-1',
    
    -- Audit Fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT NOT NULL REFERENCES "User"(id),
    updated_by TEXT NOT NULL REFERENCES "User"(id),
    is_active BOOLEAN DEFAULT true,

    -- Add constraints
    CONSTRAINT chk_log_level CHECK (log_level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR')),
    CONSTRAINT chk_runtime_interval CHECK (runtime_interval IN ('1MINUTE', '5MINUTE', '15MINUTE', '30MINUTE', '1HOUR')),
    CONSTRAINT chk_queue_type CHECK (queue_type IN ('FIFO', 'STANDARD')),
    CONSTRAINT chk_topic_type CHECK (topic_type IN ('FIFO', 'STANDARD'))
);

-- Create index
CREATE INDEX idx_preferences_user_id ON preferences(user_id);

-- Add comments
COMMENT ON TABLE preferences IS 'Stores user preferences and settings for the trading application';
COMMENT ON COLUMN preferences.user_id IS 'Reference to the user who owns these preferences';
COMMENT ON COLUMN preferences.is_active IS 'Soft delete flag';
COMMENT ON COLUMN preferences.log_level IS 'Logging level (DEBUG, INFO, WARNING, ERROR)';
COMMENT ON COLUMN preferences.runtime_interval IS 'Trading runtime interval (1MINUTE, 5MINUTE, etc)';
COMMENT ON COLUMN preferences.topic_type IS 'Message queue topic type (FIFO, etc)';
COMMENT ON COLUMN preferences.queue_type IS 'Message queue type (FIFO, etc)';
COMMENT ON COLUMN preferences.strategy IS 'Trading strategy identifier';
COMMENT ON COLUMN preferences.region_name IS 'AWS region name';

COMMIT;
