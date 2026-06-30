# atlas
Enterprise AI Intelligence Platform powered by Microsoft Fabric, Azure AI and Power BI

## High-Level Architecture

```mermaid
flowchart LR
    A["Market Data APIs"] --> B["Fabric Pipelines"]
    B --> C["Bronze Lakehouse"]
    C --> D["Silver Lakehouse"]
    D --> E["Gold Warehouse"]
    E --> F["Trading Signal Engine"]
    F --> G["Power BI Dashboard"]
    E --> H["Future AI Intelligence Layer"]
    H --> G
```