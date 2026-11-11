# Bloodline Voice MVP — Implementation Plan

## Scope
Voice AI first. No CRM, live number port, automated estimates, or appointment booking in this phase.

## Verified baseline
- Forked from kirklandsig/AIReceptionist.
- Existing framework: LiveKit Agents + OpenAI Realtime + SIP integration.
- Python 3.11+; standard OpenAI API key required.
- Upstream license: AGPL-3.0. Preserve notices and review network-use obligations.

## Voice behavior
- Introduce itself explicitly as Bloodline Hauling's virtual receptionist.
- Qualify junk removal, property cleanouts, furniture, appliances, mattresses, and debris hauling.
- Ask for caller name, callback number, service location, item types, approximate quantity, access constraints, and preferred callback window.
- Repeat essential details for confirmation.
- Never quote binding prices, promise availability, or finalize appointments.
- Ask callers to send photos using the business's approved existing messaging channel; do not promise automatic text delivery before it is integrated.
- Offer human callback when uncertain or when caller requests it.
- Handle emergencies by advising appropriate emergency services, not by inventing business capabilities.

## Initial acceptance tests
1. Agent starts in a sandbox with test credentials.
2. Natural two-way speech and interruptions work.
3. Caller information is captured and summarized.
4. Unclear requests and silence recover gracefully.
5. No unapproved price or scheduling commitments.
6. No real customer calls routed until end-to-end tests pass.

## Deferred decisions
- Confirm Mike's operating hours, escalation number, and exact service area.
- Choose a test SIP number/provider after a voice-only session works.
- Verify conditional forwarding with the eventual carrier.
- Determine call recording and consent requirements before enabling recording.
- CRM and SMS automation are Phase 2.

## Security
Never commit .env, API keys, customer information, or recordings. Keep the fork's AGPL license and attribution.
