---
title: GitHub Actions
published: true
publish_date: "2026-07-30T10:47:40"
hide:
- navigation
- toc
description: Build a working CI/CD pipeline with GitHub Actions, from a first build-and-test
  workflow to deploying an artefact, with the YAML to copy and the habits that keep
  workflows fast and safe.
tags:
- CI/CD
- GitHub
---

# GitHub Actions: CI/CD Without Leaving Your Repository

GitHub Actions puts your pipeline next to your code. No separate CI server, no second set of credentials to manage, no tab-switching to find out why the build went red. You commit a YAML file and GitHub runs it.

This walkthrough builds up a pipeline in stages: test on every push, then deploy, then put a human in front of production.

## What GitHub Actions Actually Is

It is an event-driven runner attached to your repository. Something happens (a push, a pull request, a schedule, a manual click) and GitHub executes the jobs you defined.

The parts worth knowing:

- **Events** trigger workflows: pushes, pull requests, issue activity, cron schedules.
- **YAML** defines everything, so your pipeline is reviewable and versioned like the rest of the repo.
- **Marketplace actions** cover the boring steps (checkout, language setup, caching) so you are not scripting them yourself.
- **Repository integration** means secrets, environments, and status checks are already where you expect them.

## Building a Pipeline

Four things to get right: where the files live, a workflow that installs and tests on every push, a deploy step, and a way to hold that deploy back until someone approves it.

### Directory Structure

Workflows live in `.github/workflows`. Every YAML file in that directory is a workflow GitHub will consider running.

A Node.js project might look like this:

```bash
my-project/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── src/
│   └── index.js
│
├── tests/
│   └── index.test.js
│
├── package.json
└── README.md
```

Everything below happens in `.github/workflows/ci-cd.yml`.

### A Workflow That Installs, Tests, and Builds

Start with the pipeline you will actually use every day: on each push and pull request to `main`, install dependencies, run the tests, build the project.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '14'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Build application
        run: npm run build
```

### Reading the Workflow

<!-- markdownlint-disable MD030 -->
- **name:** what shows up in the Actions tab.
- **on:** the triggers. Here, pushes and pull requests aimed at `main`.
- **jobs:** the work itself.
  - **build:** one job, running on a GitHub-hosted Ubuntu machine.
  - **steps:** run in order, and the job stops at the first failure:
    - **Checkout code:** `actions/checkout@v3` fetches the repository into the runner.
    - **Set up Node.js:** `actions/setup-node@v3` installs the version you pin (Node.js 14 here).
    - **Install dependencies:** `npm install`.
    - **Run tests:** `npm test`.
    - **Build application:** `npm run build`.
<!-- markdownlint-enable MD030 -->

That is a complete CI pipeline. Push to `main` or open a pull request and you find out within minutes whether you broke something, which is the whole point.

## Adding Deployment

Next, ship the build. This example syncs a static site to an S3 bucket.

### Extending the Workflow

Store the AWS credentials as repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) along with `BUCKET_NAME`. Never put them in the YAML.

The updated `ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '14'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Build application
        run: npm run build

      - name: Deploy to S3
        if: success()
        env:
          AWS_ACCESS_KEY_ID: ${{ '{{' }} secrets.AWS_ACCESS_KEY_ID {{ '}}' }}
          AWS_SECRET_ACCESS_KEY: ${{ '{{' }} secrets.AWS_SECRET_ACCESS_KEY {{ '}}' }}
          AWS_REGION: ${{ '{{' }} secrets.AWS_REGION {{ '}}' }}
        run: |
          aws s3 sync ./build s3://$BUCKET_NAME --region $AWS_REGION
```

### The Deploy Step

- **if: success():** only deploy when the earlier steps passed. A failed test should never reach the bucket.
- **env:** pulls the credentials from repository secrets into the step's environment.
- **run:** the AWS CLI syncs `./build` to the bucket.

To add the secrets, go to `Settings > Secrets > Actions` in the repository and add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and `BUCKET_NAME`.

## Putting a Human in Front of Production

Automatic deploys on every push are fine for staging. For production, most teams want someone to press the button. Splitting build and deploy into separate jobs and gating the deploy on `workflow_dispatch` gets you that:

```yaml
name: CI/CD Pipeline with Manual Deployment Approval

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '14'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Build application
        run: npm run build

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'workflow_dispatch'
    steps:
      - name: Deploy to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ '{{' }} secrets.AWS_ACCESS_KEY_ID {{ '}}' }}
          AWS_SECRET_ACCESS_KEY: ${{ '{{' }} secrets.AWS_SECRET_ACCESS_KEY {{ '}}' }}
          AWS_REGION: ${{ '{{' }} secrets.AWS_REGION {{ '}}' }}
        run: |
          aws s3 sync ./build s3://$BUCKET_NAME --region $AWS_REGION
```

### The Gate

- **workflow_dispatch:** adds a "Run workflow" button in the Actions tab.
- **needs: build:** the deploy job waits for a green build.
- **if: github.event_name == 'workflow_dispatch':** the deploy only runs when a person started the workflow. Ordinary pushes still build and test, they just stop short of shipping.

## Habits Worth Keeping

- **Secrets stay secrets.** API keys and cloud credentials belong in repository or environment secrets, never in the YAML or a committed `.env`.
- **Cache your dependencies.** `actions/cache@v3` cuts install time on repeat runs, which is usually the cheapest speed win available.
- **Trim permissions.** Workflow tokens are generous by default. Narrow them to what the job needs so a compromised action cannot rewrite your repository.
- **Read the logs.** Check both failures and successes now and then. Slow steps and flaky tests show up there long before anyone complains.

## Closing Thoughts

The value of GitHub Actions is proximity: the pipeline lives with the code, changes through pull requests, and reports back in the same place you already work.

Start with the build-and-test workflow above. Add deployment when the tests are worth trusting, add a manual gate when a mistake would reach real users, and grow from there. A pipeline you can read in one screen beats an elaborate one nobody understands.
