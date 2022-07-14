#!/usr/bin/python3
# Track views over time


import sys
import time
import json
from stackapi import StackAPI

def query_user(site, user):
    "Get all questions and answers for user:"
    api = StackAPI(site)
    questions = api.fetch('users/{ids}/questions', ids=[user], fromdate=0)
    answers = api.fetch('users/{ids}/answers', ids=[user], fromdate=0)
    return [str(item['question_id']) for item in questions['items'] + answers['items']]


def parse_url(url):
    "Given a Question url, fetch the site name and question number"
    if url.startswith('http'):
        site = url.split('/')[2].split('.')[0]
        number = url.split('/')[4]
    else:
        # Legacy site:user_id format
        site, number = url.split('.')
    return site, number



def fetch_views(site, questions):
    "Given a site name and list of questions, fetch the view count"
    api = StackAPI(site)
    result = api.fetch('questions/{ids}', ids=questions)
    items = result.pop('items')
    if result['backoff']:
        print("Warning: Backoff triggered")
        print(result)
    if result['quota_remaining'] <= 64:
        print("Low quota:", result['quota_remaining'])
        print(result)
    return {item['question_id']:item['view_count'] for item in items}


def main():
    # Process each url looking for site names and question ids
    data = {}
    for url in sys.argv[1:]:
        site, number = parse_url(url)
        if site not in data:
            data[site] = set()
        if '/questions/' in url:
            data[site].add(number)
        else:
            print("Querying", site, 'for user:', number)
            questions = query_user(site, number)
            time.sleep(1)
            data[site].update(questions)

    # Process accumulated questions
    out = {}
    for site, questions in data.items():
        if questions:
            print("Querying", site, 'for question ids:', ', '.join(questions))
            result = fetch_views(site, list(questions))
            out[site] = result
            time.sleep(1)

    with open('se.views.out', 'a') as f:
        json.dump([int(time.time()), out], f)
        f.write('\n')

if __name__ == "__main__":
    main()
