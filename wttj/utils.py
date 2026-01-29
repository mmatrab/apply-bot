import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup

CRED_FILE_NAME = 'cred.json'
APPLIED_JOBS_LIST_FILE_NAME = 'applied_jobs_list.json'
def get_creds():
    with open(CRED_FILE_NAME, mode='r') as f:
        cred = json.load(f)

    return cred


def get_jobs_list(html):
    soup = BeautifulSoup(html, 'lxml')
    jobs_soup = soup.select('ol')
    jobs_list = []

    base_url = 'https://www.welcometothejungle.com/'

    for j in jobs_soup:
        link = j.select_one('a[class="sc-6i2fyx-0 gIvJqh"]')['href']
        company = j.select_one('span.sc-ERObt.gTCEVh.sc-6i2fyx-3.eijbZE.wui-text').text
        heading = j.select_one('.sc-bXCLTC.hlqow9-0.helNZg').text
        location = j.select_one('.sc-68sumg-0.gvkFZv').text
        tags = j.select('div[class="sc-bXCLTC kpWcuw"][role="listitem"]')
        tags_text = [t.text for t in tags]
        info = {
            'link': urljoin(base_url, link),
            'company': company,
            'heading': ' '.join(heading.split()),
            'tags': tags_text
        }

        jobs_list.append(info)

    return jobs_list


def get_job_description(html):
    soup = BeautifulSoup(html, 'lxml')
    about_section = soup.select_one('#about-section')
    # description_section = soup.select_one('#description-section')
    profile_section = soup.select_one('#profile-section')
    recruitment_section = soup.select_one('#recruitment-section')

    all_sections = [about_section, profile_section, recruitment_section]
    complete_text = ''

    for section in all_sections:
        if section is not None:

            try:
                heading = section.select_one('h2').text
            except Exception as e:
                print(e)
                heading = ''

            try:
                paragraphs = section.select('p')
                paragraphs_text = '\n'.join([p.text for p in paragraphs])
            except:
                paragraphs_text = ''

            text = heading + '\n' + paragraphs_text
            complete_text = complete_text + text + '\n\n'

    return complete_text


class AppliedJobsList:
    def __init__(self):
        with open(APPLIED_JOBS_LIST_FILE_NAME, mode='r') as f:
            self.jobs_list = json.load(f)


    def is_applied(self, job_obj):
        applied = False
        for j in self.jobs_list:
            if j['company'] + j['heading'] == job_obj['company'] + job_obj['heading']:
                applied = True
                break

        return applied


    def update_applied_list(self, job_obj):
        self.jobs_list.append(job_obj)
        with open(APPLIED_JOBS_LIST_FILE_NAME, mode='w') as f:
            json.dump(self.jobs_list, f, indent=4)