# GameDrop // Video Game Deal Aggregator & Static Site Engine

An ultra-high-performance, database-driven video game discount aggregation platform. The project synchronizes live e-commerce discount pipelines via external APIs, structures records within a secure relational database engine, and compiles highly optimized static build artifacts served through an enterprise web server network architecture.

---

## 🎓 Academic Attribution & Project Context
* **Institution:** IES Puerto de la Cruz
* **Educational Program:** 1ºDAW (Formación Profesional de Grado Superior - Desarrollo de Aplicaciones Web)
* **Project Nature:** Challenges-Based Web Engineering Assignment (Static Site Generation Pipeline)
* **Virtualization Host Environment:** LinuxMint OS Virtual Machine running inside VirtualBox

---

## 🛠️ System Architecture & Workflow

The platform utilizes a structured **Static Site Generation (SSG)** paradigm to isolate intensive database processing and external API latency from end-user browsing experiences.

```
┌──────────────────┐       ┌─────────────────┐       ┌─────────────────────┐
│  CheapShark API  │ ───>  │   PostgreSQL    │ ───>  │ Static Site Builder │
│  (Real-time PC   │       │   Database DB   │       │   (build_site.py)   │
│   Deal Feeds)    │       │ (asc_videogames)│       └──────────┬──────────┘
└──────────────────┘       └─────────────────┘                  │
                                                                ▼
┌──────────────────┐       ┌─────────────────┐       ┌─────────────────────┐
│   End-User Web   │ <───  │ Apache Server   │ <───  │ Production Assets   │
│  Browsing View   │       │ (/var/www/html) │       │ (index.html/json)   │
└──────────────────┘       └─────────────────┘       └─────────────────────┘
```

1. **Ingestion Layer (`fetch_deals.py`):** Communicates with external endpoints, synchronizes active global digital merchant profiles, structures item listings, tracking identifiers, and price drops inside the operational data store.
2. **Persistence Layer (`db_context.py`):** Manages high-velocity connection resource pooling via context-managed cursors, maintaining complete transaction insulation across updates.
3. **Compilation Engine (`build_site.py`):** Relocation architecture that compiles active relational records into a highly compressed, cacheable JSON object array target and synchronizes structural assets into web directory configurations.
4. **Presentation Engine (`base.html` & `styles.css`):** An accelerated, highly responsive grid view running a lightweight DOM virtualization system to manage large catalog arrays with sub-millisecond execution speeds.

---

## 🗄️ Relational Database Schema (PostgreSQL)

The persistence layer is mapped out in PostgreSQL inside the designated host system. Execute the following SQL schema commands within the `asc_videogames_db` instance to allocate the target relational structures:

```sql
-- 1. Store Directory Lookups
CREATE TABLE Store (
    store_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_url VARCHAR(255) NOT NULL
);

-- 2. Game Metadata Catalogs
CREATE TABLE Game (
    game_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    background_image TEXT,
    rating NUMERIC(5,2) DEFAULT 0.00
);

-- 3. Dynamic Deal Mapping Contracts
CREATE TABLE Deal (
    deal_id VARCHAR(100) PRIMARY KEY,
    game_id INT REFERENCES Game(game_id) ON DELETE CASCADE,
    store_id INT REFERENCES Store(store_id) ON DELETE CASCADE,
    price NUMERIC(10,2) NOT NULL,
    retail_price NUMERIC(10,2) NOT NULL,
    savings NUMERIC(5,2) NOT NULL,
    purchase_url TEXT NOT NULL
);

-- Allocation Indexes for High-Velocity Query Performance Optimization
CREATE INDEX idx_deal_price ON Deal(price);
CREATE INDEX idx_game_title ON Game(title);
```

---

## 💻 Configuration and Backend Mechanics

System configurations are centralized within `config.py` to target specialized operational environments.

### 1. Environmental Variable Matrix (`config.py`)
```python
DB_PARAMS = {
    "host": "192.168.56.10",
    "database": "asc_videogames_db",
    "user": "postgres",
    "password": "@Suricat0s2o26",
    "port": 5432
}

CHEAPSHARK_BASE_URL = "[https://cheapshark.com/api/1.0](https://cheapshark.com/api/1.0)"
CHEAPSHARK_FILTERS = {
    "storeID": "1",          # Target Store Context (e.g., 1 = Steam)
    "upperPrice": "50",      # Max target price ceiling limit
    "lowerPrice": "0",
    "sortBy": "Savings",
    "pageSize": "60"         # Max number permitted of deal records to fetch
}

APACHE_DIR = "/var/www/html"
```

