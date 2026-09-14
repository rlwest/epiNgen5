# EpiEngine 5

EpiEngine is a lightweight template for building cognitive models. It includes engine components and teaching examples that serve as working resources: you can study them, modify them, copy and rename them, or replace them to suit a new model.

To begin a project, make a copy of the EpiEngine template and name that copy for the project. That copy becomes the project’s own standalone EpiEngine workspace, with its own model files and any engine components the project needs. The teaching examples remain available as starting points, but they are not requirements for the finished model.

This is an instance-based way of organizing projects. Each project has its own instance of EpiEngine, which can evolve independently. Projects do not all run through one central EpiEngine installation.

## Philosophy of EpiEngine

Established cognitive architectures such as ACT-R and Soar generally provide a shared, relatively stable set of mechanisms. Researchers build models within that common architecture; preserving its core helps test whether a unified account can explain behavior across many tasks.

EpiEngine has a different purpose. It is a computational architecture for constructing cognitive architectures, not a single cognitive architecture that all projects must adopt. It is especially suited to production-based, Common Model-style architectures. A project that aims to model ACT-R-like or Soar-like behavior in EpiEngine must explicitly assemble the relevant modules, memory systems, buffers, production rules, and timing assumptions; other projects can assemble different architectures.

This flexibility makes EpiEngine an experimental space for trying out and comparing architectural ideas. Researchers can explore a proposed mechanism in a standalone project before deciding whether it merits a change to an established unified architecture. EpiEngine supports that exploration without requiring every project to make the same architectural commitments.
