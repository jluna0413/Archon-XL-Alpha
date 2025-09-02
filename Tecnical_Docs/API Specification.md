##  **API Specification (OpenAPI 3.0)**

This specification defines the contract for the new /ui-automation service, which is the public-facing API for the Aether Environment.

YAML

openapi: 3.0.1  
info:  
  title: Archon-XL Aether Control Plane API  
  description: API for managing and interacting with the visual UI automation environment.  
  version: 1.0.0  
servers:  
  \- url: https://api.archon-xl.com/v1

paths:  
  /ui-automation/sessions:  
    post:  
      summary: Create a new UI Automation Session  
      description: Provisions a new emulator instance in the Aether Environment for a test run.  
      requestBody:  
        required: true  
        content:  
          application/json:  
            schema:  
              $ref: '\#/components/schemas/SessionConfigRequest'  
      responses:  
        '202':  
          description: Accepted. The session is being provisioned.  
          content:  
            application/json:  
              schema:  
                $ref: '\#/components/schemas/Session'  
        '400':  
          description: Invalid configuration request.

  /ui-automation/sessions/{sessionId}:  
    get:  
      summary: Get Session Status  
      parameters:  
        \- name: sessionId  
          in: path  
          required: true  
          schema:  
            type: string  
            format: uuid  
      responses:  
        '200':  
          description: The current session details.  
          content:  
            application/json:  
              schema:  
                $ref: '\#/components/schemas/Session'  
        '404':  
          description: Session not found.

  /ui-automation/sessions/{sessionId}/execute:  
    post:  
      summary: Execute a Task in the Session  
      parameters:  
        \- name: sessionId  
          in: path  
          required: true  
          schema:  
            type: string  
            format: uuid  
      requestBody:  
        required: true  
        content:  
          application/json:  
            schema:  
              $ref: '\#/components/schemas/ExecutionRequest'  
      responses:  
        '200':  
          description: Task execution completed successfully.  
          content:  
            application/json:  
              schema:  
                $ref: '\#/components/schemas/ExecutionResult'  
        '422':  
          description: Task could not be completed (e.g., UI element not found).

  /ui-automation/sessions/{sessionId}/artifacts:  
    get:  
      summary: Get Session Artifacts  
      parameters:  
        \- name: sessionId  
          in: path  
          required: true  
          schema:  
            type: string  
            format: uuid  
      responses:  
        '200':  
          description: A list of available artifacts for the session.  
          content:  
            application/json:  
              schema:  
                $ref: '\#/components/schemas/Artifacts'

components:  
  schemas:  
    SessionConfigRequest:  
      type: object  
      properties:  
        device\_type:  
          type: string  
          example: "Pixel\_7"  
        os\_version:  
          type: string  
          example: "Android\_13"  
        app\_url:  
          type: string  
          format: uri  
          description: URL to the .apk or .ipa file to be pre-installed.  
    Session:  
      type: object  
      properties:  
        sessionId:  
          type: string  
          format: uuid  
        status:  
          type: string  
          enum: \[PROVISIONING, READY, RUNNING, COMPLETED, FAILED\]  
        createdAt:  
          type: string  
          format: date-time  
    ExecutionRequest:  
      type: object  
      properties:  
        prompt:  
          type: string  
          description: The natural language instruction for the agent.  
          example: "Log in with username 'testuser' and password from the vault, then navigate to the settings page."  
        credentials\_key:  
          type: string  
          description: Optional key to retrieve credentials from the secure vault.  
    ExecutionResult:  
      type: object  
      properties:  
        status:  
          type: string  
          enum: \[SUCCESS, FAILURE\]  
        message:  
          type: string  
          example: "Successfully navigated to the settings page."  
        final\_screenshot\_url:  
          type: string  
          format: uri  
    Artifacts:  
      type: object  
      properties:  
        video\_recording\_url:  
          type: string  
          format: uri  
        action\_log\_url:  
          type: string  
          format: uri

---

