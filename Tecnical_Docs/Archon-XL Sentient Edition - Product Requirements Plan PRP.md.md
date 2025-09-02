Of course. Integrating a powerful and multifaceted capability like the Mobile-Agent plugin requires a deliberate and thoughtful approach to user interface and experience design. A system this complex must be managed through a clear, intuitive, and powerful UI.

I have re-architected the PRP to include a dedicated UI/UX section, detailing the necessary interface elements. This plan ensures that users can not only access the new capabilities but can also manage, configure, and orchestrate them seamlessly.

Here is the updated, production-ready PRP for Archon-XL: Sentient Edition, now complete with a comprehensive UI/UX architecture.



Archon-XL: Sentient Edition - Product Requirements Plan (PRP)

1.0 Introduction

This document outlines the strategic development of Archon-XL: Sentient Edition, a paradigm-shifting evolution of the Archon project. The primary goal is to create a fully integrated, extensible platform for AI-driven product development, bridging the entire lifecycle from ideation and coding to deployment and real-world user interface testing.

By refactoring Archon into a plugin-based architecture, we will integrate a suite of powerful capabilities: advanced agent training (ART/MCP-RL), persistent memory (Byterover), secure code execution (Cipher), visual workflow construction (Sim.AI), and—most critically—a groundbreaking visual automation layer powered by Mobile-Agent. This transforms Archon-XL into a system that not only writes and manages code but can also see, understand, and interact with graphical user interfaces like a human user, enabling true end-to-end automation.



2.0 Project Objectives

Develop a Unified, Modular Architecture: Refactor Archon into a robust, plugin-based platform that ensures scalability, maintainability, and seamless integration of diverse functionalities.

Achieve Autonomous Tool Mastery: Integrate the ART/MCP-RL plugin to enable AI agents to master programmatic tools (APIs, CLIs) through reinforcement learning, without human-labeled data.

Enable Visual UI Automation: Integrate the Mobile-Agent v3 project as a core plugin, empowering Archon-XL agents to operate mobile applications through a visual interface. This facilitates automated UI testing, interaction with non-API systems, and full product validation.

Provide an Intuitive Command Center: Design and build a comprehensive user interface that makes the platform's vast capabilities accessible, manageable, and easy to orchestrate.

Ensure Secure and Stateful Operations: Guarantee operational integrity through the Cipher plugin for sandboxed code execution and the Byterover plugin for persistent, version-controlled project memory.

Establish Ethical AI Governance: Implement a stringent framework for security, privacy, and ethical oversight, particularly concerning the visual automation capabilities of Mobile-Agent.



3.0 Core Integrations (Plugin Extensions)

3.1 Agent \& Automation (Open-RL + ART/MCP-RL Plugin)

The core engine for teaching agents to use programmatic tools and APIs. It remains foundational for backend logic and code-based tasks.

3.2 Workflow Builder (Sim.AI Plugin)

The central nervous system for Archon-XL. This visual interface will be used to chain together all other plugin functionalities into cohesive, automated workflows.

3.3 Secure Execution (Cipher Plugin)

Provides a secure, ephemeral environment for executing agent-generated code, preventing any potential harm to the host system.

3.4 Project Memory (Byterover Plugin)

Provides agents with long-term, context-aware memory, allowing them to recall past interactions, code structures, and project goals across multiple sessions.

3.5 Comprehensive MCP Tools

The 20 MCP tools for coding, project management, and DevOps remain essential for the code-generation half of the product lifecycle.

3.6 Visual Automation (Mobile-Agent Plugin)

This transformative plugin bridges the gap between code and user experience by giving Archon-XL the ability to operate applications via their graphical user interface.

Core Technology: Leverages a Vision-Language Model (VLM) for screen perception and action generation. The agent's self-reflection capability allows it to recover from errors.

Architectural Integration: The Aether Environment: A secure, cloud-based farm of on-demand Android/iOS emulators managed by a Control Plane API and a Secure Credential Vault.

Exposed Capabilities: The plugin will expose high-level tools to the Sim.AI workflow builder, such as ui\_automation.create\_session, ui\_automation.install\_app, and ui\_automation.execute\_task.



4.0 User Interface \& Experience (UI/UX) Architecture

The power of Archon-XL is only realized if its components can be easily managed and orchestrated. The UI will be designed as a Unified Command Center based on the following principles:

Modularity and Intuitiveness: The UI will mirror the plugin-based architecture. Each major plugin will have a dedicated, intuitive interface, while the Workflow Builder unifies them.

Transparency and Control: The user must always have a clear view of what the agents are doing, with the ability to intervene, configure, and manage their behavior.

Context-Awareness: The interface will adapt to provide the most relevant information and controls based on the user's current task.

4.1 Main Application Layout

A persistent, three-part layout will provide a consistent user experience:

Primary Navigation Bar (Left Sidebar): A vertical, icon-based navigation bar for switching between major views.

Main Content Area: The central workspace that displays the content for the currently selected view.

Global Status Bar (Bottom): A thin bar at the bottom displaying the status of background tasks (e.g., "RL Training in Progress," "Aether Emulator Booting," "Workflow 'X' Running").

