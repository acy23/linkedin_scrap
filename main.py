import time, random, string, json, requests
from urllib.parse import urlparse
import concurrent.futures
from mongoExcelDTO import PersonDTO
from mongoService import MongoDBConnection

connection = MongoDBConnection()

data_to_be_inserted = []
headers = {
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'bcookie="v=2&b16a6880-63b4-4e24-82af-71d1d03805bf"; bscookie="v=1&20220920061515d8a31d73-4891-4a3c-8220-91f7438c75c4AQGW52ZsQXfpT3PpywAYuKc_ZlVUX40u"; G_ENABLED_IDPS=google; aam_uuid=39133127669886033803705351608428271643; li_theme=light; li_theme_set=app; li_sugr=324b85ab-a442-4966-a23b-df702a8bbc46; _gcl_au=1.1.812203118.1663679997; timezone=Europe/Istanbul; s_fid=3F90ECCF2A10D79D-36AA37FC393DEB40; gpv_pn=developer.linkedin.com%2F; s_ips=754; s_tp=2514; li_rm=AQE2ReSV7ki09AAAAYjDnW3a4R4x18VypDsvyxgYU9AAP2YPfQr62s8yuIJfn383Lztl1ws-4FbOI_Fp7NRnwRpm6Zb6P9kCDqfM3UEHGXM2WTJ_0W22NutP8N3BwH6C5mY_61ZrvRt9gBo_AzPhlWHYVJwzl4mFoJFzvf-FtfBEnb_Tm1GJHqR67hLAg3g58P9i4-ApL97kyhQBMdKFeCBB3iKym2L479NW_x5g32bzT9mFVCyhgvsSaBNivLW4Bkv03sna_gMEkhQb5yVaSj0xiIUjdE1XpSUBulJd2dasyNIliJBS4NaYXQipCXI8-vleJPLRIKsdJINUFfo; visit=v=1&M; mbox=PC#429670f1ff524e97aae7ef1b04fd840f.37_0#1703000788|session#41d49f7c4f6b4b88abd194c3c7086536#1687450648; s_tslv=1687448788687; _guid=c3aff38e-4c42-42fe-9d99-61fdd927d3e7; g_state={"i_l":0}; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; AnalyticsSyncHistory=AQIVI8skjSeIKQAAAYlvTNG8IcFjfAF_YYmDollKz2bdfrO3FGRZLTy6akdf8LSx7Q-Inu6lpeyL8x31zdh8Uw; lms_ads=AQFNXuf9RGGnPgAAAYlvTNPNyjMH48VhmwxGyd_eMllv2N_gj6KFAAcbj0ivyQh5Jzb03lNPjbkRIIEFKJpLdnu5NYc_uMeU; lms_analytics=AQFNXuf9RGGnPgAAAYlvTNPNyjMH48VhmwxGyd_eMllv2N_gj6KFAAcbj0ivyQh5Jzb03lNPjbkRIIEFKJpLdnu5NYc_uMeU; lang=v=2&lang=tr-tr; JSESSIONID="ajax:5158197680970797865"; li_at=AQEDAS5iJPUAc2elAAABiW9PIAsAAAGJk1ukC00Ap0QkYrF1bfLLSfJmT3poysZLrjPb2mme9CjQP-MZiuYv2QKJT0LdJST5Gbv0fSRXihAAo3mBUQEUm7vnvncuPPSc1Zm4EvkVTx5IjHXEsIw3zaba; liap=true; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19557%7CMCMID%7C39276468790955694713720855767473515472%7CMCAAMLH-1690394411%7C6%7CMCAAMB-1690394411%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1689796811s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C945697933; UserMatchHistory=AQJxYFIiqkpoZwAAAYlvjFd-LmxYP7cts1_E2UJmnaQBHlgnr1w6wvExRS5lHiORCvHOuJIktLZBcoUeTeW_gEBGzcx5D19yOd6mFvAhMb8OLaRbPkUXjvNgpc5huDqN0m-Gl_XRw-cfi1LFkJojE60XnUEXouVxQY0wkyeSdpn4JOsOFb3Z47C2CtmLthUYxwAGHKas7R1XMrNzCiZFBVMQKCGlk3rk7YBUC0fvV4zIFiVH5OSvK1Du6d1XHCi3IbKFGNqzV9fHcDBAHVouixCnaGK6GceVyou7aK1pJXO2G9vS7nKMrOcXkIfecFZawsMK1BIO9gQh1k8posT0PakuWrkfn_M; lidc="b=VB25:s=V:r=V:a=V:p=V:g=4334:u=362:x=1:i=1689793617:t=1689876004:v=2:sig=AQEqsF2fTJCn9qqs-dirYsF-dLkXVNDQ"',
    'csrf-token': 'ajax:5158197680970797865',
    'referer': '',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-li-lang': 'tr_TR',
    'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base_contact_details;VgeYaTLFS4yMufHaRgOlEw==',
    'x-li-track': '{"clientVersion":"1.12.9535","mpVersion":"1.12.9535","osName":"web","timezoneOffset":3,"timezone":"Europe/Istanbul","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
    'x-restli-protocol-version': '2.0.0'
}


