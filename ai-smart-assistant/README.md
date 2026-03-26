# AI Smart Assistant — AWS Cloud Club Workshop

An AI-powered HR Smart Assistant built on **Amazon Bedrock**, designed to automate employee inquiries about policies, benefits, and procedures.

Built during the **AWS Cloud Club Workshop** at UNC Charlotte (March 2026) using the AWS SimuLearn platform.

## Problem Statement

An HR department is overwhelmed by **500+ daily employee requests** covering policies, benefits, and procedures. Current limitations include:

- Responses restricted to business hours only
- Limited capacity for simultaneous replies
- No automated or self-service option for employees

## Solution

An AI Smart Assistant powered by Amazon Bedrock that provides **24/7 automated responses** to common HR inquiries, freeing up the HR team to focus on complex cases.

### Architecture

```
Employee Query
      │
      ▼
┌──────────────┐     ┌─────────────────────┐     ┌──────────────┐
│   Amazon     │────▶│  Amazon Bedrock      │────▶│   Amazon     │
│   Bedrock    │     │  Knowledge Bases     │     │     S3       │
│   Agent      │     │  (Policies & Docs)   │     │  (HR Docs)   │
│              │     └─────────────────────┘     └──────────────┘
│              │
│              │     ┌─────────────────────┐     ┌──────────────┐
│              │────▶│   Action Groups     │────▶│  AWS Lambda   │
│              │     │  (Custom Actions)   │     │  (Logic)      │
└──────────────┘     └─────────────────────┘     └──────────────┘
                                                        │
                                                        ▼
                                                 ┌──────────────┐
                                                 │   Amazon     │
                                                 │  DynamoDB    │
                                                 │ (Employee    │
                                                 │  Records)    │
                                                 └──────────────┘
```

## AWS Services Used

| Service | Purpose |
|---------|---------|
| **Amazon Bedrock** | Foundation model hosting and agent orchestration |
| **Amazon S3** | Storage for HR policy documents and knowledge base source data |
| **Amazon OpenSearch Service** | Vector search for knowledge base retrieval |
| **AWS Lambda** | Backend logic for action groups |
| **Amazon DynamoDB** | Employee data and request tracking |

## What I Learned

- Setting up an **Amazon Bedrock Agent** with knowledge bases for retrieval-augmented generation (RAG)
- Connecting **knowledge bases** to S3-hosted documents so the agent can answer policy questions accurately
- Adding **action groups** to extend the agent's capabilities beyond simple Q&A
- Integrating **Lambda functions** as the compute layer for custom actions
- Using **DynamoDB** for structured data lookups alongside unstructured document retrieval

## Workshop Format

This project was built using **AWS SimuLearn**, a generative AI-powered learning platform that simulates real-world client engagements. The format included:

1. **Discovery** — Conversing with an AI-generated HR customer to understand requirements
2. **Design** — Proposing an architecture using AWS services
3. **Build** — Implementing the solution step-by-step in a live AWS Management Console
4. **Validate** — Testing the assistant against real HR queries

## Acknowledgments

- **AWS Cloud Club at UNC Charlotte** for hosting the workshop
- **AWS SimuLearn** for the hands-on learning platform
