import requests
import json
import pandas as pd
from datetime import date, timedelta
from secret import plato_token


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This module is was created by our first software developer intern -- Jans_Bertran --
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def grab_submissions(form_id, api_token):
    url = f"https://design.platoforms.com/api/v4/form/{form_id}/submissions/?resultsperpage=75"
    payload = {}
    headers = {
        'Authorization': f'token {api_token}'
    }
    return requests.request("GET", url, headers=headers, data=payload).json()


def get_chart_num(id_, api_token):
    url = f"https://design.platoforms.com/api/v4/submission/{id_}/"
    payload = {}
    headers = {
        'Authorization': f'token {api_token}',
        'Cookie': 'sessionid=7scn2ghwtqovr5co5yu087bioq4meul6'
    }
    return requests.request("GET", url, headers=headers, data=payload).json()['submit_data']


def chart_num(submit_data):
    for i, v in enumerate(submit_data):
        if v['label'] == 'Chart Number':
            return v['value']


def get_url(sub_id, plato_form):

    url = f"https://design.platoforms.com/api/v4/sharing/submission/editor/{sub_id}/"

    payload={}
    headers = {
      'Authorization': f'token {plato_form}',
      'Cookie': 'csrftoken=BUH7q5rsGr8rVA8XtQ9evzPldZZP0teyofBX265l8mOx5Au3jTj4hWu9FhuoQ3X0'
        }
    return requests.request("GET", url, headers=headers, data=payload).json()

if __name__ == '__main__':

    FORM_ID = 'frht1kq7733'
    submissions = grab_submissions(FORM_ID, plato_token)
    print('Getting the last 75 forms submissions')
    submissions = pd.DataFrame(submissions['submissions'])
    submissions = submissions[['id', 'submit_date']]
    for i in submissions.index:
        print(i)
        submissions.loc[i, 'chart_num'] = (chart_num(get_chart_num(submissions.loc[i, "id"], plato_token)))
        submissions.loc[i, 'url'] = get_url(i, plato_token)['sharingUrl']

    today = date.today().strftime('%Y-%m-%d')
    print('Look for the file ' + today + '_UPS.xlsx')
    submissions.to_excel(today + '_UPS.xlsx')
