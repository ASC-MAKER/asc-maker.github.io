# CHALLENGES-BASED WEB PROJECT | STATIC SITE GENERATION 
This project has been created to improve our web development skills.

## STEPS: DAY 1
### Products To Sell / Theme
- **VIDEOGAMES**

### Product's APIs ([RAWG](https://rawg.io) & [CheapShark](https://cheapshark.com))
We have selected a **dual-API strategy** to meet our project requirements:
- **RAWG API:** Used as the primary source for **metadata**. It provides access to over 500,000+ games, including high-quality **images (backgrounds and screenshots)**, detailed descriptions, genres, and platform compatibility.
- **CheapShark API:** Used specifically for **real-time pricing and deals**. Since RAWG does not provide live prices, CheapShark fills this gap by offering updated costs and purchase links for PC games across multiple stores.

### Doc Research

#### 1. API Fetching (Scraping) with Python
API fetching consists of making direct HTTP requests to server endpoints to obtain structured data.

- **Main Libraries:**
  - `requests`: The standard tool for sending `GET` and `POST` requests.
  - `json`: Native library to process and save the data.
        
- **Workflow:**
  - **Identify Endpoints:** Get the **API Key** by registering at [RAWG](https://rawg.io). CheapShark does not require a key.
  - **Send Request:** Use `requests.get(url)` to fetch the response from both APIs.
  - **Process JSON:** Convert the text response into a Python dictionary using `response.json()`.
  - **Data Merging:** Cross-reference the results (usually by matching the game title) to combine RAWG images with CheapShark prices into a single object.

#### 2. JSON Storage
To persist the collected data, we use the `json` module to write files to the local disk. This is essential for **Static Site Generation (SSG)**, as the site will be built using these pre-fetched files.

- **Method `json.dump()`:** Allows writing a Python object (dictionary or list) directly into a `.json` file.
- **Organization:** Store games in an array format to easily iterate through them during the site build process.

#### 3. Secure Server Implementation (HTTPS)
To ensure a secure server, the connection must be wrapped in an SSL/TLS encryption layer.

- **Requirements:** A certificate (`cert.pem`) and a private key (`key.pem`) are needed.
- **Development:** Self-signed certificates can be generated with **OpenSSL**. In Python, this is implemented using `http.server` combined with the `ssl` module to wrap the socket.

#### 4. Two-Factor Authentication (2FA)
2FA adds a security layer where the user provides something they know (password) and something they have (a code on their mobile device).

- **TOTP (Time-based One-Time Password):** The most common method (compatible with Google Authenticator).
- **Recommended Library:** `PyOTP`.
  - **Step 1:** Generate a **unique secret key** for the user.
  - **Step 2:** Display a **QR Code** that the user scans with their authenticator app.
  - **Step 3:** Verify the **6-digit code** entered by the user during login.

### VMs Technical Specifications

| Configuración | VM Servidor Web (SSG) | VM Base de Datos (PostgreSQL) |
| :------------ | :-------------------- | :---------------------------- |
| **Sistema Operativo** | Linux Mint (22.3) Xfce | Linux Mint (22.3) Xfce |
| **Versión (VBox)** | Ubuntu (64-bit)| Ubuntu (64-bit) |
| **Procesador (vCPU)** | 4 Cores | 4 Cores |
| **Memoria RAM** | 4 GB | 8 GB |
| **Disco Virtual** | 25 GB (Dynamic VDI) | 50 GB (Dynamic VDI) |
| **Tipo de Red** | NAT (Internet) | Internal Net (Host-only) |
| **Usuario Sistema** | `project_web` | `project_db` |
| **Propósito de Red** | External Access/Internet | Data isolation and security |


### Architecture Diagram
[![Diagram](https://mermaid.ink/img/pako:eNqFU4Fu2jAQ_RXLVaVWgpAEAsSaKhUoXaUypaMr05KpMuQAq8FGjlnLqv77zkla0krbEiVxTu_ePb87P9OFSoEyutJ8uya3o0QSvPLdvAx8Vrm5n-5zAxsSR-t9LhY8I9GQNMlMyFQ95i0L-Vmm2WugMQg6rr6MZApT1ghifbfv1pDT6ef7YSZAmvgW9EZInjEbJJHShvh-BQWZJvKDrLvJ_QzmJL6bEPudgv4FGjVNhDTk-3h4USvzZSXkU1y8W-dbvlhDhf80162zotY7WefbbYwPuVYrsSAtVHRJhkoa1FlDjWdWQfxtPCNjoeGRZ9m_9Y4GhdwIjVhpmN5c_0VuBcjjGvJCono46A06bb9upFGaryA-uRtdkZHIHxgJ3MvB6Xu5o8F_1B4f233Ck8BXXoaqJpJmkyS0KD1W-pHrVMhVIce2FPtKTm6H0WlCEXhWGl7mH1pMmg5SfIWNMkAmXKLeDYYPe_J9THcwvXS2zC-oyurXdozIzQ70vqqDTSpRtlsFxnoVaWXUQmUF81XEiBf6jtftO57reEUeLvyKouhLSfLqe8k04oajrxr4poJWJtfMusiNyFTlVG72Gbw7LkuRZexoGdi7kRutHoAdtdvtat1Meb7mWvM9dosEdZZquksC8JAA3ghcL-iF8w9onK0K3F8GEL6BfeilbZ828HSLlDKjd9CgGzxr3P7SZ0uTULPGViSU4TKFJd9lJqGJfMG0LZc_lNq8Zmq1W60pW_Isx7_dNuUGRoLjiB8gOE-gh2onDWV93KzloOyZPlHmdUIn9MNuvxc06J6yXtfphUE36JSxlwb9XRRznV7geV4n8D036Iau7738AYS1ar0?type=png)](https://mermaid.live/edit#pako:eNqFU4Fu2jAQ_RXLVaVWgpAEAsSaKhUoXaUypaMr05KpMuQAq8FGjlnLqv77zkla0krbEiVxTu_ePb87P9OFSoEyutJ8uya3o0QSvPLdvAx8Vrm5n-5zAxsSR-t9LhY8I9GQNMlMyFQ95i0L-Vmm2WugMQg6rr6MZApT1ghifbfv1pDT6ef7YSZAmvgW9EZInjEbJJHShvh-BQWZJvKDrLvJ_QzmJL6bEPudgv4FGjVNhDTk-3h4USvzZSXkU1y8W-dbvlhDhf80162zotY7WefbbYwPuVYrsSAtVHRJhkoa1FlDjWdWQfxtPCNjoeGRZ9m_9Y4GhdwIjVhpmN5c_0VuBcjjGvJCono46A06bb9upFGaryA-uRtdkZHIHxgJ3MvB6Xu5o8F_1B4f233Ck8BXXoaqJpJmkyS0KD1W-pHrVMhVIce2FPtKTm6H0WlCEXhWGl7mH1pMmg5SfIWNMkAmXKLeDYYPe_J9THcwvXS2zC-oyurXdozIzQ70vqqDTSpRtlsFxnoVaWXUQmUF81XEiBf6jtftO57reEUeLvyKouhLSfLqe8k04oajrxr4poJWJtfMusiNyFTlVG72Gbw7LkuRZexoGdi7kRutHoAdtdvtat1Meb7mWvM9dosEdZZquksC8JAA3ghcL-iF8w9onK0K3F8GEL6BfeilbZ828HSLlDKjd9CgGzxr3P7SZ0uTULPGViSU4TKFJd9lJqGJfMG0LZc_lNq8Zmq1W60pW_Isx7_dNuUGRoLjiB8gOE-gh2onDWV93KzloOyZPlHmdUIn9MNuvxc06J6yXtfphUE36JSxlwb9XRRznV7geV4n8D036Iau7738AYS1ar0)