### 2. Manual System Execution Routine
The compilation and synchronization commands must be run manually through the shell environment inside your project deployment directories:

```bash
# Step 1: Execute external data ingestion to sync structural database states
python3 src/fetch_deals.py

# Step 2: Compile relational database states down into optimized production target assets
python3 src/build_site.py
```

---

## ⚡ High-Performance Client Architecture

The frontend layout avoids common rendering performance bottlenecks (such as scroll-linked layout thrashing, style recalculation jams, and visual layout shifts) by using a clean, hardware-accelerated static pipeline.

* **IntersectionObserver Structural Virtualization:** Evaluates layout viewport intercepts asynchronously. Cards moving outside the target visibility bounding frames (`rootMargin: "400px"`) receive a performance-saving `contain-visibility: hidden` rule inside CSS through a custom class toggle to ensure that the browser's paint engine avoids calculating invisible geometric surfaces.
* **Native Asynchronous Image Swapping:** Media images use an asynchronous encoding framework (`decoding="async"`) combined with data-attribute placeholder parameters, preventing rendering lockups when heavy asset rows move into view.
* **Asynchronous Chunk-Streaming Engine:** Renders records smoothly in precise arrays of 20 elements via user interaction triggers, avoiding intensive bulk DOM insertion operations.
* **Zero Jitter Compositor Mechanics:** Removed dynamic JavaScript scroll calculations entirely. Fixed layout elements run directly via GPU layer acceleration targets using the native browser compositing thread, avoiding all scroll latency or artificially introduced slowdowns.

---

## 📱 Responsive Layout Grid Architecture

The catalog layout changes grid column density natively via CSS media queries. Card spacing scales fluidly to maximize viewing densities while maintaining complete text readability and interactive click areas across all device resolutions:

| Display Target | Viewport Width Boundary | Grid Layout Density | Typography / Element Tweaks |
| :--- | :--- | :--- | :--- |
| **Enterprise Monitors** | Over `1200px` | **5 Columns Grid** | Standard 0.95rem Titles / 12px Card Padding |
| **Laptops / Monitors** | `901px` to `1200px` | **4 Columns Grid** | Compact 16px Row Container Gaps |
| **Tablet Form Factors** | `601px` to `900px` | **3 Columns Grid** | Header Padding Reductions, 14px Grid Gaps |
| **Compact Mobile Viewports** | `381px` to `600px` | **Dense 2 Columns Grid** | Compact 0.85rem Titles / 6px Badges / 10px Padding |
| **Ultra-Small Handsets** | Under `380px` | **Dense 2 Columns Grid** | Title scale-down protection (0.8rem) / 8px Gaps |

---

## 📊 Network Topology & Virtualization Map

Below is the complete end-to-end blueprint tracking data routing across internet entry ports, local network firewalls, down into VirtualBox NAT network switches, and terminating inside the isolated Virtual Machine container:

```
🌐 WAN ACCESS INTERNET (gamedrop.duckdns.org)
       │
       ▼ [Public External Gateway IP: 88.24.76.106]
┌────────────────────────────────────────────────────────┐
│               MOVISTAR ROUTER ENGINE                   │
│   Internal Gateway Address: 192.168.1.1                │
│   Network DHCP Scopes Pool: 192.168.1.101 - 199        │
│                                                        │
│   ── Port Mapping Forward Rule: ───────────────────    │
│   [Ext Port: 8443] ──> Forward To ──> [192.168.1.100:8443]
└──────────────────────────┬─────────────────────────────┘
                           │
      ┌────────────────────┴────────────────────┐
      ▼                                         ▼
┌──────────────────────────┐              ┌─────────────────────────────────────┐
│  STRONG WiFi Repeater    │              │         WINDOWS HOST MACHINE        │
│  IP: 192.168.1.2         │              │  MAC Addr mapped via Router Lease   │
│  (Moved outside Pool to  │              │  LAN Client Binding: 192.168.1.100  │
│   eliminate Conflicts)   │              │  Firewall Rule: Allow 8443 Inbound  │
└──────────────────────────┘              └──────────────────┬──────────────────┘
                                                             │
                                                             ▼
                                          ┌─────────────────────────────────────┐
                                          │     VIRTUALBOX HYPERVISOR SWITCH    │
                                          │  NAT Mapping: Host Interface Bound  │
                                          │                                     │
                                          │  ── Port Forwarding Map Rules: ──   │
                                          │  Host: 0.0.0.0:8443                 │
                                          │  Guest: 10.0.2.15:443               │
                                          └──────────────────┬──────────────────┘
                                                             │
                                                             ▼
                                          ┌─────────────────────────────────────┐
                                          │      GUEST OS: UBUNTU LINUXMINT     │
                                          │  Virtual Internal IP: 10.0.2.15     │
                                          │  Security Profile: UFW Active       │
                                          │  Web Engine: Apache (Port 443/SSL)  │
                                          └─────────────────────────────────────┘
```

