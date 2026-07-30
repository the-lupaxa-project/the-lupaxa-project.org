---
title: GitHub Actions
published: true
hide:
- navigation
- toc
description: Learn how to use GitHub Actions for CI/CD, with a step-by-step guide
  on automating builds, tests, and deployments, complete with YAML configurations
  and best practices.
tags:
- CI/CD
- GitHub
---

# Using GitHub Actions for CI/CD: A Comprehensive Guide

GitHub Actions have quickly become a popular choice for automating CI/CD workflows directly within GitHub. With GitHub Actions, developers can automate the build, test, and deployment processes without needing an external CI/CD tool, making it a convenient and powerful option for streamlining software delivery. This article will explore how GitHub Actions can be used for CI/CD, with step-by-step examples, YAML configurations, and directory structures.

## 1. What are GitHub Actions?

GitHub Actions are a workflow automation tool integrated directly into GitHub. It allows developers to create custom workflows that respond to GitHub events, such as pushes, pull requests, or issues. For CI/CD, GitHub Actions enables you to automate the build, test, and deployment processes each time code changes are pushed to the repository.

Key features include:

- **Event-driven workflows:** Workflows can be triggered by events like code pushes, pull requests, issue creation, or on a schedule.
- **Customizable workflows:** YAML-based configuration allows for easy customization of workflows to fit specific project needs.
- **Pre-built actions and reusable workflows:** GitHub provides a marketplace with pre-built actions that can be reused, reducing the time and effort required to create workflows from scratch.
- **Integrated with GitHub ecosystem:** Since GitHub Actions is built into GitHub, it integrates seamlessly with your repository, making it easy to set up and manage CI/CD.

## 2. Setting Up CI/CD with GitHub Actions

Let's walk through setting up a simple CI/CD pipeline using GitHub Actions. For this example, we'll cover:

- Directory structure
- Writing a basic GitHub Actions YAML configuration
- Running automated tests
- Deploying to a staging environment

### Directory Structure

When setting up GitHub Actions, workflows are defined within the `.github/workflows` directory of your repository. This directory contains YAML files that specify the workflows you want to create.

Here's an example directory structure for a Node.js application:

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

The file `.github/workflows/ci-cd.yml` is where we'll define our GitHub Actions workflow.

### Writing a Basic CI/CD Workflow

Let's start with a simple CI/CD workflow that installs dependencies, runs tests, and builds the project each time code is pushed to the `master` branch.

Create a YAML file named `ci-cd.yml` within the `.github/workflows` directory and add the following configuration:

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

### Explanation of the Workflow Steps:

<!-- markdownlint-disable MD030 -->
- **name:** Gives the workflow a name for easy identification.
- **on:** Specifies the events that trigger this workflow. Here, the workflow runs on `push` and `pull_request` events targeting the `master` branch.
- **jobs:** Defines the jobs to run within the workflow.
  - **build:** Defines a job called build that runs on an Ubuntu virtual machine.
  - **steps:** Defines the individual steps for this job:
    - **Checkout code:** Uses the `actions/checkout@v3` action to pull the repository code.
    - **Set up Node.js:** Uses `actions/setup-node@v3` to set up a Node.js environment with the specified version (Node.js 14 in this case).
    - **Install dependencies:** Installs project dependencies with `npm install`.
    - **Run tests:** Runs tests using the `npm test` command.
    - **Build application:** Builds the application with `npm run build`.
<!-- markdownlint-enable MD030 -->

This basic workflow provides a foundational CI pipeline. Every time code is pushed to the main branch, the workflow installs dependencies, runs tests, and builds the application, providing immediate feedback if any step fails.

## 3. Adding Deployment to the Workflow

In this section, we'll extend the workflow to include deployment. In this example, we'll demonstrate deployment to an S3 bucket, commonly used to host static files.

### Extending the YAML for Deployment:

We'll assume that we have AWS credentials set up as GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`), as well as a `BUCKET_NAME` for deployment.

Update the `ci-cd.yml` file as follows:

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

### Explanation of Deployment Step:

- **if: success():** This ensures that the deployment step runs only if the previous steps were successful.
- **env:** This block sets up environment variables for AWS credentials using secrets stored in the GitHub repository.
- **run:** Uses the AWS CLI to sync the contents of the ./build directory with the specified S3 bucket.

To set up your AWS credentials and bucket name as secrets, navigate to your GitHub repository, go to `Settings > Secrets > Actions`, and add each secret ( `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `BUCKET_NAME`).

## 4. Adding a Manual Approval Step for Deployment

For teams that want a layer of control before deploying to production, GitHub Actions supports manual approval steps using the `workflow_dispatch` event.

Here's an example of how to add a manual approval step:

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

### Explanation of Manual Approval Step:

- **workflow_dispatch:** Allows you to manually trigger this workflow from the GitHub Actions tab in your repository.
- **f: github.event_name == 'workflow_dispatch':** Ensures that the deployment step is only triggered if the workflow was manually started. This condition provides an additional layer of control, so code is not automatically deployed with every push.

## 5. Best Practices for Using GitHub Actions in CI/CD

When using GitHub Actions for CI/CD, consider the following best practices:

- **Use Secrets for Sensitive Data:** Always store sensitive data, such as API keys and AWS credentials, as secrets in GitHub.
- **Cache Dependencies:** To speed up workflows, use the `actions/cache@v3` action to cache dependencies, which will reduce installation time for subsequent runs.
- **Limit Permissions:** GitHub Actions runs with elevated permissions. Limit these permissions where possible to reduce the risk of accidental or malicious changes.
- **Monitor and Review:** Regularly monitor workflows and review logs for successful and failed runs. Analysing these logs can help identify potential issues and optimise workflows.

## Conclusion: Powering CI/CD with GitHub Actions

GitHub Actions provides a powerful, flexible platform for automating CI/CD directly within GitHub. By leveraging GitHub Actions, teams can streamline the development lifecycle, from code integration and testing to deployment. With easy-to-configure YAML files, seamless integration with the GitHub ecosystem, and support for various environments, GitHub Actions is a valuable tool for any software development team.

This guide has covered the basics of setting up a CI/CD pipeline with GitHub Actions, including configurations for builds, tests, and deployments. With a solid understanding of GitHub Actions, you can customize and scale your workflows to meet the unique demands of your projects and bring greater efficiency to your development process.
