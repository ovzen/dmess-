"""
celery-задачи приложения
"""

import os

import markdown
import gitlab
from django.conf import settings

from admin.models import GitlabMetrics
from dmess.celery import app
from main.models import WikiPage


@app.task()
def markdown_convert(**kwargs):
    """
    Отложенное задание для преобразования markdown-поля в модели в html-код.

    Берём markdown-текст, преобразовываем в html и записываем обратно в модель
    :param kwargs: словарь с параметрами. Должен содержать ключ id (primary key в модели WikiPage)
    """
    wiki_object = WikiPage.objects.get(id=kwargs['id'])
    text_html = markdown.markdown(wiki_object.text_markdown)
    if wiki_object.text_html != text_html:
        wiki_object.text_html = text_html
        wiki_object.save()


@app.task()
def gitlab_metrics_fetch():
    """
    Регулярное задание, забирающее последнии данные о репозитории проекта с Gitlab.

    Берем данные, c помощью api, и записываем в модель GitlabMetrics в формате key: value
    :return: None
    """
    gl = gitlab.Gitlab(
        settings.GITLAB_DOMAIN_URL, private_token=os.environ['GITLAB_PRIVATE_TOKEN']
    )
    project = gl.projects.get(settings.GITLAB_PROJECT_ID)

    metrics = {
        GitlabMetrics.CURRENT_BRANCHES: project.branches.list(as_list=False).total,
        GitlabMetrics.COMMITS: project.commits.list(as_list=False).total,
        GitlabMetrics.OPENED_ISSUES: project.issues.list(
            state='opened', as_list=False
        ).total,
        GitlabMetrics.OPENED_MERGE_REQUESTS: project.mergerequests.list(
            state='opened', as_list=False
        ).total,
    }
    for key, value in metrics.items():
        GitlabMetrics(key=key, value=value).save()
