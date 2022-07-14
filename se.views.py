#!/usr/bin/python3
# Track views over time


import sys
import time
import json
from stackapi import StackAPI


def query(name, user):
    "Get all questions and answers for user:"
    site = StackAPI(name)
    questions = site.fetch('users/{ids}/questions', ids=[user], fromdate=0)
    answers = site.fetch('users/{ids}/answers', ids=[user], fromdate=0)
    question_ids = [item['question_id'] for item in questions['items'] + answers['items']]
    result = site.fetch('questions/{ids}', ids=question_ids)
    return {item['question_id']:item['view_count'] for item in result['items']}


def main():
    site_names = {name: uid for name, uid in zip(*[iter(sys.argv[1:])]*2)}
    out = {}
    for site_name, user in site_names.items():
        # print("Querying:", site_name, 'for user', user)
        out[site_name] = query(site_name, int(user))
        time.sleep(1)

    with open('se.views.out', 'a') as f:
        json.dump([int(time.time()), out], f)
        f.write('\n')


if __name__ == "__main__":
    main()
