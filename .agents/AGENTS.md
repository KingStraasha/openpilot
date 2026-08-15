# Workspace Rules

- The default root folder for all repository downloads and workspaces is `/srv/workspaces`.
- Keep all code pushes strictly private to the user's personal fork (`KingStraasha/bluepilot`). Do NOT open pull requests or push to `BluePilotDev` unless explicitly requested by the user.
- **Target Hardware**: The target hardware device for this project is always the **Comma 4** (running AGNOS / MICI architecture). All build systems (SCons), platform detection logic, hardware abstractions, and configurations must prioritize and support the Comma 4.
