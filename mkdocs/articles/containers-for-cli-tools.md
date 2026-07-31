---
title: Containers for CLI Tools
published: true
hide:
- navigation
- toc
description: When and how to ship a CLI tool as a container. Pinning base images,
  running as non-root, keeping the attack surface small, and avoiding container
  anti-patterns for simple utilities.
tags:
- Security
- Tools
---

# Containers for CLI Tools: When a Box Helps

Not every CLI needs a container. Some benefit from one: complex native dependencies, locked runtimes, or identical behaviour in CI and laptops. Containers are a distribution and isolation tool, not automatic security.

## 1. When a Container Earns Its Keep

Good reasons:

- Native libraries that are painful to install
- Guaranteed runtime version
- CI jobs that should not pollute the runner
- Customers who already standardise on images

Bad reasons:

- "Everyone uses Docker"
- Hiding a broken install story forever
- Running as root because the Dockerfile was copied from a wiki

Prefer a plain package (pip/npm/brew) when it works.

## 2. Pin What You Build From

- Pin base image digests or immutable tags
- Rebuild deliberately; do not float on `latest`
- Scan images in CI when you publish them
- Prefer minimal bases (distroless/alpine/slim) when compatible

Your image is a dependency tree in a trench coat.

## 3. Run as Non-Root

Drop root in the final image. Mount only the directories the tool needs. Read-only root filesystem when practical. Least privilege applies inside containers too.

## 4. Keep the Attack Surface Small

- Multi-stage builds so compilers never ship
- No leftover secrets in layers (`docker history` remembers)
- Explicit entrypoint; avoid kitchen-sink images
- Document required volume mounts and ports (usually none for CLIs)

## 5. Version and Sign Like Other Artefacts

Tag images with the same version as the CLI release. Publish digests. Sign or attest when your pipeline supports it. Users should verify what they pull.

## 6. Document Escape Hatches

Explain how to run with local files mounted, how to pass config, and when *not* to use the image. A container that fights host keychains and sockets needs clear guidance.

## 7. Closing Thoughts

Containers can make CLI distribution boring and repeatable. Pin bases, run as non-root, keep layers lean, and still offer a non-container install when you can. The box should help users, not become the product.
