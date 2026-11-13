# Bloodline voice MVP — engineering audit and acceptance gates

Status: **development only**. Do not route the business number to this agent yet.

## Evidence and limits

- Bloodline's three original tests check YAML loading, hours, and prompt text. They do **not** establish a successful voice call.
- The local worker registered with LiveKit Cloud, and a Playground participant joined. This validates basic dispatch, **not** audio generation.
- The observed OpenAI Realtime failure was `invalid_api_key`; a separate direct `models.list()` request returned HTTP 401. A `SET` or `True` dotenv test checks presence only.
- `receptionist/agent.py` calls `load_dotenv(".env.local")` then `load_dotenv(".env")` with default `override=False`. Existing process variables and values from `.env.local` can take precedence over `.env`. This is why the preflight explicitly reports conflicting process values.
- A paid OpenAI balance does not prove that a particular key is valid or has Realtime permission.
- LiveKit Cloud and OpenAI remain hosted dependencies; this is not a fully offline/self-hosted inference stack.
- The repo's own README calls it both production-grade and active development; treat production claims as unverified.

## Safe local verification

From the Bloodline repository root, with the virtual environment active:

```powershell
python -m receptionist.preflight
python -m receptionist.preflight --verify-openai
python -m pytest tests/test_bloodline.py tests/test_preflight.py -q
```

The first command checks configuration without any network requests. The second performs a read-only OpenAI authentication request and prints **no key or provider error body**. A successful models listing is necessary but does not prove Realtime access.

**Security:** Never commit `.env`, `.env.local`, logs containing provider errors, or credentials. Rotate any key exposed in screenshots, terminals, or shared logs.

## Required acceptance gates

1. **Offline configuration:** YAML, hours, guardrails, and safe preflight tests pass.
2. **Authentication:** OpenAI returns success for a direct read-only API request. Then verify Realtime session creation with the same project and key.
3. **Two-way voice:** Playground plays the configured Bloodline greeting, recognizes spoken input, responds audibly, and survives at least five representative intake conversations.
4. **Intake safety:** Capture name, callback, service address, material type, access constraints, volume, and preferred pickup window. Do not claim SMS sent or appointments booked without an actual integration.
5. **Operational reliability:** Test disconnect, no audio, unavailable provider, rate limits, out-of-hours, and retries with no infinite loop.
6. **Telephony and privacy:** Only after approval, configure missed/busy call forwarding, SIP routing, disclosure/consent and data retention, verified delivery channels, and monitoring.

## Dependency / scope decisions

- Keep the LiveKit-based core while validating gate 3. Replacing it now would not resolve an OpenAI 401.
- Pin and test dependency versions before deployment; current `>=` constraints allow unreviewed future updates.
- Review and reduce unused integrations before production. The present Python package includes booking, DTMF, OAuth, recording, messaging, and other functionality that Bloodline's initial intake-only MVP does not require.
- Reassess a minimal LiveKit starter if gate 3 fails after authenticated model access is confirmed.

## Deployment policy

No real caller routing, transfers, SMS, recording, or automatic booking until each integration is configured and tested and the owner explicitly approves activation.
