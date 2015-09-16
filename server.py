from flask import Flask, render_template, redirect, url_for, request, send_file
from PIL import Image
from StringIO import StringIO
import imageGen

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home_page():
    method = request.method
    chatStr = request.form.get("chatStr")
    if method == "POST":
        chatImg = imageGen.parseChat(chatStr)
        return download_file(chatImg)
        # chatImg.save('chatImg.jpeg')
        # return send_file('chatImg.jpeg', as_attachment=True)
    return render_template("home.html")


# @app.route('/download')
def download_file(chatImg):
    if chatImg is not None:
        return serve_pil_image(chatImg)


def serve_pil_image(pil_image):
    img_io = StringIO()
    pil_image.save(img_io, 'JPEG', quality=80)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, attachment_filename="prettified_chat.jpeg")


if __name__ == "__main__":
    app.debug = True
    app.run()
