# Agentic Creative Studio

> A collaborative multi-agent AI system that automates creative content generation with built-in compliance and brand safety loops. Built for the Neural.Net Hackathon.

## 📋 Table of Contents
- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage](#-usage)

## 💡 About The Project
Modern creative workflows are fragmented, often requiring manual coordination between copywriting, legal review, and design teams. This leads to bottlenecks and a 45% rework rate.

**Agentic Creative Studio** solves this by deploying an autonomous squad of AI agents that work exactly like a human team:
1.  **Writer Agent:** Drafts initial creative copy based on a brief.
2.  **Reviewer Agent (Compliance):** Validates the copy against strict brand & legal guidelines.
3.  **Router (The Manager):** Automatically rejects non-compliant work and sends it back for revision.
4.  **Art Director Agent:** Generates matching visual assets only after the text is approved.

## ✨ Key Features
* **Truly Autonomous Workflow:** Agents collaborate, review, and hand off tasks without human intervention after the initial prompt.
* **Self-Correcting (Human-in-the-Loop Logic):** Implements a "Validate & Refine" loop where the Reviewer agent can reject drafts, forcing the Writer agent to iterate.
* **100% Open-Source Models:** Powered exclusively by open-source LLMs (Llama 3) and Image Models (Stable Diffusion v1.5).
* **Zero-Cost Infrastructure:** Optimized to run entirely on high-performance free-tier APIs (Groq & Hugging Face).

## 🏗 Architecture

Our system uses **LangGraph** to define a stateful, cyclic workflow.

```mermaid
graph TD
    A[Start: User Prompt] -->|State| B(Writer Node / Llama3)
    B -->|Draft Text| C(Reviewer Node / Llama3)
    C -->|Feedback| D{Router Decision}
    D --"REVISE"--> B
    D --"APPROVED"--> E(Art Director Node / SD v1.5)
    E -->|Saves locally| F[End: Final Assets]
    
    style D fill:#f9f,stroke:#333,stroke-width:2px
