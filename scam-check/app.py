import os, json
import streamlit as st
import streamlit.components.v1 as components
from rules import analyze, mask

st.set_page_config(page_title="Scam Check", page_icon="🛡️", layout="centered")

T = {
 "en": dict(title="🛡️ Scam Check", sub="Paste a suspicious investment message. We'll flag warning signs in plain language.",
   box="Paste the message here", btn="Check message", sample="Try a sample", lvl={"Low":"Low risk","Medium":"Medium risk","High":"High risk"},
   flags="Warning signs found", none="No common warning signs found.", unc="⚠️ This is an automated check, not a verdict. A 'low risk' result does not mean a message is safe.",
   steps="What to do next", read="🔊 Read aloud", expl="Explanation", masked="Text sent for analysis (personal details masked)",
   next=["Never share OTP, UPI PIN or passwords with anyone.",
         "Verify any advisor or broker on the official SEBI registered-intermediaries search (sebi.gov.in) before paying.",
         "Do not pay 'joining' or 'registration' fees to unknown people.",
         "If you lost money, call 1930 or report at cybercrime.gov.in; investor complaints can be filed on SEBI SCORES (scores.sebi.gov.in)."],
   priv="Privacy: nothing is stored. Phone, account and UPI details are masked before any AI processing.", lang="en-IN"),
 "hi": dict(title="🛡️ स्कैम चेक", sub="कोई भी संदिग्ध निवेश संदेश यहाँ डालें। हम आसान भाषा में चेतावनी के संकेत बताएँगे।",
   box="संदेश यहाँ पेस्ट करें", btn="संदेश जाँचें", sample="उदाहरण चुनें", lvl={"Low":"कम जोखिम","Medium":"मध्यम जोखिम","High":"उच्च जोखिम"},
   flags="मिले चेतावनी संकेत", none="कोई आम चेतावनी संकेत नहीं मिला।", unc="⚠️ यह स्वचालित जाँच है, अंतिम फ़ैसला नहीं। 'कम जोखिम' का मतलब यह नहीं कि संदेश सुरक्षित है।",
   steps="आगे क्या करें", read="🔊 सुनें", expl="स्पष्टीकरण", masked="विश्लेषण के लिए भेजा गया पाठ (निजी जानकारी छिपाई गई)",
   next=["OTP, UPI पिन या पासवर्ड किसी को न बताएँ।",
         "पैसे देने से पहले SEBI की आधिकारिक वेबसाइट (sebi.gov.in) पर सलाहकार/ब्रोकर का रजिस्ट्रेशन जाँचें।",
         "अनजान लोगों को 'जॉइनिंग' या 'रजिस्ट्रेशन' फ़ीस न दें।",
         "पैसा खोया हो तो 1930 पर कॉल करें या cybercrime.gov.in पर शिकायत करें; निवेशक शिकायत SEBI SCORES (scores.sebi.gov.in) पर।"],
   priv="गोपनीयता: कुछ भी सहेजा नहीं जाता। फ़ोन, खाता और UPI विवरण AI को भेजने से पहले छिपा दिए जाते हैं।", lang="hi-IN"),
}
SAMPLES = {
 "—": "",
 "Scam (English)": "Join our VIP Telegram group! Guaranteed 30% profit daily, sure shot stock tips from insider. Limited slots, pay registration fee 2000 to 9876543210@upi today only.",
 "Scam (Hindi)": "बधाई हो! हमारे व्हाट्सएप ग्रुप में आज ही जुड़ें। पैसा दोगुना, पक्का मुनाफ़ा गारंटी। जल्दी करें, सीमित सीटें। अपना ओटीपी शेयर करें।",
 "Harmless": "Hi, your mutual fund SIP of Rs 2000 was processed on 5th. View statement on the official app. Mutual fund investments are subject to market risks.",
}

lang = "hi" if st.sidebar.radio("Language / भाषा", ["English", "हिन्दी"]) == "हिन्दी" else "en"
t = T[lang]
st.title(t["title"]); st.caption(t["sub"])
choice = st.selectbox(t["sample"], list(SAMPLES))
text = st.text_area(t["box"], value=SAMPLES[choice], height=160)

def llm_explain(masked, level, flags, lang):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        lname = "Hindi" if lang == "hi" else "simple English"
        prompt = (f"A user received this message (personal data masked):\n\"\"\"{masked}\"\"\"\n"
                  f"Rule-based check: {level} risk; flags: {[f['en'] for f in flags]}.\n"
                  f"In {lname}, in at most 4 short sentences for a first-time investor, explain why this may or may not be a scam. "
                  "State uncertainty clearly. Never give stock tips, buy/sell advice, predictions, or recommend any product or broker.")
        r = c.messages.create(model="claude-sonnet-4-6", max_tokens=300, messages=[{"role": "user", "content": prompt}])
        return r.content[0].text
    except Exception:
        return None

if st.button(t["btn"], type="primary") and text.strip():
    masked = mask(text)
    level, score, flags = analyze(masked)
    color = {"Low": "green", "Medium": "orange", "High": "red"}[level]
    st.markdown(f"## :{color}[{t['lvl'][level]}]")
    st.progress(min(score, 10) / 10)
    st.subheader(t["flags"])
    if flags:
        for f in flags: st.markdown(f"- {f[lang]}")
    else:
        st.write(t["none"])
    expl = llm_explain(masked, level, flags, lang)
    if not expl:
        expl = (" ".join(f[lang] + "." for f in flags) if flags else t["none"])
    st.subheader(t["expl"]); st.write(expl)
    st.warning(t["unc"])
    spoken = f"{t['lvl'][level]}. {expl}"
    components.html(f"""<button style="padding:8px 14px;font-size:16px" onclick="
      const u=new SpeechSynthesisUtterance({json.dumps(spoken)});u.lang='{t['lang']}';
      speechSynthesis.cancel();speechSynthesis.speak(u);">{t['read']}</button>""", height=50)
    st.subheader(t["steps"])
    for s in t["next"]: st.markdown(f"- {s}")
    with st.expander(t["masked"]): st.code(masked)
st.divider(); st.caption(t["priv"])
st.caption("Scam Check does not give stock tips, predictions or product recommendations.")
