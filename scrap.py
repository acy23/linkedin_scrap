import time
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

import mongoExcelDTO


# Navigate to LinkedIn

def login(webDriver):
    webDriver.get('https://www.linkedin.com')

    print("x")
    try:
        webDriver.find_element(By.CSS_SELECTOR, "button.authwall-join-form__form-toggle--bottom[data-tracking-control-name='auth_wall_desktop-login-toggle']").click()
        print("found")

    except NoSuchElementException:

        login_input_email = webDriver.find_element(By.ID, "session_key")
        login_input_pass = webDriver.find_element(By.ID, "session_password")

        login_input_email.send_keys('bloggeraekle@gmail.com')
        login_input_pass.send_keys('Cazal1776')

        webDriver.find_element(By.CSS_SELECTOR, "button.btn-md.btn-primary.flex-shrink-0.cursor-pointer.sign-in-form__submit-btn--full-width[data-id='sign-in-form__submit-btn'][data-tracking-control-name='homepage-basic_sign-in-submit-btn']").click()

def goToProfileAndConntections(webDriver):
    webDriver.get("""https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Nxj""")

def getProfileUrlsOfConnections(driver):
    elements = driver.find_elements(By.XPATH,"//a[contains(@class, 'app-aware-link ')]")
    href_texts = [element.get_attribute("href") for element in elements]
    filtered_data = [url for url in href_texts if "miniProfile" in url]
    filtered_data = list(set(filtered_data))
    filtered_data = [url for url in filtered_data if url.startswith('https://www.linkedin.com/in/') and url[len('https://www.linkedin.com/in/')].islower()]
    return filtered_data

def goUrlAndGetData(connectionUrlsOnPage, driver):
    dtoList = []
    dataList = []

    # Get Contact Info section start

    for url in connectionUrlsOnPage:
        driver.get(url)     # Go to each profile

        userInfoModel = mongoExcelDTO.PersonDTO()

        driver.find_element(By.ID, "top-card-text-details-contact-info").click() # Click info button
        wait = WebDriverWait(driver, 2)  # 2 seconds is the maximum wait time

        linkedin_url = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-link"))).text
        print(linkedin_url)
        userInfoModel.linkedin_url = linkedin_url
        dataList.append(linkedin_url)

        email = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-email")))
        email_text = email.find_element(By.TAG_NAME, "a").text
        userInfoModel.email = email_text
        dataList.append(email_text)

        try:
            connection_start_time = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type")))
            span_element = connection_start_time.find_element(By.TAG_NAME, "span")
            if span_element:
                connection_start_time_text = span_element.text
                userInfoModel.connection_start_time = connection_start_time_text
                dataList.append(connection_start_time_text)
        except NoSuchElementException:
            print("No such span tag")

        try:
            website = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-websites")))
            if website:
                website_text = website.find_element(By.TAG_NAME, "a").text
                userInfoModel.website_url = website_text
                dataList.append(website_text)
        except TimeoutException:
            print("Website section element not found")

        try:
            phone = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-phone")))
            if phone:
                phone_text = phone.find_element(By.TAG_NAME, "span").text
                userInfoModel.phone = phone_text
                dataList.append(phone_text)
        except TimeoutException:
            print("Phone section element not found")

        try:
            address = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type ci-address")))
            if address:
                address_text = address.find_element(By.TAG_NAME, "a").text
                userInfoModel.address = address_text
                dataList.append(address_text)
        except TimeoutException:
            print("Address section element not found")

        try:
            birthday = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type ci-birthday")))
            if birthday:
                birthday_text = birthday.find_element(By.TAG_NAME, "span").text
                userInfoModel.birthday = birthday_text
                #dataList.append(birthday_text)
        except TimeoutException:
            print("Birthday section element not found")

        wait.until(EC.visibility_of_element_located((By.ID, "ember291"))).click()

        # Contact Info section end





    return dataList

if(__name__ == '__main__'):

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    #login(driver)
    #goToProfileAndConntections(driver)

    # That part should be done for every page.

    driver.get('https://www.linkedin.com')
    time.sleep(45)

    connectionUrlsOnPage = getProfileUrlsOfConnections(driver)
    data = goUrlAndGetData(connectionUrlsOnPage,driver)

    # That part should be done for every page.
    
    print(data)

#driver.quit()