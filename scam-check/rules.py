import re

# (id, weight, regex, English label, Hindi label)
RULES = [
 ("guaranteed", 4, r"guarantee[d]?\s+(return|profit)|assured\s+(return|profit)|risk[- ]?free|100%\s*(profit|return)|गारंटी|पक्का\s*(मुनाफ़ा|मुनाफा|रिटर्न)|बिना\s*जोखिम",
  "Promises guaranteed or risk-free returns", "गारंटीड या बिना जोखिम मुनाफ़े का वादा"),
 ("multiply", 3, r"double\s+(your\s+)?money|triple|\d+\s*x\s*(return|profit)|daily\s+(profit|income)|(\d+)\s*%\s*(per|a|every)\s*(day|week)|पैसा\s*दोगुना|दुगना|रोज़\s*कमाई|रोज\s*कमाई",
  "Unrealistic high returns (e.g. doubling money, daily profit)", "अवास्तविक रिटर्न (जैसे पैसा दोगुना, रोज़ मुनाफ़ा)"),
 ("urgency", 2, r"limited\s+(slots|seats|time)|act\s+now|hurry|last\s+chance|today\s+only|join\s+(now|immediately)|जल्दी|आज\s*ही|सीमित\s*(सीटें|समय)",
  "Creates urgency or pressure", "जल्दबाज़ी का दबाव बनाता है"),
 ("group", 2, r"telegram|whatsapp\s+group|join\s+(our|my)\s+(group|channel)|vip\s+(group|channel)|टेलीग्राम|व्हाट्सएप\s*ग्रुप",
  "Pushes you to a private Telegram/WhatsApp group", "आपको प्राइवेट टेलीग्राम/व्हाट्सएप ग्रुप में बुलाता है"),
 ("otp", 5, r"\botp\b|\bupi\s*pin\b|\bcvv\b|share\s+(your\s+)?(password|pin)|ओटीपी|यूपीआई\s*पिन",
  "Asks for OTP, PIN or password", "OTP, PIN या पासवर्ड माँगता है"),
 ("tips", 3, r"sure\s*shot|insider\s+tip|operator\s+(call|tip)|jackpot\s+(stock|tip)|multibagger\s+tip|stock\s+tips?|सटीक\s*टिप",
  "Offers 'sure-shot' stock tips", "'पक्की' स्टॉक टिप का दावा"),
 ("unreg", 3, r"(sebi|नियामक)[\s-]*(approved|registered)\s+(by\s+us|tip)|fake\s+sebi|rbi\s+approved\s+app|ipo\s+allotment\s+guaranteed|guaranteed\s+ipo|ऑलोटमेंट\s*गारंटी",
  "Suspicious regulatory/approval claims", "संदिग्ध SEBI/नियामक अनुमोदन के दावे"),
 ("pay", 3, r"(pay|send|transfer|deposit)\s+(a\s+)?(registration|joining|processing)\s+fee|pay\s+first|advance\s+(fee|payment)|रजिस्ट्रेशन\s*फ़ीस|पहले\s*पैसे",
  "Asks for upfront fee or deposit", "पहले फ़ीस या जमा राशि माँगता है"),
 ("link", 2, r"bit\.ly|tinyurl|\.apk\b|download\s+(this\s+)?app|apk",
  "Contains shortened links or unofficial app downloads", "छोटे लिंक या अनौपचारिक ऐप डाउनलोड"),
]

MASKS = [
 (r"\b[6-9]\d{9}\b", "[PHONE]"),
 (r"\b\d{12}\b", "[ID-NUMBER]"),
 (r"\b\d{9,18}\b", "[ACCOUNT]"),
 (r"[\w.\-]+@[\w\-]+", "[EMAIL/UPI]"),
]

def mask(text):
    for p, r in MASKS:
        text = re.sub(p, r, text)
    return text

def analyze(text):
    flags, score = [], 0
    for rid, w, pat, en, hi in RULES:
        if re.search(pat, text, re.I):
            flags.append({"id": rid, "weight": w, "en": en, "hi": hi})
            score += w
    level = "High" if score >= 6 else "Medium" if score >= 3 else "Low"
    return level, score, flags
