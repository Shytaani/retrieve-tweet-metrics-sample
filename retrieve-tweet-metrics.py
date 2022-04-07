from requests_oauthlib import oauth1_auth
import settings
import requests
import http
import csv


def json_to_csv(json, headers, row):
    for k, v in json.items():
        if type(v) is dict:
            json_to_csv(v, headers, row)
        else:
            if k not in headers:
                headers.append(k)
            row[k] = v
    return headers, row


params = {
    'query': f'from:{settings.user_name}',
    'tweet.fields': settings.tweets_fields
}

headers_oauth1 = oauth1_auth.OAuth1(settings.consumer_key, settings.consumer_key_secret, settings.access_token,
                                    settings.access_token_secret)

response = requests.get(settings.url, params, auth=headers_oauth1)

if response.status_code != http.HTTPStatus.OK:
    raise Exception(response.status_code, response.text)
else:
    result = response.json()['data']
    csv_headers = ['id', 'text']
    csv_rows = []
    for record in result:
        csv_row = {}
        csv_headers, csv_row = json_to_csv(record, csv_headers, csv_row)
        csv_rows.append(csv_row)

    with open('out/tweet-metrics.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for r in csv_rows:
            writer.writerow(r)