The system network configurations map accurately across endpoints as documented below:
* **Router Gateway:** 192.168.1.1 (Fixed)
* **STRONG Repeater:** 192.168.1.2 (Static Mode)
* **Windows Host Workstation:** 192.168.1.100 (DHCP Reservation / Static Lease)
* **Ubuntu VM Guest (VirtualBox NAT Network Engine):** 10.0.2.15 (Internal Loopback Environment)
* **Dynamic Client Pools:** 192.168.1.101 to 192.168.1.199 (Standard Local Scopes)

---

## 🛠️ Troubleshooting & Network Configuration Matrix

### Issue 1: Dynamic IP Conflicts on Host Machine
* **Problem:** The Windows host workstation IP address shifted intermittently between `192.168.1.39` and `192.168.1.40`, completely breaking existing router port mapping definitions.
* **Root Cause:** A high-power **STRONG WiFi Repeater** hardware device was occupying conflicting ranges dynamically inside the default router DHCP scope pool (`192.168.1.33-199`), triggering rapid lease renegotiation loops.
* **Solution Implemented:**
  1. **DHCP Reservation (Static Lease Assignment):** Entered the primary router configuration page via `192.168.1.1` -> Navigate to *LAN / Static Lease* -> Explicitly bound the Windows host system MAC address directly to IP destination `192.168.1.100`.
  2. **DHCP Scope Modification:** Adjusted the router dynamic address allocation boundaries from `192.168.1.33-199` to `192.168.1.101-199`. This frees up IPs `192.168.1.2` through `192.168.1.100` for permanent static hardware mappings.
  3. **Repeater Relocation:** Reconfigured the STRONG Repeater admin interface to use static configuration mode bound cleanly at `192.168.1.2`, isolating it outside the dynamic allocation boundary pool.

### Issue 2: VirtualBox NAT Network Isolation Overrides
* **Problem:** The Apache web engine was locked within an isolated NAT sandbox context inside the Ubuntu Virtual Machine, making it unreachable to LAN devices and standard public requests.
* **Symptoms:**
  * `https://127.0.0.1:8443` -> ✅ Functional (Internal loopback testing successful)
  * `https://192.168.1.100:8443` -> ❌ Execution Failure (Host IP connection dropped)
  * `https://88.24.76.106:8443` -> ❌ Access Forbidden (External public request drop)
* **Solution Implemented:** Configured VirtualBox software pipeline forwarding parameters to bridge incoming external host requests through to the virtual guest appliance.
  * *Path:* VirtualBox Manager UI -> Select Target VM -> Settings -> Network -> Adapter 1 (NAT Mode) -> Port Forwarding Advanced Parameters Table.

| Rule Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Apache HTTPS** | TCP | `0.0.0.0` | `8443` | `10.0.2.15` | `443` |

*Key Insight:* Apache handles listening operations inside the guest container on standard port `443`, while the host hypervisor maps traffic visibility externally on port `8443` to avoid service collisions on the main interface environment.

### Issue 3: Windows Advanced Defender Firewall Dropping Port Traffic
* **Problem:** Even after applying VirtualBox configuration layers, the host Windows security policies rejected incoming port validation requests sent on port `8443`.
* **Solution Implemented:** Added global rule declarations through administrative PowerShell command execution blocks to permit secure traffic traversals:

```powershell
# Create persistent inbound hardware handling rules
New-NetFirewallRule -DisplayName "GameDrop Apache Server Inbound" -Direction Inbound -LocalPort 8443 -Protocol TCP -Action Allow

# Create corresponding outbound verification definitions
New-NetFirewallRule -DisplayName "GameDrop Apache Server Outbound" -Direction Outbound -LocalPort 8443 -Protocol TCP -Action Allow
```

* **Verification Profile Test:**
```powershell
# Verify binding state properties directly on the active listener port
Test-NetConnection -ComputerName localhost -Port 8443
```

