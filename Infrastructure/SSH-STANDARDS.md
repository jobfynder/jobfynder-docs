# SSH Standards

**No real content exists anywhere in this repo to fill this from.** Template only.

Known, but not a documented standard: `jobfynder/jobfynder-infra` has ed25519 public keys committed under `pavan@jobfynder.com`. That confirms a key exists — it says nothing about rotation policy, who else has access, or bastion/jump-host setup.

To fill this in for real: key rotation policy, who has access to which servers, whether a bastion host is used, and where private keys are actually stored (should never be in a git repo — worth double-checking `jobfynder-infra` doesn't have one, since it did have public keys sitting in it under a confusing filename).
