## **Data Models & Schema Definitions**

The following SQL statements define the core tables for the PostgreSQL database.

SQL

\-- For managing users of the Archon-XL platform  
CREATE TABLE users (  
    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),  
    email VARCHAR(255) UNIQUE NOT NULL,  
    hashed\_password VARCHAR(255) NOT NULL,  
    created\_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  
);

\-- For storing plugin status and configurations  
CREATE TABLE plugins (  
    id VARCHAR(100) PRIMARY KEY, \-- e.g., 'aether-mobile-agent'  
    is\_enabled BOOLEAN NOT NULL DEFAULT TRUE,  
    configuration JSONB, \-- Stores plugin-specific settings  
    updated\_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  
);

\-- For storing the visual workflow definitions from Sim.AI  
CREATE TABLE workflows (  
    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),  
    user\_id UUID REFERENCES users(id) ON DELETE CASCADE,  
    name VARCHAR(255) NOT NULL,  
    definition JSONB NOT NULL, \-- The entire Sim.AI graph structure  
    created\_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  
    updated\_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  
);

\-- For logging each execution of a workflow  
CREATE TABLE workflow\_runs (  
    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),  
    workflow\_id UUID REFERENCES workflows(id) ON DELETE CASCADE,  
    status VARCHAR(50) NOT NULL, \-- PENDING, RUNNING, SUCCESS, FAILED  
    started\_at TIMESTAMPTZ,  
    completed\_at TIMESTAMPTZ,  
    results JSONB \-- Stores the final output and links to artifacts  
);

\-- For tracking each UI automation session in the Aether environment  
CREATE TABLE aether\_sessions (  
    id UUID PRIMARY KEY, \-- Corresponds to the sessionId in the API  
    workflow\_run\_id UUID REFERENCES workflow\_runs(id) ON DELETE SET NULL,  
    status VARCHAR(50) NOT NULL,  
    artifacts\_url VARCHAR(512),  
    created\_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  
);

