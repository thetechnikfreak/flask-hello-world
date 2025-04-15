from flask import Flask, send_file
import feedparser
from pptx import Presentation
from pptx.util import Inches
import requests
from io import BytesIO
import tempfile
import os

app = Flask(__name__)

FEED_URL = "http://mamoba-events.rf.gd/feed.php"

@app.route('/generate-pptx')
def generate_pptx():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return "Keine Einträge im Feed gefunden.", 404

    prs = Presentation()

    for entry in feed.entries:
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Leere Folie

        # Daten kürzen
        title = entry.get("title", "")[:30]
        desc = entry.get("summary", "")[:143]

        # Text
        txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1.5))
        tf = txBox.text_frame
        tf.text = title + "\n" + desc

        # Bild laden
        img_url = None
        if 'enclosures' in entry and entry.enclosures:
            img_url = entry.enclosures[0].get("href")

        if img_url:
            try:
                img_data = requests.get(img_url).content
                img_stream = BytesIO(img_data)
                slide.shapes.add_picture(img_stream, Inches(3), Inches(2), Inches(4), Inches(4))
            except Exception as e:
                print(f"Fehler beim Bildabruf: {e}")

    # Datei speichern
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    prs.save(tmp.name)
    return send_file(tmp.name, as_attachment=True, download_name="mamoba-veranstaltungen.pptx")

@app.route('/')
def home():
    return '✅ PPTX-Generator bereit! Nutze: /generate-pptx'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
