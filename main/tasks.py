import markdown
from dmess.celery import app


@app.task
def markdown_convert(wiki_object):
    print(wiki_object)
    # wiki_object.text_html = markdown.markdown(wiki_object.text_markdown)
    # wiki_object.save()