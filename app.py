from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

IMAGE_FOLDER = 'static/images'
ANNOTATION_FILE = 'annotations.txt'

image_list = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

@app.route('/')
@app.route('/<int:index>')
def index(index=0):
    index = max(0, min(index, len(image_list) - 1))
    image_name = image_list[index]
    return render_template_string(TEMPLATE, image_name=image_name, index=index, total=len(image_list))

@app.route('/annotate', methods=['POST'])
def annotate():
    image_name = request.form['image_name']
    with open(ANNOTATION_FILE, 'a') as f:
        f.write(image_name + '\n')
    return redirect(url_for('index', index=int(request.form['index'])))

TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>OCT Viewer</title>
    <style>
        body { font-family: Arial; text-align: center; background: #f5f5f5; }
        img { width: 100%; max-width: 1000px; margin: 10px auto; border: 1px solid #ccc; }
        .btn-row { display: flex; justify-content: center; gap: 15px; margin-top: 20px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
        h2 { margin-top: 30px; }
    </style>
</head>
<body>

<h2>{{ image_name }}</h2>
<img src="{{ url_for('static', filename='images/' + image_name) }}">

<div class="btn-row">
    <form method="get" action="{{ url_for('index', index=index - 1) }}">
        <button type="submit">⬅ Back</button>
    </form>

    <form method="post" action="{{ url_for('annotate') }}">
        <input type="hidden" name="image_name" value="{{ image_name }}">
        <input type="hidden" name="index" value="{{ index }}">
        <button type="submit">✅ Annotate</button>
    </form>

    <form method="get" action="{{ url_for('index', index=index + 1) }}">
        <button type="submit">➡ Forward</button>
    </form>
</div>

<script>
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight') {
            window.location.href = "{{ url_for('index', index=index + 1) }}";
        } else if (e.key === 'ArrowLeft') {
            window.location.href = "{{ url_for('index', index=index - 1) }}";
        } else if (e.key.toLowerCase() === 'a') {
            document.querySelector('form[action$="/annotate"]').submit();
        }
    });
</script>

</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)