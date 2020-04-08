import markdown
from dmess.celery import app


@app.task(serializer='json')
def markdown_convert(*args, **kwargs):
    print(args[0], args[1])
    # wiki_object.text_html = markdown.markdown(wiki_object.text_markdown)
    # wiki_object.save()