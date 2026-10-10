# Presago

![CI](https://github.com/Presago-Labs/presago/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Stellar](https://img.shields.io/badge/Stellar-Soroban-7D00FF?logo=stellar&logoColor=white)

Presago is a prediction-market project built with Soroban smart contracts on Stellar and a lightweight static HTML frontend.

The frontend uses plain HTML, CSS, and JavaScript. It does not require Node.js, Next.js, React, npm, or a build step.

## Table of Contents

- [How it uses Stellar](#how-it-uses-stellar)
- [Current status](#current-status)
- [Repository layout](#repository-layout)
- [Scripts](#scripts)
- [Prerequisites](#prerequisites)
- [Run the static frontend](#run-the-static-frontend)
- [Frontend files](#frontend-files)
- [Connect a wallet](#connect-a-wallet)
- [Smart contracts](#smart-contracts)
- [Testnet deployment](#testnet-deployment)
- [Security](#security)
- [Environment variables](#environment-variables)

## How it uses Stellar

Presago runs prediction markets on **Stellar** with **Soroban** smart contracts: pools, positions, referrals, and leaderboard rewards are contract state, and the static frontend connects to Freighter and submits `place_bet` invocations to Stellar Testnet. See the [Testnet contracts](#testnet-contracts) and [Mainnet contracts](#mainnet-contracts) sections for separate network-specific contract IDs, and the [contract call guide](docs/CONTRACT_CALLS.md#mainnet-deployed-contracts) for mainnet examples.

### Mainnet contracts

These contract IDs are documented for **Stellar Mainnet**. They correspond to the [Mainnet deployed contracts table in the contract call guide](docs/CONTRACT_CALLS.md#mainnet-deployed-contracts); they are **not** Testnet contract IDs.

| Contract | Mainnet contract ID |
| --- | --- |
| Prediction Market | `CDGNPRYTFDXJLWZE4YDKZXW4IEN2RLPSE4N7VM5HJ7NLPL2QC45GIXI5` |
| PULSE Token | `CAYL4TKNRMXAX5ZLQGFEZ6XOC2QHTCTN5QC2SB5BEEHLVO6SDU2UBLRH` |
| Referral Registry | `CAGJVX6EXMCKKWDJCQFIEJ34CZTHZOGLWJM6KQTGDEXEO723CJZ5773H` |
| Leaderboard | `CCWWOQSDSO3XXLCMA6A2HYRUFYVNUJZ2HPAMFQSPOB4JWYIBY2HWVTOB` |

## Current status

The Soroban contracts are deployed and initialized on Stellar Testnet. The static frontend displays live public Stellar network data and XLM pricing, connects to Freighter, and submits positions for verified Testnet market #3 directly to the deployed prediction-market contract. The other market cards remain clearly labeled demonstrations.

### Testnet contracts

These IDs are for **Stellar Testnet** only. They differ from the [Mainnet contracts](#mainnet-contracts) above; use the network-matched IDs and configuration when following the [contract call guide](docs/CONTRACT_CALLS.md#verification-checklist).

| Contract | Testnet address |
| --- | --- |
| Prediction Market | `CAPCAPWPGPOCENAJFYYIE22WYNFEDVZ3CT73M5MAKILFMBQ5TN2MIS6T` |
| PRESAGO Token | `CBYUQUXPGWUQRV7STCV3YPVLWNTFJHKLEAG7LVAOK7H4FIFJGZW5P476` |
| Referral Registry | `CCKVUVYXR6FBB4VFYGDF3IDDUVBRJGKPDDRABTZYKI2LKAJNVLF3TTQ2` |
| Leaderboard | `CCMNYMUI4XMDBTTMM7E6KNQFF3OVKS3Q2ERJ4EVQGCLW4VQCGUGG2AQM` |

Testnet deployer: `GC5D4ENQ3U3Q23L5RUG2GGIDFFVKOVJ6GUFJRTNIQ6SRP5J7RMECKSL7`

The deployment output is stored locally in the ignored `deploy-output.json` file. Contract activity can be inspected with [Stellar Expert Testnet](https://stellar.expert/explorer/testnet).

## Repository layout

- `contracts/` — Rust/Soroban contracts for markets, rewards, referrals, and leaderboards.
- `frontend/` — static HTML, CSS, and JavaScript website.
- `scripts/` — testnet/mainnet deployment and smoke-test scripts.
- The obsolete `scripts/update-accent-names.ps1` utility was retired because `frontend/src` does not exist.
- `docs/` — contract invocation examples and technical documentation.

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/deploy-testnet.sh` | Deploys and configures all contracts on Stellar Testnet. |
| `scripts/deploy-mainnet.sh` | Deploys the contracts to mainnet. |
| `scripts/create-mainnet-markets.sh` | Seeds the initial mainnet markets after deployment. |
| `scripts/smoke-test.sh` | Runs the end-to-end contract workflow on Testnet. |
| `scripts/upgrade-gas-reduction.sh` | Upgrades contracts in place with the gas-reduction build. |
| `scripts/validate-frontend.mjs` | Validates the static frontend assets. |

The former `scripts/update-accent-names.ps1` script has been retired and deleted. It recursed over the non-existent `frontend/src` directory and only ever wrote `.bak` files; the frontend theme tokens are `--green`, `--green-dark`, and `--red`, so its `accent-green` → `accent-mint` rename does not apply to this codebase.

## Prerequisites

| Tool | Notes |
| --- | --- |
| **Node.js 22** | to run the frontend validation scripts (`.nvmrc`) |
| **Python 3** | to serve the static frontend |
| **Node.js 22** | for frontend validation scripts (`.nvmrc`) |
| **Freighter** | browser wallet on Stellar Testnet |
| **Rust + Stellar CLI** | only for the contracts workspace |

## Run the static frontend

Opening `frontend/index.html` directly works for most UI features. A local HTTP server is recommended because browsers may restrict API requests from `file://` pages.

Using Python:

```bash
cd frontend
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

You can also use the VS Code Live Server extension or deploy the contents of `frontend/` to any static host.

## Frontend files

- `frontend/index.html` — page structure and inline SVG icon library.
- `frontend/markets.html` — searchable and filterable market catalog.
- `frontend/leaderboard.html` — community ranking page.
- `frontend/styles.css` — core theme and responsive layout.
- `frontend/product.css` — trading workspace, dashboard, FAQ, and expanded product sections.
- `frontend/pages.css` — shared styling for dedicated application pages.
- `frontend/script.js` — live data, market filters, Testnet order flow, simulations, and dashboard interactions.
- `frontend/soroban.js` — Soroban simulation, signing, submission, confirmation polling, and contract errors.
- `frontend/pages.js` — market catalog and leaderboard rendering.
- `frontend/wallet.js` — Freighter connection, testnet validation, balance display, and Friendbot funding.

## Connect a wallet

1. Install the [Freighter browser extension](https://www.freighter.app/).
2. Open Freighter and switch its network to **Testnet**.
3. Serve the frontend over HTTP and select **Connect wallet**.
4. Approve access in Freighter.
5. If the testnet account is empty, use the **Fund** action to request free test XLM from Friendbot.

The wallet integration uses the official `@stellar/freighter-api` package as a pinned browser module. The site never receives or stores the wallet secret key. Freighter asks the user for approval and exposes only the selected public address.

### Place a Testnet position

1. Connect a funded Freighter account on Testnet.
2. Select the market labeled **Testnet #3**.
3. Choose YES or NO and enter at least 1 test XLM.
4. Review and approve the exact contract transaction in Freighter.
5. Wait for confirmation, then open the transaction from the dashboard in Stellar Expert.

The browser loads the source account, builds a `place_bet` invocation, simulates it through Stellar RPC, asks Freighter to sign the prepared XDR, submits it to Testnet, and polls until the ledger confirms success. A failed or cancelled wallet request is never displayed as a completed position.

The page retrieves:

- Stellar ledger information from public Horizon APIs.
- XLM/USD market information from CoinGecko.

If a public API is unavailable, the interface displays an unavailable state instead of fabricated live values.

## Smart contracts

The Soroban workspace contains four contracts:

- `prediction_market` — market creation, YES/NO bets, resolution, claims, cancellations, refunds, and fees.
- `PRESAGO_token` — reward token and authorized minters.
- `referral_registry` — user registration, referrals, and bonuses.
- `leaderboard` — points, win/loss statistics, rankings, and token rewards.

### Contract tests

Install Rust and Stellar CLI, then run:

```bash
cd contracts
cargo test --workspace
```

The current contract suite contains 89 passing tests.

## Testnet deployment

The deployment script uses the ignored `.deploy.env` file and free Friendbot test XLM:

```bash
bash scripts/deploy-testnet.sh
```

The script:

1. Builds optimized WASM artifacts.
2. Funds the deployer on testnet.
3. Deploys all four contracts.
4. Initializes and connects the contracts.
5. Configures token-minter permissions.
6. Writes the public deployment details to `deploy-output.json`.

Run the end-to-end contract workflow with:

```bash
bash scripts/smoke-test.sh
```

The smoke test creates temporary Friendbot-funded users and checks registration, betting, cancellation, refunds, resolution, claims, token rewards, fees, and leaderboard data.

## Scripts Reference

The `scripts/` directory contains automated entry points for deploying, provisioning, testing, and maintaining Presago on testnet and mainnet:

| Path | Purpose | Required Env / Credentials | Confirmation Prompt | Prerequisites & Notes |
| --- | --- | --- | --- | --- |
| `scripts/deploy-testnet.sh` | Deploys token, market, leaderboard, and referral contracts to Stellar Testnet; initializes bindings and minter permissions. | `.deploy.env` (optional; falls back to temporary Friendbot keys) | None | Outputs public contract IDs to `deploy-output.json`. |
| `scripts/deploy-mainnet.sh` | Deploys the four Presago contracts to Stellar Mainnet with verification and storage TTL initialization. | `DEPLOYER_SECRET`, `SPONSOR_SECRET`, `RESOLVER_PUBLIC_KEY` in `.deploy.env` (min. balance 50 XLM) | `deploy mainnet` (`Type 'deploy mainnet' to confirm`) | Production mainnet release script. Writes outputs to `deploy-output-mainnet.json`. |
| `scripts/create-mainnet-markets.sh` | Seeds initial prediction markets on Stellar Mainnet from `mainnet-markets.json`. | Admin keystore or `DEPLOYER_SECRET`, `MARKET_ID` from deployment output | `create` (`Review the questions above. Type 'create' to proceed:`) | Must be run after `deploy-mainnet.sh`. |
| `scripts/mainnet-markets.json` | JSON configuration seed containing initial questions, resolver accounts, and close dates for mainnet markets. | N/A (Static JSON data) | None | Consumed by `scripts/create-mainnet-markets.sh`. |
| `scripts/smoke-test.sh` | End-to-end integration smoke test exercising user creation, betting, cancellation, refunds, resolution, claims, and fees. | Friendbot access on Testnet | None | **Prerequisite:** Requires `deploy-output.json` in repository root (run `scripts/deploy-testnet.sh` first). |
| `scripts/upgrade-gas-reduction.sh` | Upgrades installed contract WASM bytecode with gas-reduction optimizations across testnet or mainnet. | Contract IDs (`MARKET_ID`, `TOKEN_ID`, etc.) and admin secret key | None | Verifies installed WASM hashes before updating. |
| `scripts/validate-frontend.mjs` | Node.js verification script checking vendor asset SRI hashes and syntax validity for static frontend distribution. | Node.js runtime (`node >= 18`) | None | Runs locally or in static frontend CI workflow. |
| `scripts/update-accent-names.ps1` | Retired PowerShell script intended to rewrite `accent-green` to `accent-mint` in legacy component layouts. | PowerShell runtime | None | **Retired:** Retained for archival reference; targets obsolete directories and is no longer executed. |

## Security

- Never commit `.deploy.env`, secret keys, seed phrases, or wallet exports.
- Contract IDs and public account addresses are safe to publish.
- Wallet connection, balance lookup, and positions on market #3 are real Testnet operations. All other market cards remain simulations and are labeled accordingly.

## Environment variables

Copy `.env.example` to `.env` and fill in your values (see the file for inline docs). Key groups:

| Variable group | Key variables |
| --- | --- |
| Deployment | `DEPLOYER_SECRET`, `SPONSOR_SECRET`, `RESOLVER_PUBLIC_KEY` (in `.deploy.env`, never committed) |

## License

This project is licensed under the MIT License.
