# LiquidCSS Scout

LiquidCSS Scout is a small Python tool that helps you trim CSS safely in projects that use
Liquid templates (Shopify themes), plain HTML, and a bit of JS.

It scans your project for class/id usage, then compares that against a CSS file and tells you:
- what looks used
- what looks unused
- what’s *maybe* used (usually because of Liquid `{{ }}` or other dynamic stuff)

It can also write out a pruned CSS file.

This is not trying to be a perfect CSS parser. The goal is practical: reduce the “CSS junk drawer”
without accidentally breaking your theme.

---

## Why this exists

If you’ve ever tried to remove unused CSS from a Shopify theme, you already know the problem:

- classes are scattered across `.liquid` files
- some class names are dynamic (`class="{{ section.id }} ..."`)
- JS may add/remove classes at runtime
- a normal “search and delete” pass is slow and risky

LiquidCSS Scout is conservative by default. If it’s not sure, it keeps the rule.

---

## Install

From source:

```bash
pip install -e .
