import time, random, string
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

def GetAndWriteData(connectionUrlsOnPage, driver, connection):
    dtoList = []
    dataList = []
    
    # Get Contact Info section start

    for url in connectionUrlsOnPage:
        driver.get(url)     # Go to each profile

        delay = random.uniform(1,20)
        time.sleep(delay)

        cookies = driver.get_cookies()  # Load cookies against auto log out.
        for cookie in cookies:
            driver.add_cookie(cookie)

        userInfoModel = PersonDTO()

        try:
            role_description = driver.find_element(By.CLASS_NAME, "text-body-medium").text
            userInfoModel.user_role_description = role_description
        except NoSuchElementException:
            print("User role description section element not found")
        except TimeoutException:
            print("User role description section element not found")

        try:
            description = driver.find_element(By.CLASS_NAME, "display-flex.ph5.pv3").text
            userInfoModel.description = description
        except NoSuchElementException:
            print("User description section element not found")
        except TimeoutException:
            print("User description section element timeout error")

        try:
            experience_tag = driver.find_element(By.ID, "experience")
            parent_element = experience_tag.find_element(By.XPATH, "parent::*")  
            last_experience_info = parent_element.find_element(By.CLASS_NAME, "pvs-entity.pvs-entity--padded.pvs-list__item--no-padding-in-columns").text

            lines = last_experience_info.split("\n")
            unique_lines = list(dict.fromkeys(lines))
            last_experience_info = ", ".join(unique_lines)

            userInfoModel.last_experince_info = last_experience_info
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

        userInfoModel.created_by = "new_user"

        dtoList.append(userInfoModel)
    
    connection.insert_many_documents("datacollection", dtoList)

    return dtoList

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))
