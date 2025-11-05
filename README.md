# Nostr Wallet Connect (NIP-47) Implementation

This is a minimal implementation of NIP-47 for connecting LND to external wallets via Nostr.

## Setup

1. Install dependencies: `source venv/bin/activate && pip install -r requirements.txt`
2. Configure LND RPC path, macaroon path, cert path, and relay URL in `main.py`.
3. Run: `source venv/bin/activate && python main.py`

The code generates and prints a NWC URI. Share this URI with the external wallet app to connect and send NIP-47 requests.

Note: For LND operations like payments, you need an admin macaroon with write permissions.

## Features

- Generates NWC URI for external wallet connection.
- Handles NIP-47 requests: pay_invoice, get_balance, make_invoice, lookup_invoice, list_transactions, get_info.
<<<<<<< HEAD
- Connects to LND for Lightning operations.
=======
- Connects to LND for Lightning operations.
>>>>>>> d024489 (feat: build script that connect LND node with external wallets following NIP-47 protocol)
