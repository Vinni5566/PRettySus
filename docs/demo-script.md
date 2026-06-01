# PRettySus Demo Script (3 Minutes)

## 1. The Hook (0:00 - 0:30)
*Visually: Show a PR with a lot of code changes (e.g., authentication flow) but a terrible description like "update things".*

"Hi everyone. We’ve all seen pull requests like this: 400 lines of code changed, and the description just says 'fixed logic'. 

When engineers use AI to write code, they often submit lazy, generic PR descriptions. Over time, this causes **Squash-and-Merge Amnesia**. The core engineering context—the *why* and the *how*—is lost forever. 

Existing tools try to fix this by asking an LLM, 'Is this AI generated?' which is slow, expensive, and fundamentally flawed. 

Our solution is **PRettySus**: a 100% deterministic, AI-free static analysis tool for engineering communication. We measure *Repository Memory Integrity*."

## 2. The Core Analysis & Communication Coverage (0:30 - 1:15)
*Visually: Run the PRettySus analyzer on the dashboard.*

"Here’s how it works. PRettySus looks at the actual Git diff and extracts the underlying 'code entities'—the variables, the classes, the database models being touched.

Then, it treats the PR description like **Code Coverage**. 
Look at this map. The PR modified critical `auth` and `jwt_manager` files, but the engineer didn't mention them at all. Because these are high-impact files, PRettySus flags this as a **Critical Policy Violation** and heavily drops the score.

We enforce that your English explanation must cover the code you actually wrote."

## 3. Squash Risk & Main Branch Sentry (1:15 - 2:00)
*Visually: Click the "Noisy Squash Merge" sample and hit analyze.*

"But the biggest danger happens at merge time. 

Watch what happens when an engineer pushes 15 micro-commits like 'fix logic' and tries to squash them into the main branch. 

Our **Squash Risk Analyzer** instantly calculates a 'Squash Noise Score' by detecting duplicate clusters and generic phrasing. It activates the **Main Branch Sentry**, which flags this as **UNSAFE FOR MAIN BRANCH**.

But we don’t just reject it. Look at the **Buried Signal** panel. PRettySus found the one commit that actually mattered hidden in the noise. And below that, it provides a **Deterministic Suggested Summary**—built purely from diff analysis and coverage maps—that the engineer can copy to preserve the repository's history."

## 4. Closing & Impact (2:00 - 2:30)
*Visually: Switch to the terminal to show the CLI and GitHub Action.*

"Because PRettySus is purely deterministic, it runs instantly and safely inside your CI/CD pipeline without sending your private code to OpenAI. 

It can run as a GitHub Action, returning beautiful Markdown reports right in your PR comments, or locally as a CLI tool.

We aren't just checking spelling. We are forcing engineers to leave breadcrumbs. PRettySus guarantees that your repository memory remains intact for future engineers, Code Search, and RAG architectures."
