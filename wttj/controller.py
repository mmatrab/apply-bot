from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import sleep
from utils import get_jobs_list, get_job_description
from chat import get_cover_letter, get_answer
import traceback



# LOGIN SELECTORS
sign_in_menu_btn_selector = (By.CSS_SELECTOR, 'button[data-testid="header-user-button-login"]')
email_selector = (By.CSS_SELECTOR, 'input#email_login')
password_selector = (By.CSS_SELECTOR, 'input#password')
sign_in_btn_selector = (By.CSS_SELECTOR, 'button[data-testid="login-button-submit"]')
cookie_accept_btn_selector = (By.CSS_SELECTOR, 'button[id="axeptio_btn_acceptAll"]')

# selector to remove location filter
location_cross_selector = (By.CSS_SELECTOR, 'div[class="sc-ccVCaX vawhe1-1 bsbneF"] button')
jobs_result_selector = (By.CSS_SELECTOR, '[data-testid="search-results"]')

# apply button on job page that opens up application form pop up
apply_btn_selector = (By.CSS_SELECTOR, 'button[data-testid="job_sticky-button-apply"]')
job_text_selector = (By.CSS_SELECTOR, 'section[id="about-section"]')

# selectors for elements inside application form
cover_letter_selector = (By.CSS_SELECTOR, '[data-testid="apply-form-field-cover_letter"]')
questions_field_selector = (By.XPATH, "//legend[contains(text(), 'Quelques questions…')]/parent::node()")
checkbox1_selector = (By.CSS_SELECTOR, 'input[data-testid="apply-form-terms"]')
checkbox2_selector = (By.CSS_SELECTOR, 'input[data-testid="apply-form-consent"]')
submit_btn_selector = (By.CSS_SELECTOR, 'button[data-testid="apply-form-submit"]')

BROWSER_URL = 'http://browser:4444/wd/hub'

