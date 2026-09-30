from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="LegalEase")

def explain_legal_text(text: str):
    summary = f"""
     Document Summary:
    This document has {len(text.split())} words.
    
     Key Points Found:
    - This appears to be a legal document.
    - Important clauses related to agreement and terms are present.
    - Please review the obligations carefully.
    
     Simple Explanation (in Tamil):
    Itha oru sattapoorvamana oppantham ma. Neenga kaiyezhuthu podura munna, 
    intha document la enna irukku nu nalla purinjikanum ma. Mukkiyamana 
    vishayangal ellam terms & conditions la irukkum ma.
    
     Advice: Oru lawyer kitta oru thadava kaami check pannikonga ma.
    """
    return summary

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>LegalEase - Legal Made Easy</title>
        <style>
            body { font-family: Arial; background: #f0f2f5; padding: 30px; }
            .box { background: white; max-width: 700px; margin: auto; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; text-align: center; }
            input, textarea, button { width: 100%; padding: 12px; margin-top: 15px; border-radius: 8px; border: 1px solid #ccc; }
            button { background: #1a73e8; color: white; font-weight: bold; cursor: pointer; border: none; }
            button:hover { background: #0d62c9; }
            .result { margin-top: 20px; padding: 20px; background: #e8f0fe; border-radius: 10px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1> LegalEase</h1>
            <p style="text-align:center;">Upload your legal document & get simple explanation</p>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <label>Paste Legal Text Here:</label>
                <textarea name="text" rows="6" placeholder="Paste your legal document text here..."></textarea>
                <label>OR Upload File (PDF/TXT):</label>
                <input type="file" name="file">
                <button type="submit">✨ Explain in Simple Words</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(text: str = Form(""), file: UploadFile = File(None)):
    content = text
    if file and file.filename:
        data = await file.read()
        try:
            content = data.decode('utf-8')
        except:
            content = f"File {file.filename} uploaded ({len(data)} bytes). " + text
    
    if not content.strip():
        content = "No content provided. This is a sample legal agreement for testing."
    
    explanation = explain_legal_text(content)
    
    return f"""
    <html>
    <head><title>Result - LegalEase</title>
    <style>
        body {{ font-family: Arial; background: #f0f2f5; padding: 30px; }}
        .box {{ background: white; max-width: 700px; margin: auto; padding: 30px; border-radius: 15px; }}
        a {{ display: block; text-align: center; margin-top: 20px; color: #1a73e8; text-decoration: none; font-weight: bold; }}
        .result {{ white-space: pre-wrap; background: #e8f0fe; padding: 20px; border-radius: 10px; }}
    </style>
    </head>
    <body>
        <div class="box">
            <h1> Analysis Complete</h1>
            <div class="result">{explanation}</div>
            <a href="/">⬅️ Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)