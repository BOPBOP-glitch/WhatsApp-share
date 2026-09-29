# Compatibility-Only Development

This branch changes **no patch features or behavior**.

Its purpose is only to improve build and version compatibility around the existing patch set.

## Rules

- Keep the patch set identical to `main`.
- Do not add, remove, enable, disable, or alter patch behavior.
- Keep all existing defaults unchanged.
- Validate that the generated Morphe bundle contains DEX.
- Validate that every existing patch still targets `com.whatsapp`.
- Add WhatsApp versions only after build-time and device testing.
- Treat an untested WhatsApp version as unsupported.

## Current target

- Package: `com.whatsapp`
- Declared version: `2.26.27.4`
- Status: experimental until real-device testing is completed.

Compatibility work must not be described as anti-ban protection. Platform-side enforcement cannot be guaranteed by a patch bundle.
