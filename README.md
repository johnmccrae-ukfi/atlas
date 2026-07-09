# atlas
Enterprise AI Intelligence Platform powered by Microsoft Fabric, Azure AI and Power BI

**Current Release:** v0.8.0 – AI Trading Intelligence Foundation

## High-Level Data Architecture

```mermaid
flowchart LR

A["Market Data Provider APIs"]

B["Microsoft Fabric Lakehouse"]

C["Market Data Legacy Files"]

D["Python/Visual Studio Code"]

E["Bronze Layer"]

F["Silver Layer"]

G["Gold Analytics"]

H["AI Intelligence Layer"]

I["Direct Lake Semantic Model"]

J["PowerBI Reports"]

K["Future AI Services"]

A --> B
C --> D
D --> B
B --> E
E --> F
F --> G
G --> H
H --> I
H --> K
I --> J
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