4.2 Primary Navigation Bar \& Views

The navigation bar will provide direct access to the following core views:

\[Icon: Dashboard] Dashboard: The landing page. Provides a high-level overview of system status, recent workflow runs, active agents, and key performance metrics.

\[Icon: Workflow] Workflow Builder (Sim.AI): The primary workspace. This view will feature the Sim.AI drag-and-drop interface. A palette on the left will contain nodes representing all available tools, logically grouped by their source plugin (e.g., "MCP Tools," "Visual Automation Tools," "Memory Tools").

\[Icon: Mobile Device] Aether Control Center: A dedicated interface for managing the Visual Automation plugin. It will contain:

A list of active and recent emulator sessions.

A live-view option to watch the agent interact with an application in real-time.

A repository for managing application files (.apk/.ipa) to be used in tests.

Access to session artifacts (video recordings, action logs).

\[Icon: Brain] Project Memory (Byterover): An interface to browse, search, and manage the agent's long-term memory store. Users can inspect saved data and revert to previous versions.

\[Icon: Cog] Settings: A centralized area for platform and plugin configuration.

4.3 The Settings View

This view is critical for user control and will be organized into two main sections:

4.3.1 Plugin Management

A clean, list-based interface showing all installed plugins (ART/MCP-RL, Mobile-Agent, Cipher, etc.). Each entry will display:

Plugin Name \& Version

A brief description of its capability.

A master Enable/Disable toggle switch. Disabling a plugin will remove its tools from the Workflow Builder palette and its view from the main navigation bar.

4.3.2 Plugin Configuration

Clicking a plugin from the management list will open a dedicated configuration pane. This allows for granular control over each component:

ART/MCP-RL Config:

Dropdown to select the base LLM for training (e.g., GPT-4o, Llama 3).

Fields to adjust key training hyperparameters (learning rate, epochs).

API key management for the selected model.

Mobile-Agent / Aether Config:

Fields to input the Aether Control Plane API endpoint.

Default emulator configuration (e.g., device type: "Pixel 7," OS version: "Android 13").

Secure credential management for adding and rotating test user accounts in the vault.

Byterover Config:

Database connection string and credentials.

Configuration for memory pruning or TTL (Time-To-Live) policies.

4.4 Workflow Artifacts Viewer

This is a context-sensitive view, not a main navigation tab. After a workflow is executed, clicking on its run history will open this comprehensive viewer. It will feature a multi-tab layout to display all outputs from the run:

Summary Tab: High-level results, duration, and success/fail status.

Logs Tab: Raw, interleaved logs from all programmatic tools used in the workflow.

Visual Evidence Tab: If the Mobile-Agent was used, this tab will display the full video recording of the emulator session, synchronized with a step-by-step log of the agent's perceptions and actions (e.g., "Detected 'Login' button," "Tapped coordinates \[x, y]").



5.0 Development Roadmap

Phase 1: Core Architecture \& Environment Setup (Months 1-3)

Refactor Archon; design the Aether Environment; develop the ART/MCP-RL and Byterover plugins.

UI/UX: Wireframing of all major views and component library setup.

Phase 2: Core Plugins \& Visual Agent Integration (Months 4-6)

Develop Sim.AI, Cipher, and initial MCP tools.

Develop the core Mobile-Agent plugin and its communication with the Aether Control Plane.

Phase 3: UI Development \& Workflow Integration (Months 7-9)

UI/UX: Build out the primary UI shell: Navigation, Dashboard, and the complete Settings view with plugin management and configuration panels.

Integrate the Sim.AI plugin into the Workflow Builder view, populating its palette with tools from active plugins.

UI/UX: Develop the Aether Control Center for live session monitoring.

Phase 4: Beta Testing \& System Hardening (Months 10-12)

Conduct end-to-end testing of complex workflows.

UI/UX: Develop the Workflow Artifacts Viewer and gather specific user feedback on UI intuitiveness and workflow clarity.

Onboard beta testers and conduct security audits.



6.0 API \& Data Flow

The API structure remains the same, with the addition of endpoints for the UI to fetch configuration and status.

/settings/plugins: GET to list all plugins and their status/config, POST to update configurations.

/status/background-tasks: An endpoint for the global status bar to poll for ongoing operations.



7.0 Success Metrics

End-to-End Workflow Success: >90% success rate on a benchmark of complex, multi-plugin workflows.

Mobile-Agent Reliability: <5% error rate on a benchmark of 20 UI tasks.

Performance: Emulator provisioning < 90s; VLM action latency < 3s.

User Adoption \& Usability: Achieve a System Usability Scale (SUS) score of 80+ from beta testers, indicating a highly intuitive and effective user interface.



8.0 Ethical \& Security Considerations

The principles of Data Isolation, Secure Credential Handling, Preventing Misuse, and Transparency/Auditability remain paramount. The UI will support these principles by making audit logs and security configurations easily accessible to administrators.



9.0 Sources

Mobile-Agent Project: https://github.com/X-PLUG/MobileAgent

Archon (Original Project): https://github.com/coleam00/Archon

Open-RL, ART \& MCP-RL, Sim.AI: Respective GitHub repositories.



