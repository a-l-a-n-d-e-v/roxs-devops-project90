-- This script will be executed when the PostgreSQL container starts
-- It will be run by the postgres user with superuser privileges

-- Connect to the votes database
\c votes

-- Create the votes table if it doesn't exist
CREATE TABLE IF NOT EXISTS votes (
    id VARCHAR(255) PRIMARY KEY,
    vote VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the vote column for better query performance
CREATE INDEX IF NOT EXISTS idx_vote ON votes(vote);

-- Grant all privileges to the postgres user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Notify that the initialization is complete
SELECT 'Votes table created successfully' as message;
