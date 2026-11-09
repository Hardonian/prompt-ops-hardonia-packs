# Security scan evidence — prompt-ops-hardonia-packs

- Scanned: 2026-11-09T02:02:06Z (report dir `agent-scan-20261109T020206Z`)
- Engine: NVIDIA SkillSpector 2.12.0 (Apache-2.0), static heuristics only (`--no-llm`, keyless). 71 detection patterns across 17 categories: prompt injection, data exfiltration, tool poisoning, supply chain, etc. This is the open-source scanner behind NVIDIA's Verified Skills pipeline.

## Results (all top-level content units)

| Unit | Score | Severity | Findings | Verdict |
|---|---|---|---|---|
| assets | 0 | LOW | 0 | SAFE |
| docs | 0 | LOW | 0 | SAFE |
| packs | 0 | LOW | 0 | SAFE |
| scripts | 0 | LOW | 0 | SAFE |

No baseline suppression was needed for this repository — every unit scored 0 on a clean scan.

## Cadence
Every version bump re-scans before publication via `agent-oss-scan.sh` (baseline-aware), plus an automated weekly gate; any unit scoring >=40 halts publication review until human-triaged.

## Limitations
Static analysis proves absence of known malicious patterns in shipped text content; it does not attest to output quality, and LLM-assisted semantic analysis was not used (deliberately keyless/offline for reproducibility).

Questions: reply to your purchase receipt or via the contact listed on the product page.
