# Multi-Platform Anonymous Routing Engine
An asynchronous session-based chat routing agent designed for real-time anonymous pairing and concurrent semi-anonymous message forwarding. Engineered with a strict separation of concerns, utilizing an in-memory key-value cache for high-throughput state tracking and an optimized relational storage engine for persistence.

The core communication layer is abstracted to support unified polling across multiple instant messaging networks, with active production modules optimized for the Telegram and Bale Messenger bot APIs.

---

## Architecture Overview

The system architecture decouples ephemeral network sessions from data persistence to maximize I/O throughput and eliminate locking bottlenecks during high-concurrency event loops.

[Network Webhooks / Polling]
│
▼
┌────────────────────────────────────────┐
│   Python 3.14 Async Event Loop         │
│   (python-telegram-bot v20.x Core)     │
└─────┬────────────────────────────┬─────┘
│                            │
│ (Fast In-Memory State)     │ (TCP Gateway Link)
▼                            ▼
┌────────────────────────┐   ┌────────────────────────┐
│ Redis Cache Instance   │   │ MariaDB SQL Engine     │
│ - User State Machine   │   │ - User Registries      │
│ - Dynamic Match Queues │   │ - Historical Archives  │
│ - Active Chat Pointers │   │ - Health Verification  │
└────────────────────────┘   └────────────────────────┘

### Key Technical Implementations
* Async I/O Core: Powered natively by Python's `asyncio` loop to handle non-blocking database and network operations.
* Redis State Machine: Manages low-latency lifecycle states (`searching`, `anon-chat`, `semi-chat`, `idle`) and active dynamic routing indices.
* Containerized Health Checking: Implements strict upstream dependency verification to block service polling until database engine subsystems are fully initialized.
* Network Gateway Layer: Configured with explicit Docker bridge gateway mappings (`172.17.0.1`) to isolate and bypass kernel-level local DNS resolution issues across disparate GNU/Linux firewalls (Fedora/Ubuntu systems).

---

## Technical Specifications & Features

### 1. Anonymous Matchmaking Framework
* Queue Architecture: Atomic Redis list operations handle real-time FIFO user matchmaking.
* Session Lifecycle: Automated flushing mechanisms wipe transient states upon termination to prevent deadlock states or memory leaks.
* Routing Commands: Decoupled logic handlers catch and execute mid-session instructions (`/next`, `/end`) seamlessly.

### 2. Multi-Session Semi-Anonymous Routing
* Tokenized Deep-Linking: Generates unique cryptographically-safe link entry points to map incoming hidden identities to a static receiver host.
* Concurrent Context Switching: Supports multiple active sessions per user. A dynamic pointer tracked via Redis isolates incoming packets and routes them dynamically based on the current context array selected by the user.

### 3. Database & Storage Architecture
* Cache Engine (Redis): Handles dynamic matchmaking queues, transient peer mappings, and structural session cache metadata.
* Storage Engine (MariaDB/MySQL): Maintains long-term normalization tables for core user registries, identity configurations, and historical connection logging.

---

## Deployment & Orchestration

The infrastructure is entirely managed via containerized execution vectors inside isolated Docker networks.

### 1. Configuration Environment (`.env`)
Ensure the following variable array is defined in the root context directory before deployment:

```env
BOT_TOKEN=your_network_api_token
DB_NAME=secret_chat_db
DB_USER=bot_admin
DB_PASSWORD=your_secure_password
DB_ROOT_PASSWORD=your_root_password
DB_HOST=172.17.0.1
```

2. Orchestration Commands

Initialize multi-container builds and execute in isolated detached modes:
Bash
``` sudo docker compose up -d --build ```

Inspect orchestration status, network sockets, and container subsystem health:
Bash
``` sudo docker compose ps ```

Monitor live logging outputs from the core runtime application container:
Bash
``` sudo docker compose logs -f bot ```

Directory Taxonomy
Plaintext

├── db/                 # Initialization schemas, pooling engines, and async CRUD models
├── handlers/           # Message routing matrices, state triggers, and session controllers
├── keyboards/          # Dynamic layout generation for reply and inline UI components
├── main.py             # Event loop bootstrap and network polling lifecycle supervisor
├── Dockerfile          # Multi-stage optimized runtime environment layout
└── docker-compose.yml  # Microservice stack orchestrator (Bot + Redis + MariaDB)
