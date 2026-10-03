# Scam Check (SANGYAN hackathon prototype, Tracks A + E)
Paste a suspicious investment message and get a plain-language risk level (English/Hindi), the red flags found, a read-aloud explanation and official next steps (SEBI SCORES, 1930, cybercrime.gov.in).

## Run
    pip install -r requirements.txt
    streamlit run app.py
Optional AI explanation: `export ANTHROPIC_API_KEY=...` (works without it, using rule-based explanations).

## Architecture
- `rules.py`: regex rule engine (English + Hindi red flags, weighted score) and PII masking (phone, account, ID, UPI/email).
- `app.py`: Streamlit UI, optional LLM explanation (Claude API, masked text only), browser Web Speech API for read-aloud.

## Guardrails
No stock tips, predictions, product promotion or monetisation. No OTP/SMS collection. Nothing stored. Uncertainty shown on every result.

## Third-party components
Streamlit (Apache-2.0), Anthropic API (optional), browser Web Speech API.

## Deploy
Push to GitHub, then deploy on Streamlit Community Cloud (add ANTHROPIC_API_KEY as a secret).
