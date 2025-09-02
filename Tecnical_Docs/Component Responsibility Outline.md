## **Component Responsibility Outline**

* **Component: Archon Core (Flask Web Application)**  
  * **Responsibilities:**  
    * User authentication and management.  
    * Loading, enabling/disabling, and configuring plugins.  
    * Serving the main web interface (UI).  
    * Providing the primary API gateway.  
  * **Collaborators:** Database, Workflow Engine, all Plugins.  
* **Component: Workflow Engine (Celery \+ Redis)**  
  * **Responsibilities:**  
    * Executing workflow graphs asynchronously.  
    * Managing task queues, retries, and state.  
    * Invoking the correct plugin methods for each node in a workflow.  
  * **Collaborators:** Archon Core, all Plugins, Database.  
* **Component: Plugin: Aether (Mobile-Agent)**  
  * **Responsibilities:**  
    * Providing ui\_automation.\* tools to the workflow engine.  
    * Acting as the client for the Aether Control Plane API.  
    * Translating high-level workflow tasks into specific API calls.  
  * **Collaborators:** Workflow Engine, Aether Control Plane.  
* **Component: Aether Control Plane (Separate Microservice)**  
  * **Responsibilities:**  
    * Managing the lifecycle of cloud emulators (create, start, stop, destroy).  
    * Orchestrating the Mobile-Agent model to run on a given emulator.  
    * Storing and serving session artifacts (videos, logs).  
  * **Collaborators:** Cloud Provider API, Secure Artifact Storage.