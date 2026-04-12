
# AI Review Response Agent

An intelligent AI-powered SaaS platform that automates customer review management for businesses by generating smart, multilingual, adaptive responses to Google Business reviews.

---

## 🚀 Features

### Core AI Capabilities
- Live Google Business review fetching via Zernio API
- AI-generated contextual review responses
- Sentiment classification (positive / negative)
- Dynamic language style detection:
  - English
  - Hinglish
  - Telugu-English
  - Hindi-English
  - Mixed colloquial
- Colloquial Romanized multilingual reply generation

---

### Automation Modes
#### 1. Approval Mode
AI drafts responses → owner approves manually

#### 2. Smart Auto Mode
- Positive reviews auto-posted automatically
- Negative reviews sent for manual approval

---

### Dashboard Features
- Live review dashboard
- Approve responses
- Edit AI-generated replies
- Sync Reviews button for live refresh
- Dynamic automation mode display

---

### Memory Engine
AI learns owner preferences from edits:
- Preferred tone
- Emoji usage
- Reply length style
- Preferred language style

Future replies adapt automatically.

---

## 🏗 Architecture Overview

```plaintext
Google Reviews → Zernio API → Fetch Engine
                         ↓
                Sentiment Classifier
                         ↓
             Language Style Detector
                         ↓
                Memory Preference Engine
                         ↓
               Response Generation Engine
                         ↓
       Approval / Smart Auto Decision Layer
                         ↓
          Firestore + Google Review Posting
````

---

## 📁 Project Structure

```plaintext
app/
│
├── agent/
│   └── workflow.py
│
├── reviews/
│   ├── fetch_live.py
│   ├── classify.py
│   ├── detect_language.py
│   ├── respond.py
│   ├── reply_live.py
│   └── memory_engine.py
│
├── templates/
│   ├── dashboard.html
│   ├── edit_review.html
│   └── settings.html
│
├── firebase_config.py
├── main.py
├── test_live.py
└── init_business_profile.py
```

---

## ⚙️ Setup Instructions

---

### 1. Clone Project

```bash
git clone <your_repo_url>
cd ai-review-agent
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create `.env`

```env
ZERNIO_API_KEY=your_zernio_api_key
GROQ_API_KEY=your_groq_api_key
```

---

### 4. Firebase Setup

Add Firebase service account JSON:

```plaintext
firebase_key.json
```

Configure in:

```python
firebase_config.py
```

---

### 5. Initialize Business Profile

Run once:

```bash
python init_business_profile.py
```

---

## ▶️ Running Application

Start server:

```bash
uvicorn app.main:app --reload
```

Open:

```plaintext
http://localhost:8000
```

---

## 🔄 Sync Reviews

Instead of running scripts manually:

Use dashboard button:

```plaintext
Sync Reviews
```

This:

* fetches latest reviews
* generates AI responses
* updates Firestore
* auto-posts if enabled

---

## 🧠 Memory Engine Workflow

1. Owner edits AI response
2. Edit history saved
3. Memory engine analyzes patterns
4. Business memory profile updated
5. Future responses adapt automatically

---

## 🌍 Language Intelligence Examples

### Review:

```plaintext
Mee place chala bagundi andi!
```

### AI Reply:

```plaintext
Thanks andi! Mee support ki chala santosham 😊
```

---

### Review:

```plaintext
Food bahut tasty tha!
```

### AI Reply:

```plaintext
Bahut shukriya! Phir zaroor aaiyega 😊
```

---

## 🔥 Future Enhancements

* Analytics insights dashboard
* Trend detection engine
* Smart auto preview simulator
* Multi-location business support
* Scheduled reply windows

---

## 🛡 Tech Stack

* FastAPI
* Firebase Firestore
* Groq LLM API
* Google Business API via Zernio
* Tailwind CSS
* Python

---

## 👩‍💻 Author

Built by Lalasa V

---