class Controller:

    def __init__(self, email, password, job_list_url):
        # initialize the chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        
        self.driver = webdriver.Remote(command_executor=BROWSER_URL, options=options)

        # save login details and job list url for accessing later
        self.email = email
        self.password = password
        self.job_list_url = job_list_url


    def go_to_website(self):
        """Goes to the base url and waits until the login button and cookie notice appears"""
        print('Going to the website...')
        website_url = 'https://www.welcometothejungle.com/'
        self.driver.get(website_url)

        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(sign_in_menu_btn_selector))
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(cookie_accept_btn_selector))

    def accept_cookies(self):
        """Tries to click accept on cookie notice and ignores if it fails"""
        print('Trying to accept the cookies...')

        try:
            cookie_accept_btn = self.driver.find_element(*cookie_accept_btn_selector)
            cookie_accept_btn.click()
            print('Accepted the cookies....')
        except:
            print("Couldn't accept cookies...")
            pass

        sleep(2)


    def login(self):
        """
        1. clicks sign in button in menu
        2. fills email and password fields
        3. clicks sign in button
        """
        print('Going to sign in...')
        sign_in_menu_btn = self.driver.find_element(*sign_in_menu_btn_selector)
        sign_in_menu_btn.click()

        WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(email_selector))
        sleep(4)
        email_input = self.driver.find_element(*email_selector)
        password_input = self.driver.find_element(*password_selector)

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)

        sign_in_btn = self.driver.find_element(*sign_in_btn_selector)
        sign_in_btn.click()

        print('Signed in...')
        sleep(5)


    def go_to_job_list(self):
        """
            1. goes to job list url
            2. waits 6 seconds to make sure that the jobs are loaded
        """

        print('Going to job list url...')
        self.driver.get(self.job_list_url)
        sleep(6)


    def remove_location_filter(self):
        """removes the default search filter"""
        try:
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(location_cross_selector))
            cross = self.driver.find_element(*location_cross_selector)
            cross.click()
            sleep(5)
        except:
            pass


    def get_jobs_list(self):
        """
        1. assumes that the bot is on job list url
        2. grabs the html for jobs section
        3. parses the jobs and gets them in a list of dictionaries
        4. finally returns the parsed list of jobs
        """
        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(jobs_result_selector))
        results = self.driver.find_element(*jobs_result_selector)
        html = results.get_attribute('outerHTML')
        jobs_list = get_jobs_list(html)
        return jobs_list


    def get_page_count(self):
        """gets the number of pages from pagination that can be used to run the loop """
        try:
            sleep(2)
            page_count = self.driver.find_elements(By.CSS_SELECTOR, '.sc-fUkmAC.fTXNVO li')[-2]
            page_count = page_count.text
            print('Total page count: ', page_count)
        except:
            print('Error occurred when finding the page count')
            return None

        return int(page_count)


    def can_apply(self):
        """checks if the application is inside or outside the website"""
        apply_btn = self.driver.find_elements(*apply_btn_selector)

        if apply_btn:
            return True
        else:
            return False



    def apply_job(self, job):
        job_url = job['link']
        print('Going to apply to: ')
        print(f'Company: {job["company"]}   Heading: {job["heading"]}')
        print(f'Link: ', job['link'])

        tab1 = self.driver.current_window_handle
        self.driver.execute_script('window.open();')

        for window_handle in self.driver.window_handles:
            if window_handle != tab1:
                self.driver.switch_to.window(window_handle)

        self.driver.get(job_url)

        # Wait until the button is loaded
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="job_sticky-button-apply"]')))
        sleep(2)


        if self.can_apply():
            # get job text and print it
            page_body = self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
            job_text = get_job_description(page_body)

            print('Job text:\n ', job_text)

            # click apply button
            # TODO: problem with this section, sometimes the page doesn't load properly and apply button doesn't get clicked
            # after clicking the apply button, I need a way to check if I clicked it
            while True:
                try:
                    apply_btn = self.driver.find_element(*apply_btn_selector)
                    apply_btn.click()
                    sleep(4)

                    # get the cover letter field and enter the cover letter
                    cover_letter_field = self.driver.find_elements(*cover_letter_selector)

                    if cover_letter_field:
                        cover_letter_field = cover_letter_field[0]
                        cover_letter = get_cover_letter(job_text)
                        print('COVER LETTER: ', cover_letter)
                        cover_letter_field.send_keys(cover_letter)

                    # get the parent element of questions
                    questions_field = self.driver.find_elements(*questions_field_selector)

                    if questions_field:
                        questions_field = questions_field[0]
                        # get the individual question sections that contain the question text and textarea field for answering the questions
                        questions_sections = questions_field.find_elements(By.CSS_SELECTOR, 'div')
                        # loop through the questions and answer them
                        questions_count = len(questions_sections)

                        for i in range(questions_count):
                            questions_sections = questions_field.find_elements(By.CSS_SELECTOR, 'div')
                            q = questions_sections[i]

                            label = q.find_element(By.CSS_SELECTOR, 'label')
                            textarea = q.find_element(By.CSS_SELECTOR, 'textarea')
                            print('QUESTION: ', label.text)
                            answer = get_answer(label.text)
                            print('ANSWER: ', answer)
                            textarea.send_keys(answer)

                    # check required checkboxes
                    checkbox1 = self.driver.find_element(*checkbox1_selector)
                    self.driver.execute_script("arguments[0].scrollIntoView();", checkbox1)
                    sleep(0.5)
                    checkbox1.click()

                    checkbox2 = self.driver.find_element(*checkbox2_selector)
                    checkbox2.click()

                    # finally submit the job application
                    submit_btn = self.driver.find_element(*submit_btn_selector)
                    submit_btn.click()

                    break
                except:
                    print("Page couldn't load properly, reloading it...")
                    traceback.print_exc()
                    self.driver.refresh()
                    sleep(3)
                    self.get_rid_of_alert()
                    sleep(7)



            sleep(4)
            print('submitted the job application....\n\n')
            job['status'] = 'APPLIED'

            # close the tab and move back to tab1
            self.driver.execute_script('window.close();')

            sleep(2)
            self.get_rid_of_alert()
            sleep(2)

            self.driver.switch_to.window(tab1)


        else:
            print('Skipping because application outside of the website...\n\n')
            job['status'] = 'SKIPPED'

            self.driver.execute_script('window.close();')
            self.driver.switch_to.window(tab1)




    def get_rid_of_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass