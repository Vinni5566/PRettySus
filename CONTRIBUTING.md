# Contributing to PRettySus

First off, thanks for taking the time to contribute!

## Core Philosophy
PRettySus is an **AI-free, deterministic static analysis tool**. 
We do not accept contributions that introduce LLM dependencies, AI-based text generation, or heuristic probability-based text classifiers (like GPTZero). All checks must be rooted in deterministic string matching, regex parsing, and structured data analysis.

## Development Setup
1. Clone the repo
2. Run `make install` to install frontend and backend dependencies.
3. Run `make test` to ensure the deterministic tests pass.
4. Run `make demo` to start the frontend and backend servers.

## Pull Request Process
1. Ensure your PR description adequately explains *why* the change is being made and *how* it affects the scoring algorithm.
2. Ensure you have added `pytest` coverage for any new static analysis rules.
3. Keep the codebase modular. Analyzers should remain independent of each other.
