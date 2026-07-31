# Legacy claim-registry mirrors

The authoritative epistemic claim registry is:

- `docs/CLAIMS.md`

The canonical machine-readable mirrors are:

- `docs/CLAIMS.csv`
- `docs/CLAIMS.json`

The files in this directory are retained only for backward compatibility with earlier repository paths:

- `claims/claim_registry.csv`
- `claims/claim_registry.json`

They must remain byte-for-byte equivalent in scientific content to the canonical `docs/CLAIMS.*` mirrors. CI treats any divergence as a repository defect. New tools and contributors should read `docs/CLAIMS.*` directly and must not edit the legacy mirrors independently.
