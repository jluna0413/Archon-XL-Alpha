## **1\. Architecture Decision Records (ADRs)**

These records document the key architectural decisions for the project.

### **ADR-001: Adopting a Plugin-Based Architecture**

* **Status:** Accepted  
* **Context:** The original Archon project was a monolithic application. The goals for Archon-XL include significant new capabilities (UI automation, advanced RL training, etc.) that require integration of disparate, complex systems. We need an architecture that supports modularity, extensibility, and independent development.  
* **Decision:** We will refactor the core Archon application into a plugin-based architecture. A central "Archon Core" will manage a standardized plugin interface for loading, configuring, and exposing services. Each major functionality (ART/MCP-RL, Aether/Mobile-Agent, Byterover, Cipher) will be implemented as a distinct plugin.  
* **Consequences:**  
  * **Pros:**  
    * Enables parallel development on different features.  
    * Allows third-party developers to extend the platform.  
    * Simplifies testing by allowing plugins to be mocked or isolated.  
    * Plugins can be enabled/disabled by users to customize their instance.  
  * **Cons:**  
    * Requires a well-defined and stable plugin API, adding initial development overhead.  
    * Potential for performance issues if the plugin communication layer is not optimized.

### **ADR-002: Creation of the "Aether Environment" for UI Automation**

* **Status:** Accepted  
* **Context:** The Mobile-Agent plugin needs a secure, scalable, and isolated environment to run mobile applications for UI testing. Using physical devices is not scalable or secure. Using simple local emulators does not provide necessary isolation or cloud-native management.  
* **Decision:** We will build the "Aether Environment," a dedicated, cloud-based service that manages a farm of virtualized mobile device emulators. This environment will be managed by a "Control Plane API" responsible for provisioning, terminating, and instrumenting the emulators. This decouples the UI automation environment from the core Archon-XL application.  
* **Consequences:**  
  * **Pros:**  
    * **High Security & Isolation:** Each test run occurs in a pristine, sandboxed environment that is destroyed afterward.  
    * **Scalability:** We can dynamically scale the number of emulators up or down based on demand.  
    * **Centralized Management:** Simplifies updates, monitoring, and app deployments for the test environment.  
  * **Cons:**  
    * Introduces significant infrastructure complexity and cost.  
    * Creates a new service that must be developed, maintained, and monitored.

### **ADR-003: Selection of Sim.AI for Workflow Orchestration**

* **Status:** Accepted  
* **Context:** Archon-XL requires a user-friendly way to orchestrate complex workflows that chain together actions from different plugins (e.g., code generation \-\> build \-\> UI test). We considered building a custom orchestrator, using a data-engineering tool like Apache Airflow, or integrating an existing open-source visual workflow builder.  
* **Decision:** We will integrate the open-source Sim.AI project as the core workflow builder. It will be wrapped within its own plugin and serve as the primary user interface for composing agentic tasks.  
* **Consequences:**  
  * **Pros:**  
    * Provides a mature, no-code/low-code visual interface out-of-the-box, saving significant development time.  
    * The tech stack (Next.js, PostgreSQL) is modern and aligns well with our expertise.  
    * Its open-source nature allows for future customization if needed.  
  * **Cons:**  
    * We are dependent on an external project's roadmap and maintenance.  
    * There may be a learning curve for integrating our specific plugin tools as custom nodes.

---

