import json
import urllib.parse
import urllib.request
import os

def read_webhose_key():
    webhose_api_key = None

    if os.path.isfile('search.key'):
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    else:
        with open('../search.key', 'r') as f:
            webhose_api_key = f.readline().strip()

    return webhose_api_key

def run_query(search_terms, size=10):
    webhose_api_key = read_webhose_key()
    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    query_string = urllib.parse.quote(search_terms)
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string,
                    size=size
    )

    results=[]

    try:
        print(search_url)
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        #response = urllib2.urlopen(search_url).read()
        print(8)
        json_response = json.loads(response)
        print(7)


        for post in json_response['posts']:
            results.append({'title':post['title'],
                            'link':post['url'],
                            'summary':post['text'][:200]})

    except:
        print('Error when querying the Webhose API')

    return results

if __name__=='__main__':
    search_term = input('searchterm:\n')
    results = run_query(search_term)
    for result in results:
        print(result['title'],result['link'],result['summary'])
        print('\n')