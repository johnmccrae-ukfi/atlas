# atlas
Enterprise AI Intelligence Platform powered by Microsoft Fabric, Azure AI and Power BI

**Current Release:** v0.3.0 – Silver Foundation

## High-Level Data Architecture

```mermaid
flowchart LR

A["Market Data Providers"]

B["Microsoft Fabric"]

C["Bronze Delta"]

D["Silver Delta"]

E["Gold Delta"]

F["Power BI"]

G["Future AI Services"]

A --> B
B --> C
C --> D
D --> E
E --> F
E --> G
```

## Development Architecture

```mermaid
flowchart LR

A["VS Code<br/>Python Development"]

B["Microsoft Fabric<br/>Workspace"]

C["GitHub<br/>dev"]

D["Pull Request"]

E["GitHub<br/>main"]

F["Version Tag"]

A --> C
B --> C
C --> D
D --> E
E --> F