def extract_profile_id(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    profile_id = path.strip("/").split("/")[-1]
    return profile_id

def parse_response(response):
    try:
        data = json.loads(response)

        included_data = data.get("included", [])
        userInfoModel = PersonDTO()

        for item in included_data:
            if item.get("$type") == "com.linkedin.voyager.dash.identity.profile.Profile":
                if item.get("address"):
                    userInfoModel.address = item.get("address")
                userInfoModel.phone = item.get("phoneNumbers", [])
                userInfoModel.firstname = item.get("firstName")
                userInfoModel.lastname = item.get("lastName")

                email_address = item.get("emailAddress", {}).get("emailAddress")
                if email_address:
                    userInfoModel.email = email_address

                birth_dates = item.get("birthDateOn")
                if birth_dates is not None:
                    userInfoModel.month = birth_dates.get("month")
                    userInfoModel.day = birth_dates.get("day")

                userInfoModel.headline = item.get("headline")

            if item.get("$type") == "com.linkedin.voyager.dash.identity.profile.Website":
                website_url = item.get("url")
                if website_url:
                    userInfoModel.website_url = website_url
                    #break  # Found website URL, exit the loop

            if item.get("$type") == "com.linkedin.voyager.dash.identity.profile.PhotoFilterPicture":
                display_image_reference = item.get("displayImageReference")
                if display_image_reference is not None:
                    userInfoModel.profile_picture_url = display_image_reference.get("url")

            userInfoModel.created_by = "esram77_final"

        return userInfoModel

    except Exception as ex:
        print("PARSER ERROR:", ex)

def send_request(linkedinUrl, memberIdentity):
    url = 'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(memberIdentity:' + memberIdentity + ')&&queryId=voyagerIdentityDashProfiles.84cab0be7183be5d0b8e79cd7d5ffb7b'
    headers['referer'] = linkedinUrl.encode('utf-8')  # Encode the referer value as UTF-8
    response = requests.get(url, headers=headers)
    return response

def process_data(lm):
    try:
        userLinkedinUrl = lm['linkedin_url']
        memberIdentity = extract_profile_id(userLinkedinUrl)

        response = send_request(userLinkedinUrl, memberIdentity)
        parsed_result = parse_response(response.text)
        if parsed_result:
            parsed_result.linkedin_url = userLinkedinUrl

        data_to_be_inserted.append(parsed_result)
        print("ADDED: ", parsed_result)
    except Exception as err:
        print("ERR: ", err, lm)

if(__name__ == '__main__'):
    data = connection.get_documents_by_creator('datacollection','esram77')
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for lm in data:
            executor.map(process_data, lm)
    connection.insert_many_documents("datacollection", data_to_be_inserted)
    