# WhatsApp Morphe Patches — V2 Safe Compatibility

V2 is being rebuilt around **compatibility first**.

## Main rule

There is no credible way to guarantee that a modified WhatsApp account can never be restricted.
For that reason, the stable V2 profile avoids anti-detection, login-integrity bypasses, server-limit
bypasses, automation, bulk messaging, and protocol impersonation.

## V2 Safe profile

Target: **WhatsApp 2.26.27.4** only while V2 is under validation.

Planned stable patch set:

- Anti Revoke — local retention of revoked content
- Anti View Once — local handling of view-once media
- HD Media — local media quality preference
- Copy Statuses — local UI feature
- Remove Communities — local UI feature
- Remove Updates — local UI feature
- Anti Edit — local message-history behavior
- Anti Disappearing — local message-retention behavior

High-risk / compatibility-sensitive patches are intentionally excluded from the stable V2 bundle:
Anti Detector, Login Fix, signature/integrity bypasses, forward-limit bypasses, network-security
disabling, and similar patches.

## Compatibility policy

See [docs/COMPATIBILITY_V2.md](docs/COMPATIBILITY_V2.md) and
[compatibility/2.26.27.4.json](compatibility/2.26.27.4.json).

The V2 branch is experimental until an actual WhatsApp APK for the declared version passes
patch-time and launch testing on-device.
