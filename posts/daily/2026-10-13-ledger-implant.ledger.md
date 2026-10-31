# Fact ledger — Ledger hardware wallets with hidden implant, sold via SE-Asian reseller CryptoBilis — 2026-10-13, Asia/Vientiane

Mode: deep (single story). Style: hacker_circuit. Window 2026-10-09 → 2026-10-13. Series: hacker stories 1/3 (next: Midnight Mimosa Android malware; French supermarket fridge attack).

## 5W1H
- WHO: Ledger (French hardware-wallet maker); CryptoBilis (reseller, claims to be authorised Ledger reseller in Malaysia; listed for Indonesia, Malaysia, Philippines); Mark Karpelès (ex-Mt. Gox CEO); on-chain analysts Specter, Bitquery, Yfarmx, Arkham; SEAL 911; CZ
- WHAT: Wallets of buyers who bought via CryptoBilis drained; Ledger confirmed an unauthorised hardware implant in one affected user's device
- WHEN: Drains reported 2026-10-09; implant confirmed 2026-10-10
- WHERE: Southeast Asia (Malaysia-based reseller)
- WHY: Supply-chain tampering — device modified before reaching the user (mechanism not confirmed by Ledger)
- HOW (claimed): Karpelès: hidden board + LTE/eSIM/antenna behind screen padding, wired to display bus, reads 24-word recovery phrase during setup and sends it over cellular

## Facts
| # | Fact | Figure | As of | Confidence | Sources |
|---|---|---|---|---|---|
| 1 | Ledger investigating losses among users who bought from CryptoBilis | — | 2026-10-09 | ຢືນຢັນແລ້ວ | [1][2][3][4] |
| 2 | Ledger told CryptoBilis to pause all sales and shipments | — | 2026-10-09 | ຢືນຢັນແລ້ວ | [1][2][3][4] |
| 3 | Bought from CryptoBilis in last 90 days → do not initialise; already set up → move assets to new signer with new seed | 90 days | 2026-10-09 | ຢືນຢັນແລ້ວ (Ledger statement) | [1][2][4] |
| 4 | Ledger: "one of the impacted users' devices contained an unauthorized hardware implant" | 1 device | 2026-10-10 | ຢືນຢັນແລ້ວ (Ledger statement, via 2 outlets) | [4][6] |
| 5 | Ledger: no indication its own infrastructure/systems/services compromised | — | 2026-10-10 | ຢືນຢັນແລ້ວ | [2][4] |
| 6 | Ledger working with authorities; thanked SEAL 911 | — | 2026-10-10 | ລາຍງານ | [4] |
| 7 | CryptoBilis ceased hardware-wallet sales until investigation ends | — | 2026-10-10 | ລາຍງານ | [4] |
| 8 | Loss estimates: $71.5M (Arkham), $72–86M+ (Specter), ~$92.9M / 311 wallets (Bitquery), ~$93.4M / 471 addresses (Yfarmx) | $71.5M–$93.4M | 2026-10-09/10 | ການປະເມີນ — Ledger not confirmed → body only, with range + caveat | [1][2][3][4][5] |
| 9 | Karpelès implant description (LTE, eSIM, antenna, SPI/display, ~2×2 mm "spy SIM") | — | 2026-10-09 | ຢືນຢັນບໍ່ໄດ້ — attributed claim, not linked to CryptoBilis by Ledger | [3][4][5] |
| 10 | Ledger has not accused CryptoBilis of tampering; third party in supply chain possible | — | 2026-10-09 | ລາຍງານ | [2] |
| 11 | Ledger never asks for the 24-word recovery phrase | — | 2026-10-10 | ຢືນຢັນແລ້ວ (standing Ledger policy) | [4] |
| 12 | Phishing / fake ads / fake apps target panicked users migrating funds | — | 2026-10-09 | ລາຍງານ (Taylor Monahan) | [1] |
| 13 | CZ: possible supply-chain attack involving a single vendor | — | 2026-10-10 | ລາຍງານ | [5] |
| 14 | Questions raised about other wallet brands (Trezor, Tangem) sold by same reseller | — | 2026-10-09 | ລາຍງານ — watchlist only | [2] |
| 15 | Earlier 2026 implant reports incl. Thailand | — | — | 1 source — omit | [3] |

## Counter-view
- Only one implanted device is confirmed by Ledger; the full mechanism and whether every drained wallet had an implant are unconfirmed [4].
- Ledger has not accused CryptoBilis; tampering could have happened elsewhere in the supply chain [2]. CryptoBilis had no public statement as of 2026-10-09 [2].

## Lao angle
- No Lao victims reported. Lao buyers often buy IT/security devices via Facebook shops or resellers in Thailand/Malaysia. Lesson: buy security hardware only from the maker's official store. Not investment advice.

## Watchlist
| What | When | Why |
|---|---|---|
| Ledger investigation result / authorities | Not dated | Who tampered, how many devices |
| Other brands sold by CryptoBilis | Not dated | Scope may widen beyond Ledger |

## Glossary
| Term | Lao |
|---|---|
| Hardware wallet | ກະເປົາເງິນຄຣິບໂຕແບບຮາດແວ |
| Recovery phrase (seed) | ຄຳກູ້ຄືນ 24 ຄຳ |
| Supply-chain attack | ການໂຈມຕີຜ່ານຫ່ວງໂສ້ການສະໜອງ |
| Implant | ຊິບ/ອຸປະກອນທີ່ຝັງລັບ |

## Sources
[1] Ledger says Southeast Asia reseller linked to $86M draining — Protos — https://protos.com/ledger-says-southeast-asia-reseller-linked-to-86m-draining/ — retrieved 2026-10-13
[2] Ledger's crypto wallets reportedly backdoored, $71 million already moved — Gizmodo — https://gizmodo.com/ledgers-crypto-wallets-reportedly-backdoored-71-million-in-crypto-already-moved-2000824372 — retrieved 2026-10-13
[3] Ledger users warned of potential implant in Malaysian devices — Crypto Briefing — https://cryptobriefing.com/ledger-malaysia-hidden-implant-cryptobilis/ — retrieved 2026-10-13
[4] Ledger confirms hidden hardware implant in affected user's wallet — Bitcoin.com News — https://news.bitcoin.com/security/ledger-confirms-hidden-hardware-implant-in-affected-users-wallet/ — retrieved 2026-10-13
[5] CZ warns Ledger users as Mt. Gox chief reports hidden chip — The Crypto Times — https://www.cryptotimes.io/2026/10/10/cz-warns-ledger-users-as-mt-gox-chief-reports-hidden-chip-in-his-device/ — retrieved 2026-10-13
[6] Ledger confirms spy chip implant behind wallet crypto thefts — BleepingComputer (headline) — https://www.bleepingcomputer.com/ — retrieved 2026-10-13
