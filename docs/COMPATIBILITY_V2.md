# V2 Compatibility Policy

V2 prioritizes compatibility and account safety over feature count.

## Rules

1. Support only explicitly tested WhatsApp versions.
2. Fail closed: if a fingerprint is not found, abort that patch instead of guessing.
3. Keep risky patches out of the stable profile.
4. Do not bypass server-side limits or automate messaging.
5. Do not ship anti-detection or login-integrity bypasses in the stable bundle.
6. Test each patch independently, then in combinations.
7. Promote a WhatsApp version to stable only after:
   - patch-time success;
   - app launch success;
   - basic send/receive smoke test;
   - media send/receive smoke test;
   - restart test;
   - no crash during a short soak test.

## Risk groups

### Stable-candidate
Local UI or local message/media behavior:
- Anti Revoke
- Anti View Once
- HD Media
- Copy Statuses
- Remove Communities
- Remove Updates
- Anti Edit
- Anti Disappearing

### Excluded from stable V2
- Anti Detector
- Login Fix
- signature/integrity spoofing
- network-security disabling
- forwarding/server-limit bypasses
- automation/bulk messaging
- protocol impersonation

No modified WhatsApp build can be guaranteed ban-proof. This policy reduces avoidable risk; it does not remove platform-side enforcement risk.
