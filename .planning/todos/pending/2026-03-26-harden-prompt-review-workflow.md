---
created: 2026-03-26T10:41:43.948Z
title: Harden prompt review workflow
area: general
files: []
---

## Problem

The prompt-review request earlier in this session only told the agent to invoke the safety-review skill and follow its instructions. It did not include the actual prompt that needed review. That leaves the reviewer to analyze the wrapper instruction instead of the real target prompt, which reduces the value of the review and can miss prompt-injection, privacy, or clarity issues in the prompt that actually needs scrutiny.

## Solution

Create a standard prompt-review request template that always includes the target prompt in a clearly delimited block, tells the reviewer to treat that prompt as untrusted input to analyze rather than instructions to execute, and requires explicit handling when the prompt is missing or empty. Reuse that template for future safety-review requests.
