---
title: Least Privilege for CI
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Hardening CI/CD credentials. Short-lived tokens, OIDC, protected
  environments, and the GitHub Actions patterns that keep long-lived secrets out of
  your pipelines.
tags:
- Security
- CI/CD
---

# Least Privilege for CI: Credentials That Expire

CI is a privileged robot with a keyboard. If it holds long-lived cloud keys or classic PATs, a compromised workflow becomes a compromised estate. Least privilege for CI means the pipeline gets only what it needs, only for as long as it needs it.

## Prefer Short-Lived Identity

Where platforms allow it, use **OIDC / federated identity** so jobs receive temporary tokens instead of stored static keys. An Actions job assuming a cloud role is the common pattern.

Static secrets in repository settings should be the exception you can justify.

## Split Jobs by Trust

- Pull requests from forks: no production secrets
- Build/test: read-only where possible
- Publish/deploy: protected environment, explicit reviewers if needed
- Signing: narrowest key, separate job

A single mega-job with every secret is convenient and unsafe.

## Scope Tokens Ruthlessly

If you must use a token:

- Minimum scopes
- Expiration dates
- Fine-grained permissions over classic "all repos"
- Rotate on a schedule

Org-wide admin PATs in Actions are an incident waiting for a calendar date.

## Protect the Paths That Publish

Require passing checks before deploy. Restrict who can approve production environments. Prevent `pull_request_target` foot-guns that expose secrets to untrusted code.

Treat workflow files as security-sensitive code, because they are.

## Log Access, Not Secrets

Print which identity and role was assumed. Never print tokens. Mask secret values. Assume PR logs are public.

## Inventory and Expire

List CI secrets quarterly. Delete orphans. Confirm OIDC trust policies still match repos that exist. Abandoned workflows with live credentials are quiet liabilities.

## Closing Thoughts

CI least privilege is boring hygiene with outsized payoff: short-lived identity, split trust boundaries, tiny scopes, protected publish paths. Make the pipeline earn every credential, then take it back when the job ends.
