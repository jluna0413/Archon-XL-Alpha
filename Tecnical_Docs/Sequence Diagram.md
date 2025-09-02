## **Sequence Diagram (Mermaid.js)**

This diagram illustrates the "Code-to-UI-Test" workflow.

Code snippet

sequenceDiagram  
    participant User  
    participant ArchonUI  
    participant WorkflowEngine  
    participant MCPPlugin  
    participant AetherPlugin  
    participant AetherControlPlane

    User-\>\>ArchonUI: Start Workflow 'Deploy & Test Feature X'  
    ArchonUI-\>\>WorkflowEngine: Enqueue Workflow Run  
    WorkflowEngine-\>\>MCPPlugin: Execute Node: generate\_code(prompt)  
    MCPPlugin--\>\>WorkflowEngine: Return build\_artifact\_url  
    WorkflowEngine-\>\>AetherPlugin: Execute Node: execute\_task(app\_url, prompt)  
    AetherPlugin-\>\>AetherControlPlane: POST /ui-automation/sessions (app\_url)  
    AetherControlPlane--\>\>AetherPlugin: Return { sessionId }  
    AetherPlugin-\>\>AetherControlPlane: POST /sessions/{sessionId}/execute (prompt)  
    Note over AetherControlPlane: Mobile-Agent runs UI task on emulator...  
    AetherControlPlane--\>\>AetherPlugin: Return { status: SUCCESS, results\_url }  
    AetherPlugin--\>\>WorkflowEngine: Return { artifacts\_url }  
    WorkflowEngine-\>\>ArchonUI: Update Workflow Run Status: SUCCESS  
    ArchonUI-\>\>User: Display link to video recording and logs  
