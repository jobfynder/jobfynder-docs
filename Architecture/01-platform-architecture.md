Platform Architecture
Executive Summary

Jobfynder is a distributed, AI-powered recruitment platform built as a collection of independent services.

Rather than operating as a monolithic application, the platform separates communication, intelligence, business logic, search, messaging, and data storage into dedicated services.

This architecture enables:

Independent scaling
Higher reliability
Faster deployments
Better fault isolation
Vendor independence
AI provider flexibility
Long-term maintainability

Every service exists for a single reason and communicates through well-defined interfaces.

2.1 Platform Vision

Jobfynder is not:

a job board
an ATS
a CRM
a messaging app

Jobfynder is a Recruitment Operating System.

Its purpose is to connect fragmented recruiting workflows into one intelligent platform.

The platform continuously transforms:

Unstructured Communication

↓

Structured Knowledge

↓

Intelligent Actions

↓

Successful Placements

This transformation is the core capability of Jobfynder.

2.2 Architectural Principles

Every component of the platform follows these principles.

Principle 1
One Responsibility

Every service owns exactly one business capability.

Examples

Hermes

→ AI Intelligence

ERS

→ Communication

Jobfynder Core

→ Business Logic

Typesense

→ Search

RabbitMQ

→ Message Delivery

Redis

→ Fast State

Principle 2
Loose Coupling

Services should communicate using APIs or asynchronous events.

No service should directly depend on another service's internal implementation.

This enables:

easier deployment
simpler testing
independent scaling
Principle 3
Stateless Processing

Business services should remain stateless whenever possible.

State belongs in:

PostgreSQL
Redis
RabbitMQ
Typesense

not inside application memory.

This allows:

horizontal scaling
container replacement
rolling deployments
Principle 4
Event-Driven

Whenever possible,

communication should happen through events rather than direct calls.

Example

Recruiter submits a Job

↓

RabbitMQ

↓

Hermes

↓

Job Parser

↓

Matching Worker

↓

Notification Worker

Multiple systems can react independently.

2.3 Platform Components
User Channels

Users interact through:

Web Application
Telegram
WhatsApp
Email
Browser Extension
REST API
Future Mobile App

These channels should remain "thin."

Business logic never belongs inside channels.

Communication Layer

COMM-1

Responsibilities:

Reverse Proxy
SSL
RabbitMQ
Redis
ERS
Webhooks
Telegram Gateway
WhatsApp Gateway
Email Gateway

Purpose:

Receive information.

Route information.

Never perform AI.

Intelligence Layer

INTEL-1

Responsibilities:

Hermes
AI Workers
Parsing
Matching
Embeddings
Knowledge Engine
Learning Engine
Typesense

Purpose:

Transform information into knowledge.

Business Layer

Jobfynder Core

Responsibilities:

Authentication
Authorization
Business Rules
Workflows
Social Network
Job Management
Consultant Management
Vendor Network
Trust Engine
Billing
Data Layer

Persistent Data

PostgreSQL

Search

Typesense

Transient State

Redis

Messaging

RabbitMQ

Files

Cloudinary

AI Layer

Portkey

↓

Model Routing

↓

Gemini

↓

DeepSeek

↓

Future Models

Langfuse continuously observes quality, latency, cost, and traces.

2.4 Platform Diagram

This diagram should be included in JEOS (we'll later turn it into a polished Mermaid or Draw.io diagram):

                           USERS
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
     Web UI               Telegram               WhatsApp
        │                      │                      │
        └──────────────┬───────┴──────────────┬───────┘
                       │
                  Cloudflare
                       │
               Nginx Proxy Manager
                       │
                 COMM-1 Server
      ┌────────────────────────────────────────────┐
      │ Redis                                     │
      │ RabbitMQ                                 │
      │ ERS (future)                             │
      │ Telegram Gateway                         │
      │ WhatsApp Gateway                         │
      │ Email Gateway                            │
      └───────────────────┬────────────────────────┘
                           │
                    Internal Docker Network
                           │
                    INTEL-1 Server
      ┌────────────────────────────────────────────┐
      │ Hermes API                                │
      │ Job Parser                                │
      │ Resume Parser                             │
      │ Matching Engine                           │
      │ Knowledge Engine                          │
      │ Typesense                                │
      └───────────────────┬────────────────────────┘
                           │
                    Jobfynder Core
                           │
                     PostgreSQL
                           │
                      Cloudinary
2.5 Service Boundaries
Service	Owns
Hermes	AI reasoning, parsing, orchestration
ERS	Real-time communication and message delivery
Jobfynder Core	Business rules and workflows
RabbitMQ	Event transport
Redis	Cache and temporary state
Typesense	Search index
PostgreSQL	Persistent system of record
Cloudinary	File and media storage
Portkey	AI gateway and routing
Langfuse	AI observability and evaluation

Rule: A service must never "reach inside" another service's database or internal implementation. Communication happens through APIs or events.

2.6 Data Flow Philosophy

Every workflow follows the same lifecycle:

Capture
    ↓
Validate
    ↓
Normalize
    ↓
Enrich
    ↓
Store
    ↓
Index
    ↓
Notify
    ↓
Learn

Examples:

Job posting
Resume submission
Hotlist upload
Recruiter message
Consultant onboarding

This consistency simplifies both development and debugging.

2.7 Non-Functional Requirements

Every production service must provide:

/health
/version
Structured JSON logging
Metrics
Configuration through environment variables
Docker image
Graceful shutdown
Timeouts
Retry strategy (where appropriate)
Automated tests

These are mandatory standards, not optional enhancements.

2.8 Scalability Strategy

Design for growth in stages:

Stage 1 – MVP
Docker Compose
Two DigitalOcean servers
Manual deployments
Stage 2 – Growth
GitHub Actions
Container Registry
Automated deployments
Improved monitoring
Stage 3 – Scale
Multiple communication nodes
Multiple intelligence nodes
Managed databases (if required)
High availability

This staged approach avoids premature complexity while keeping a clear path for expansion.

📌 ADR References

At the end of the chapter, reference the Architecture Decision Records that support it:

ADR-0001 – Platform Engineering Philosophy
ADR-0002 – Two-Server Architecture
ADR-0003 – Communication / Intelligence Separation
ADR-0004 – Docker Compose as Initial Orchestration
ADR-0005 – RabbitMQ as Event Backbone