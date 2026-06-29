# Quantcast Measure GTM Web Tag

**A sandboxed Google Tag Manager template for the Quantcast Measure pixel: page views, conversions, custom labels and consent, without Custom HTML.**

[![Maintained by New North Digital](https://img.shields.io/badge/Maintained%20by-New%20North%20Digital-455CE9)](https://newnorth.nl/?utm_source=github&utm_medium=gtm-template&utm_campaign=quantcast-web-tag)

## Features

- Page-view and conversion modes from a single tag.
- Pushes onto the native `_qevents` queue and loads `quant.js` once per page.
- Conversion mode adds `event: 'refresh'` with optional revenue and order ID for ROAS and dedupe.
- Custom labels in `_fp.event.<Name>` format for Audience Insights segmentation.
- Custom-variable table for extra keys such as `pcat`, `customer` or `uid`.
- Debug logging gated behind a checkbox; nothing sensitive is logged.

## Why this instead of Custom HTML?

Quantcast's only client-side GTM path today is a Custom-HTML container import. A sandboxed template runs without the `Custom HTML` permission, validates its inputs, scopes its script-injection to `secure.quantserve.com`, and integrates cleanly with GTM Consent Mode.

## Installation

### From the Community Template Gallery
1. In a GTM web container, open **Templates → Tag Templates → Search Gallery**.
2. Search for **Quantcast Measure by New North Digital** and add it.
3. Create a new tag from the template.

### Manual installation
1. Download `template.tpl` from this repo.
2. In GTM: **Templates → New → ⋮ → Import**, select the file, and save.

## Setup guide

1. **Page view** — create a tag, set Event type to **Page view**, enter your **p-code** (e.g. `p-31kzUz5cMTB9k`, or a GTM variable), and fire it on **All Pages**.
2. **Conversion** — create a second tag, set Event type to **Conversion**, reference your transaction value in **Revenue** and your order reference in **Order ID**, and fire it on your purchase trigger.
3. **Consent** — gate both tags with GTM's tag-level consent settings (require `ad_storage`) or a consent trigger. The Quantcast beacon does not self-gate.

---

Maintained by [New North Digital](https://newnorth.nl/?utm_source=github&utm_medium=gtm-template&utm_campaign=quantcast-web-tag).
