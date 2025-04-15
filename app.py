from flask import Flask, send_file, request
import feedparser
from pptx import Presentation
from pptx.util import Inches
import requests
from io import BytesIO
import tempfile

app = Flask(__name__)

@app.route('/generate-pptx')
def generate_pptx():
    feed_url = request.args.get('url')
    if not feed_url:
        return "Bitte ?url= angeben", 400

    feed = feedparser.parse(feed_url)
    prs = Presentation()

    for entry in feed.entries:
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Leer
        title = entry.title
        desc = entry.description
        img_url = None

        # Bild suchen (enclosure oder im description-HTML)
        if 'enclosures' in entry and entry.enclosures:
            img_url = entry.enclosures[0].href

        # Textbox
        txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        tf = txBox.text_frame
        tf.text = title + "\n" + desc

        # Bild hinzufügen
        if img_url:
            try:
                img_data = requests.get(img_url).content
                img_stream = BytesIO(img_data)
                slide.shapes.add_picture(img_stream, Inches(2), Inches(2), Inches(4), Inches(4))
            except Exception as e:
                print(f"Fehler beim Bild: {e}")

    # Temporäre Datei
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
    prs.save(temp.name)
    return send_file(temp.name, as_attachment=True, download_name="veranstaltungen.pptx")

@app.route('/')
def hello():
    return 'Nutze /generate-pptx?url=https://...'

