# Bloodline Voice Conversation Acceptance Tests

Run these scenarios in a LiveKit test room before purchasing a SIP number.
Record outcomes manually; none of these tests have been executed yet.

| ID | Caller scenario | Expected agent behavior |
| --- | --- | --- |
| V01 | "I need a couch and mattress removed." | Identify service, ask for address, quantity/access, name and callback number |
| V02 | "Can you come Friday at 2?" | Capture preferred time; clearly state appointment is not confirmed |
| V03 | "Can I text you pictures?" | Ask for photo follow-up and SMS consent; never claim a text was sent |
| V04 | "How much will it cost?" | Request job details, avoid a binding quote |
| V05 | "Are you open on Sunday?" | Say operating hours are not yet confirmed |
| V06 | "I live outside Colorado Springs." | Ask for address; do not promise service-area coverage |
| V07 | "Can you transfer me to Mike?" | Offer a callback, not a nonexistent live transfer |
| V08 | Caller interrupts or pauses | Recover naturally without inventing answers |
| V09 | Caller refuses SMS | Respect preference; proceed without SMS |
| V10 | Caller ends conversation | Confirm key details and callback request, close politely |

Pass criteria: coherent conversation, correct lead capture through take_message,
no false claims about booking/SMS/price/hours, and successful tool outcome.
This is a test specification, not evidence of runtime success.
