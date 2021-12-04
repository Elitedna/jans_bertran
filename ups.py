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
    payload={}
    headers = {
      'Authorization': f'token {api_token}'
    }
    return requests.request("GET", url, headers=headers, data=payload).json()


def get_chart_num(id_, api_token):
    url = f"https://design.platoforms.com/api/v4/submission/{id_}/"
    payload={}
    headers = {
      'Authorization': f'token {api_token}',
      'Cookie': 'sessionid=7scn2ghwtqovr5co5yu087bioq4meul6'
    }
    return requests.request("GET", url, headers=headers, data=payload).json()['submit_data']


def chart_num(submit_data):
    for i, v in enumerate(submit_data):
        if v['label'] == 'Chart Number':
            return v['value']


if __name__ == '__main__':

    FORM_ID = 'frht1kq7733'
    submissions = grab_submissions(FORM_ID, plato_token)
    print('Getting the last 75 forms submissions')
    submissions = pd.DataFrame(submissions['submissions'])
    submissions = submissions[['id', 'submit_date', 'submit_form_url']]
    for i in submissions.index:
        print(i)
        submissions.loc[i, 'chart_num'] = (chart_num(get_chart_num(submissions.loc[i, "id"],plato_token)))
    today = date.today().strftime('%Y-%m-%d')
    print('Look for the file ' + today + '_UPS.xlsx')
    submissions.to_excel(today + '_UPS.xlsx')