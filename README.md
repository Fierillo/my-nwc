# Nostr Wallet Connect (NIP-47) Implementation

This is a minimal implementation of NIP-47 for connecting LND to external wallets via Nostr. Assumes Linux environment.

## Prerequisites

- **Python 3.11+**: Check with `python3 --version`. If not installed, run `sudo apt update && sudo apt install python3 python3-pip python3-venv`.
- **LND (Lightning Network Daemon)**: Running and configured. Obtain:
  - RPC path: Usually `/home/your_user/.lightning/bitcoin/lightning-rpc` (adjust for network: bitcoin, testnet, etc.).
  - Admin macaroon: Path to `admin.macaroon` (e.g., `/home/your_user/.lightning/bitcoin/admin.macaroon`).
  - TLS cert: Path to `tls.cert` (e.g., `/home/your_user/.lightning/bitcoin/tls.cert`).
- **Git**: For cloning if needed, but code is local.

## Installation

1. **Clone or navigate to the project directory**:
   cd /path/to/your/project/my-nwc

2. **Create a virtual environment** (isolates dependencies):
   python3 -m venv venv

3. **Activate the virtual environment**:
   - On Linux/Mac: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
   - `source` loads the environment variables for the venv. Deactivate with `deactivate`.

4. **Install dependencies**:
   pip install -r requirements.txt

## Configuration

Edit `main.py` with your paths:

- `lnd_rpc_path`: Path to LND RPC socket.
- `macaroon_path`: Path to admin.macaroon (required for payments).
- `cert_path`: Path to tls.cert (if using TLS).
- `relay_url`: Nostr relay, e.g., 'wss://relay.nostr.band'.

Example:
lnd_rpc_path = '/home/user/.lightning/bitcoin/lightning-rpc'
macaroon_path = '/home/user/.lightning/bitcoin/admin.macaroon'
cert_path = '/home/user/.lightning/bitcoin/tls.cert'

## Usage

1. **Activate venv**: `source venv/bin/activate`
2. **Run the server**: `python main.py`
3. The code prints a NWC URI. Copy and share with the external wallet app.
4. The server listens for NIP-47 requests and processes them via LND.

## Features

- Generates NWC URI for external wallet connection.
- Handles NIP-47 requests: pay_invoice, get_balance, make_invoice, lookup_invoice, list_transactions, get_info.
- Connects to LND for Lightning operations.

## Notes

- Admin macaroon is required for write operations like payments.
- If LND is remote, use TCP: `lnd_rpc_path = 'tcp://host:port'`.
- For issues, check LND logs and ensure paths are correct.
- Code follows minimal, clean practices with no unnecessary complexity.
