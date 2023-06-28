import time
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from mongoExcelDTO import PersonDTO
from mongoService import MongoDBConnection


# Navigate to LinkedIn

def login(webDriver):
    webDriver.get('https://www.linkedin.com')

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

def GetAndWriteData(connectionUrlsOnPage, driver, connection):
    dtoList = []
    dataList = []
    
    # Get Contact Info section start

    for url in connectionUrlsOnPage:
        driver.get(url)     # Go to each profile

        userInfoModel = PersonDTO()

        try:
            role_description = driver.find_element(By.CLASS_NAME, "text-body-medium").text
            userInfoModel.user_role_description = role_description
        except NoSuchElementException:
            print("User role description section element not found")
        except TimeoutException:
            print("User role description section element not found")

        try:
            div_element = driver.find_element(By.CSS_SELECTOR, ".pvs-list__outer-container")
            li_element = div_element.find_element(By.CSS_SELECTOR, ".artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column")
            element = li_element.find_element(By.CSS_SELECTOR, ".pvs-entity.pvs-entity--padded.pvs-list__item--no-padding-in-columns")

            role = element.find_element(By.XPATH ,'.//div[contains(@class, "mr1")]//span').text
            company = element.find_element(By.XPATH ,'.//span[contains(@class, "t-14")]').text

            userInfoModel.job_title = role
            userInfoModel.company_name = company
        except NoSuchElementException:
            print("Last job section does not found.")
        except TimeoutException:
            print("Timeout error while getting latest job data.")
            

        driver.find_element(By.ID, "top-card-text-details-contact-info").click() # Click info button
        wait = WebDriverWait(driver, 2)  # 2 seconds is the maximum wait time

        fullname = wait.until(EC.visibility_of_element_located((By.ID, "pv-contact-info"))).text
        userInfoModel.fullname = fullname

        linkedin_url = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-link"))).text
        print(linkedin_url)
        userInfoModel.linkedin_url = linkedin_url
        dataList.append(linkedin_url)

        try:
            email = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-email")))
            email_text = email.find_element(By.TAG_NAME, "a").text
            userInfoModel.email = email_text
            dataList.append(email_text)
        except NoSuchElementException:
            print("Email section element not found")
        except TimeoutException:
            print("Email section element not found")

        try:
            connection_section = wait.until(EC.visibility_of_element_located((By.XPATH, "//section[contains(@class, 'pv-contact-info__contact-type') and not(contains(@class, ' '))]")))
            if connection_section:
                connection_date = connection_section.find_element(By.CSS_SELECTOR, ".pv-contact-info__ci-container.t-14").text
                userInfoModel.connection_start_time = connection_date
        except NoSuchElementException:
            print("No such span tag")
        except TimeoutException:
            print("No such span tag")

        try:
            website = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-websites")))
            if website:
                website_text = website.find_element(By.TAG_NAME, "a").text
                userInfoModel.website_url = website_text
                dataList.append(website_text)
        except TimeoutException:
            print("Website section element not found")
        except NoSuchElementException:
            print("Website section element not found")

        try:
            phone = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-phone")))
            if phone:
                phone_text = phone.find_element(By.TAG_NAME, "span").text
                userInfoModel.phone = phone_text
                dataList.append(phone_text)
        except TimeoutException:
            print("Phone section element not found")
        except NoSuchElementException:
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
            birthday_section = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pv-contact-info__contact-type.ci-birthday")))
            if birthday_section:
                birthday_text = birthday_section.find_element(By.CSS_SELECTOR, ".pv-contact-info__ci-container .pv-contact-info__contact-item").text
                userInfoModel.birthday = birthday_text
                #dataList.append(birthday_text)
        except TimeoutException:
            print("Birthday section element not found")

        # Contact Info section end

        dtoList.append(userInfoModel)
    
    connection.insert_many_documents("datacollection", dtoList)

    return dtoList

if(__name__ == '__main__'):

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # That part should be done for every page.

    driver.get('https://www.linkedin.com')

    connection = MongoDBConnection()

    dataList = []

    page_number = 2

    time.sleep(45)

    while True:
        try:
            connectionUrlsOnPage = getProfileUrlsOfConnections(driver)
            if not connectionUrlsOnPage:
                print("Data collection is done :)...")
                break

            x = GetAndWriteData(connectionUrlsOnPage, driver, connection)

            base_url = "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page="

            driver.get(base_url + str(page_number) + "&sid=Mce")

            page_number += 1
           
        except NoSuchElementException:
            print("No continue button found")
            break

    # That part should be done for every page.


#driver.quit()