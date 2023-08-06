from typing import List

PATTERNS = [
    {
        'group': 'tracingHeaders',
        'match': lambda name:
        name == 'x-request-id' or name == 'x-ot-span-context'
    },
    {
        'group': 'tracingHeaders',
        'match': lambda name: name.startswith('x-b3-')
    },
    {
        'group': 'miscHeaders',
        'match': lambda name: name.startswith('x-forwarded-')
    }]


def process(headers: List):
    result = {
        # str[]
        'tracingHeaders': [],
        # str[]}
        'extrasHeaders': [],
        # str[]
        'miscHeaders': []
    }

    # 排除所有不是以'x-'开头的key
    for header in filter(lambda h: h.startswith('x-'), headers):
        # 排除满足$excludes集合中条件的
        pattern = next(filter(lambda p: p.match(header), PATTERNS), None)
        group = pattern['group'] if pattern else 'extrasHeaders'
        result[group].append(header)
    return result
