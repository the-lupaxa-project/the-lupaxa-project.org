---
title: Secrets Management
published: true
hide:
- navigation
- toc
description: What counts as a secret, the five ways secrets management usually goes
  wrong, and the practices and tools that keep credentials out of your codebase and
  under control.
tags:
- Security
- DevOps
---

# Secrets Management: Keeping Credentials Under Control

Every application of any size runs on credentials it must not reveal. API keys, database passwords, encryption keys. Secrets management is the practice of storing, distributing, and controlling access to those credentials so that the thing which authenticates your service does not also authenticate an attacker.

Get it wrong and the failure mode is not subtle. Exposed credentials mean unauthorised access to systems and data, usually before anyone notices.

## 1. What Counts as a Secret

Anything that grants access or protects data:

- **API keys:** credentials for external services, payment gateways, cloud platforms, third-party APIs.
- **Database credentials:** the usernames and passwords your application uses to connect.
- **Encryption keys:** whatever encrypts or decrypts your sensitive data.
- **SSH keys:** remote access to servers.
- **Certificates and tokens:** digital certificates and authentication tokens that prove identity or authorise access.

If leaking it would let someone act as you, treat it as a secret.

## 2. Why It Deserves Real Effort

### It Prevents Breaches

An exposed API key or database password is direct unauthorised access to systems and data. Managing secrets properly removes the most common route in.

### It Absorbs Human Error

Hand-managed secrets get hardcoded into source, pasted into config files, and shared in chat. Tooling automates the handling and takes the opportunity for accidents away from tired people.

### Regulators Expect It

Compliance standards mandate secure handling of sensitive information: PCI-DSS for payment data, HIPAA for healthcare. Effective secrets management is how you meet those requirements instead of explaining a fine.

### It Speeds Development Up

This one surprises people. When secure access to credentials is a solved problem, developers stop improvising around it. No manual configuration steps, no waiting for someone to email a password, no incidents caused by a shortcut.

## 3. The Five Ways It Goes Wrong

### Secrets Hardcoded in Code

The most common mistake, and the worst. A secret embedded in code is visible to everyone with repository access, and it stays in version control history and backups long after you delete the line.

**Fix:** keep secrets in environment variables, in config files excluded from version control, or in a dedicated secrets manager. Never in application code.

### Access That Is Too Broad

Giving the whole team production credentials means any one compromised laptop compromises production.

**Fix:** least privilege, so each person and service can reach only the secrets they need. Role-based access control (RBAC) makes that enforceable rather than aspirational.

### No Rotation or Expiry

A secret that never changes is a secret that stays useful to an attacker indefinitely. If one leaked without detection, they still have access today.

**Fix:** rotate on a schedule and set expiry on temporary credentials. Automated tooling can rotate for you and alert when something needs refreshing.

### Nothing Watching

Without an audit trail you cannot tell whether a secret was retrieved by your deployment pipeline or by someone else, and you have nothing to show a compliance auditor.

**Fix:** use tooling that logs access. Track who read which secret, when, and from where, and alert on access patterns that look wrong.

### Weak or Missing Encryption

Secrets sitting in plaintext, or crossing the network unencrypted, are available to anyone who can read the disk or the traffic.

**Fix:** encrypt at rest and in transit. AES-256 for storage, TLS for transport. Most secrets managers do this for you, which is a good reason to use one.

## 4. Practices Worth Adopting

### Use a Dedicated Tool

Manual secrets management does not scale past a couple of people. `HashiCorp Vault`, `AWS Secrets Manager`, `Azure Key Vault`, and `Google Cloud Secret Manager` all give you secure storage, access control, and monitoring in one place.

### Inject Through Environment Variables

Environment variables let you pass credentials into a running application without them appearing in the codebase. The values live in the runtime environment, not in a file someone can commit.

### Keep Secrets Out of Version Control

Private repositories are not a security boundary. Use `.gitignore` to exclude config files that hold credentials, and inject the real values at deployment time. Once a secret reaches git history, rotating it is the only real fix.

## 5. The Tools

### HashiCorp Vault

Open source and the most flexible of the set. Dynamic secrets, encrypted storage, access control, and audit logging, with API access and integrations across cloud providers. Worth the setup cost if you are not tied to one platform.

### AWS Secrets Manager

Fully managed, built for AWS-based applications. Automatic rotation, access control, and monitoring, wired into the rest of AWS.

### Azure Key Vault

Cloud-based storage for cryptographic keys, secrets, and certificates, integrated with Azure identity management and access control.

### Google Cloud Secret Manager

Secure and scalable secret storage for GCP, with access control, audit logging, and integration with other Google Cloud services.

## Closing Thoughts

Secrets management is unglamorous work that quietly decides how bad your worst day is. Use a dedicated tool, restrict access to what each caller needs, rotate on a schedule, encrypt everywhere, and keep credentials out of the repository.

Do that and you get the security benefit plus a smoother operation, because a team that never has to improvise around credentials ships faster and breaks less.
