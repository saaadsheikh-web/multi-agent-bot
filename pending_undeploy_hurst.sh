#!/bin/bash
# CEO-ordered undeploy — hurst_regime
# Reason: n=20, WR=25%, PF=0.27, Net=-$3.47 — all thresholds exceeded
# Logged in CEO_LOG.md at 2026-05-27T10:13Z
# Run this on the local machine to execute

curl -X POST -H "X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b" \
  "https://brigida-tristichic-janet.ngrok-free.dev/undeploy?agent=hurst_regime"
echo ""
echo "hurst_regime undeploy sent."
