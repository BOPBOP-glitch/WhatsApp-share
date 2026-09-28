# WhatsApp Morphe Patches

Experimental **no-root** Morphe patch source for WhatsApp (`com.whatsapp`).

## Included patches

- Anti Revoke
- Anti View Once / screenshot restriction bypass
- Hide Read Receipts
- Hide Typing Indicator
- Prefer HD Media
- Freeze Last Seen
- Anti Detector
- Login Fix (experimental; may require compatible microG-RE components)

All patches are **disabled by default**. Enable only the patch you need.

## Current target

- WhatsApp `2.26.27.4`
- Morphe patcher `1.14.1`
- Morphe Gradle plugin `1.3.4`

WhatsApp changes its obfuscated code frequently. A patch that works on one version can fail on a newer build.

## Add to Morphe

Repository source:

`https://github.com/BOPBOP-glitch/WhatsApp-share`

Direct add-source link:

`https://morphe.software/add-source?github=BOPBOP-glitch/WhatsApp-share`

## Releases

A semantic commit to `main` triggers GitHub Actions. The workflow builds the Morphe `.mpp` bundle and publishes it as a GitHub Release.

## Safety

Test on a secondary WhatsApp installation/account first. These patches are experimental and are not affiliated with WhatsApp, Meta, Morphe, or PichiWA.

## Attribution

Built from the GPL-3.0 Morphe patch template and selected GPL-3.0 PichiWA patch logic. See `NOTICE` and `LICENSE`.