### Issue 4: Outdated Router Port Assignment Maps
* **Problem:** The primary internet router's port map references pointed to historical, dead IP values because of initial DHCP leasing conflicts.
* **Solution Implemented:** 1. Access the edge gateway control system at `192.168.1.1` -> Access *NAT Routing Options / Port Mapping Matrix*.
  2. Deleted broken rules and initialized a clean record mapping rule named `Apache-HTTPS` pointing to destination `192.168.1.100`.

| Service / Mapping Name | External Port | Target Internal Destination IP | Private/Internal Port | Protocol Configuration |
| :--- | :--- | :--- | :--- | :--- |
| **Apache-HTTPS** | `8443` | `192.168.1.100` | `8443` | **TCP Only** |

### Issue 5: External Address Modification Controls & DuckDNS Integration
* **Problem:** Dynamic Public IP allocations from the carrier provider (Movistar) shift unpredictably, causing external endpoints to lose connectivity.
* **Solution Implemented:** Activated automated cloud mapping trackers using the DuckDNS system protocol.
  * *Target Dynamic Address:* `gamedrop.duckdns.org`
  * *Update Automation Execution Script:* Managed via file layout `/usr/local/bin/duckdns-update.sh` containing:

```bash
#!/bin/bash
# Query endpoint validation loop to keep records synchronized with DuckDNS
curl -s "[https://www.duckdns.org/update?domains=gamedrop&token=YOUR_SECRET_DUCKDNS_TOKEN&ip=](https://www.duckdns.org/update?domains=gamedrop&token=YOUR_SECRET_DUCKDNS_TOKEN&ip=)" >> /var/log/duckdns.log 2>&1
```

* *Cron Automation Schedule:* Installed inside system root cron tasks to trigger every 5 minutes:
```bash
# Append tracking task inside system crontab configurations via 'sudo crontab -e'
*/5 * * * * /bin/bash /usr/local/bin/duckdns-update.sh
```

* **Execution Verification Verification:**
```bash
# Run manual validation checklist evaluations directly from shell terminal windows
cat /var/log/duckdns.log
```

### Issue 6: Browser SSL Certificate Validation Alerts
* **Problem:** Local self-signed SSL configurations displayed strict warnings ("Connection Not Secure"), halting standard traffic.
* **Solution Implemented:** Issued an official certificate package from Let's Encrypt validation authorities via `certbot` modules:

```bash
# Execute automated multi-domain challenge validation verification parameters
sudo certbot --apache -d gamedrop.duckdns.org
```

### Issue 7: Browser HSTS Cache Jams
* **Problem:** After applying valid SSL validation structures, standard testing software windows continued to load cached self-signed certificate data due to strict HSTS internal rules.
* **Solution Implemented:**
  1. Entered the internal control utility inside Google Chrome at URL: `chrome://net-internals/#hsts`
  2. Scrolled down to the *Delete domain security policies* section input container.
  3. Submitted the targeted test route (`gamedrop.duckdns.org`) and restarted browser processing threads.

### Issue 8: Host Server Infrastructure Hardening Strategy
* **Solution Implemented:** Hardened the exposed Linux network interface through three coordinated layers:

```bash
# Layer 1: Establish Fail2Ban automated attack tracking definitions
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban --now

# Layer 2: Lock down target local input profiles using Uncomplicated Firewall (UFW)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 8443/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

* **Layer 3: Disable Apache Footprint Disclosures:** Edited `/etc/apache2/conf-enabled/security.conf` configuration lines to prevent signature disclosures to scanners:
```apache
ServerTokens Prod
ServerSignature Off
```

---

## 🎯 Production Access Matrix Reference

| Access Topology | Target Connection Endpoint Path | Operational Verification Status |
| :--- | :--- | :--- |
| **Local Host VM View** | `https://127.0.0.1:8443` | ✅ System Active / Verified |
| **Local Area Network (LAN)** | `https://192.168.1.100:8443` | ✅ System Active / Verified |
| **External Internet WAN (Direct IP)** | `https://88.24.76.106:8443` | ✅ System Active / Verified |
| **External Internet WAN (DNS Name)** | `https://gamedrop.duckdns.org:8443` | ✅ System Active / Verified |

---

## 📄 License & Terms
This repository is open-source software distributed under the terms of the **GNU General Public License Version 3, 29 June 2007**. See the included [`LICENSE.txt`](LICENSE) file inside the root repository structure for complete authorization details.
