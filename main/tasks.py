"""tasks.py - celery-задачи проекта"""

import markdown
import requests

from admin.models import GitlabMetrics
from dmess.celery import app
from main.models import WikiPage


@app.task()
def markdown_convert(**kwargs):
    """Отложенное задание для преобразования markdown-поля в модели в html-код.

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
    results = {
        'openedIssues': 0,
        'openedMergeRequests': 0,
        'currentBranches': 0,
        'commits': 0,
    }
    gitlab_api_url = 'https://gitlab.informatics.ru/api/v4/projects/1932'
    gitlab_metrics_urls = {
        'openedIssues': gitlab_api_url + '/issues_statistics',
        'openedMergeRequests': gitlab_api_url + '/merge_requests?state=opened&per_page=1',
        'currentBranches': gitlab_api_url + '/repository/branches?per_page=1',
        'commits': gitlab_api_url + '/repository/commits?per_page=1'
    }
    params = {
        'private_token': 'q_CTeYuyhchyiXxiRVBS'
    }
    results['openedIssues'] = \
        requests.get(gitlab_metrics_urls['openedIssues'], params=params).json()['statistics']['counts']['opened']
    results['openedMergeRequests'] = requests.get(gitlab_metrics_urls['openedMergeRequests'], params=params).headers['X-Total']
    results['currentBranches'] = requests.get(gitlab_metrics_urls['currentBranches'], params=params).headers['X-Total']
    results['commits'] = requests.get(gitlab_metrics_urls['commits'], params=params).headers['X-Total']
    item = GitlabMetrics(opened_issues=results['openedIssues'], opened_merge_requests=results['openedMergeRequests'],
                         current_branches=results['currentBranches'], commits=results['commits'])
    item.save()
    return None
