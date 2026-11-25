# HH Kitchen Restock — Architecture

Reference only. The SKILL.md files are the playbooks; this doc is
the map, for when the shape of the suite needs checking.

## Flow

```mermaid
flowchart LR
    cron["Sun 2pm PT<br/>weekly cron"] --> gather["GATHER<br/>ask list only"]
    gather --> reply["Peter replies<br/>what's needed"]
    reply --> build["BUILD<br/>cart, no submit"]
    build --> submit["SUBMIT<br/>confirm first"]
    submit --> reconcile["RECONCILE<br/>after delivery"]
```

## Layers

Skills hold mechanism only. Config is the only state. Connectors
are external use, reached only through their own docs.

```mermaid
flowchart TB
    subgraph skills["SKILLS — muse-skills repo"]
        model["hh-kitchen-restock<br/>model + bin/restock CLI"]
        gather["gather"]
        build["build"]
        submit["submit"]
        reconcile["reconcile"]
        model -.-> gather
        model -.-> build
        model -.-> submit
        model -.-> reconcile
    end
    subgraph config["CONFIG — local, never in repo"]
        localcfg[("restock.json<br/>store · platform · the line<br/>backstock · specials · spec cards · orders")]
        repocfg[("repo config.json<br/>pointers only")]
    end
    subgraph connectors["CONNECTORS — external use"]
        tasks["Google Tasks<br/>Inventory list"]
        insta["Ordering platform<br/>search · cart · checkout"]
    end
    gather -->|"reads"| localcfg
    build -->|"reads"| localcfg
    submit -->|"log-order: writes"| localcfg
    reconcile -->|"learn: writes"| localcfg
    skills -->|"reads"| repocfg
    gather -->|"reads inventory"| tasks
    reconcile -->|"complete: writes"| tasks
    build -->|"builds cart"| insta
    submit -->|"checkout"| insta
    reconcile -->|"reads order record"| insta
```

- **Config reads:** gather and build read `restock.json`; every
  skill reads the repo `config.json` pointers.
- **Config writes:** only submit (`log-order`) and reconcile
  (`learn`) write `restock.json`.
- **Connector writes:** reconcile is the only skill that writes
  to Google Tasks (`complete`, delivered items only). The
  ordering platform is written by build (cart) and submit
  (checkout), and read back by reconcile (the order record).
