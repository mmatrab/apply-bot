from controller import Controller
from utils import get_creds, AppliedJobsList
from selenium.webdriver.common.by import By
from time import sleep

creds = get_creds()
applied_jobs = AppliedJobsList()

a = Controller(creds['email'], creds['password'], creds['job_list_url'])
a.go_to_website()
a.accept_cookies()
a.login()
a.go_to_job_list()
a.remove_location_filter()
page_count = a.get_page_count()

for page_num in range(1, page_count+1):
    jobs_list = a.get_jobs_list()

    for job in jobs_list:
        if not applied_jobs.is_applied(job):
            a.apply_job(job)
            applied_jobs.update_applied_list(job)
        else:
            print(f'job already applied: {job["link"]}')

    # Find the <ul> element by class name
    ul_element = a.driver.find_element(By.CLASS_NAME, 'sc-fUkmAC.fTXNVO')

    # Find the last <li> element inside the <ul> element
    last_li_element = ul_element.find_elements(By.TAG_NAME, 'li')[-1]

    # Find the link inside the last <li> element and click on it
    link_inside_last_li = last_li_element.find_element(By.TAG_NAME, 'a')
    link_inside_last_li.click()

    sleep(7)





