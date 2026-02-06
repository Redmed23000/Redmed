# Redmed Secure Telehealth Monorepo

Production-oriented bilingual (FR/EN) Swiss telehealth platform MVP monorepo.

## Assumptions
- Switzerland-only service model.
- No cross-border prescriptions.
- No guarantee of medical outcomes.
- Platform scope: intake, triage, follow-up, documentation, secure messaging, teleconsultation support.

## Structure
- `apps/marketing`: Public marketing site (`/fr`, `/en`).
- `apps/patient`: Patient portal.
- `apps/clinician`: Clinician dashboard.
- `packages/db`: Prisma schema + client.
- `packages/shared`: Zod schemas, RBAC, encryption, rate limiting.
- `packages/ui`: Shared UI primitives.

## Local setup
1. Install pnpm 9+.
2. `pnpm install`
3. Start Postgres and create database.
4. `cp .env.example .env`
5. `pnpm --filter @redmed/db generate`
6. `pnpm --filter @redmed/db migrate`
7. Run apps:
   - `pnpm --filter @redmed/marketing dev`
   - `pnpm --filter @redmed/patient dev -- --port 3001`
   - `pnpm --filter @redmed/clinician dev -- --port 3002`

## Environment variables
See `.env.example`, plus app-specific `.env.example` files under each app.

## Security notes
- Auth via Auth0 with role claim and MFA claim checks.
- MFA required for clinician and admin sensitive API flows.
- Server-side RBAC checks in APIs.
- AES-256-GCM field encryption for clinical notes/messages/intake summaries.
- Append-only audit log model and write helper.
- Security headers configured (CSP, HSTS, frame denial).
- Rate limiting for auth/sensitive endpoints via shared helper.

## Deployment
1. Provision managed Postgres and run Prisma migrations.
2. Configure Auth0 tenant/app, role claims, and MFA policy (required for clinician/admin).
3. Configure Stripe product/subscription + billing portal return URL.
4. Configure S3-compatible storage credentials and private bucket.
5. Configure Sentry DSN for server and client.
6. Deploy each Next.js app separately (e.g., Vercel), share packages through monorepo build.
7. Set strict HTTPS and domain-level security controls.

## Compliance posture (MVP)
- Swiss-only patient operations.
- Emergency disclaimer included in public marketing copy.
- No automated medical outcome promises.
- Auditability, least-privilege RBAC, encrypted sensitive fields.
