-- Data Models & Schema Definitions (from Technical_Docs/Data Models & Schema Definitions.md)

-- For managing users of the Archon-XL platform
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- For storing plugin status and configurations
CREATE TABLE IF NOT EXISTS plugins (
    id VARCHAR(100) PRIMARY KEY,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    configuration JSONB,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- For storing the visual workflow definitions from Sim.AI
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    definition JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- For logging each execution of a workflow
CREATE TABLE IF NOT EXISTS workflow_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    results JSONB
);

-- For tracking each UI automation session in the Aether environment
CREATE TABLE IF NOT EXISTS aether_sessions (
    id UUID PRIMARY KEY,
    workflow_run_id UUID REFERENCES workflow_runs(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL,
    artifacts_url VARCHAR(512),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
