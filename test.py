from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDMwOTJjNGI3MWE5ODA1NDc3MzBkZGMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NDMwYWEwMmM0NTRiZDE4MTY3YjBkMTQifQ.8Q6PhxlSBksH69FDYs0QmC5UFGGag8AK5tAJjCDkZ4o"
profile_id = "66bf0e8f80ea8e8bbe7b21f2"


post_url = "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2CrecentSearchParam%3A(id%3A3976882492%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3ANorth%2520America%2CselectionType%3AINCLUDED))))%2Ckeywords%3Asearch%2520engine%2520optimization)&sessionId=kZVUUWdkRha2J6fnB1Vrnw%3D%3D"
gl = GoLogin(
    {
        "token": api_key,
        "profile_id": profile_id
    }
)

with sync_playwright() as p:
    debugger_address = gl.start()
    browser = p.chromium.connect_over_cdp("http://" + debugger_address)
    default_context = browser.contexts[0]
    page = default_context.pages[0]


    page.goto("https://www.linkedin.com/sales/lead/ACwAAAALxw0BuZNtOUEbRQT0jqsBicgrtOcFYMc,NAME_SEARCH,ULmZ?_ntb=hb4CvIzQRIuO1THKF%2B6neQ%3D%3D")
    page.wait_for_load_state("load")
    sleep(3)

    p_p_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[2]//h2")
    p_c_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[2]//p[@data-anonymize='company-name']")
    p_c_t_e_1 = page.locator("((//li[@class='_experience-entry_1irc72'])[2]//span)[1]")

    previous_position_1 = p_p_e_1.inner_text() if p_p_e_1.count() > 0 else ''
    previous_position_1 += ', ' + p_c_e_1.inner_text() if p_c_e_1.count() > 0 else ''
    previous_position_1 += ', ' + p_c_t_e_1.inner_text() if p_c_t_e_1.count() > 0 else ''

    p_p_e_2 = page.locator("(//li[@class='_experience-entry_1irc72'])[3]//h2")
    p_c_e_2 = page.locator("(//li[@class='_experience-entry_1irc72'])[3]//p[@data-anonymize='company-name']")
    p_c_t_e_2 = page.locator("((//li[@class='_experience-entry_1irc72'])[3]//span)[1]")
    previous_position_2 = p_p_e_2.inner_text() if p_p_e_2.count() > 0 else ''
    previous_position_2 += ', ' + p_c_e_2.inner_text() if p_c_e_2.count() > 0 else ''
    previous_position_2 += ', ' + p_c_t_e_2.inner_text() if p_c_t_e_2.count() > 0 else ''

    p_p_e_3 = page.locator("(//li[@class='_experience-entry_1irc72'])[4]//h2")
    p_c_e_3 = page.locator("(//li[@class='_experience-entry_1irc72'])[4]//p[@data-anonymize='company-name']")
    p_c_t_e_3 = page.locator("((//li[@class='_experience-entry_1irc72'])[4]//span)[1]")
    previous_position_3 = p_p_e_3.inner_text() if p_p_e_3.count() > 0 else ''
    previous_position_3 += ', ' + p_c_e_3.inner_text() if p_c_e_3.count() > 0 else ''
    previous_position_3 += ', ' + p_c_t_e_3.inner_text() if p_c_t_e_3.count() > 0 else ''

    p_p_e_4 = page.locator("(//li[@class='_experience-entry_1irc72'])[5]//h2")
    p_c_e_4 = page.locator("(//li[@class='_experience-entry_1irc72'])[5]//p[@data-anonymize='company-name']")
    p_c_t_e_4 = page.locator("((//li[@class='_experience-entry_1irc72'])[5]//span)[1]")
    previous_position_4 = p_p_e_4.inner_text() if p_p_e_4.count() > 0 else ''
    previous_position_4 += ', ' + p_c_e_4.inner_text() if p_c_e_4.count() > 0 else ''
    previous_position_4 += ', ' + p_c_t_e_4.inner_text() if p_c_t_e_4.count() > 0 else ''

    p_p_e_5 = page.locator("(//li[@class='_experience-entry_1irc72'])[6]//h2")
    p_c_e_5 = page.locator("(//li[@class='_experience-entry_1irc72'])[6]//p[@data-anonymize='company-name']")
    p_c_t_e_5 = page.locator("((//li[@class='_experience-entry_1irc72'])[6]//span)[1]")
    previous_position_5 = p_p_e_5.inner_text() if p_p_e_5.count() > 0 else ''
    previous_position_5 += ', ' + p_c_e_5.inner_text() if p_c_e_5.count() > 0 else ''
    previous_position_5 += ', ' + p_c_t_e_5.inner_text() if p_c_t_e_5.count() > 0 else ''

    print('p1', previous_position_1)
    print('p2', previous_position_2)
    print('p3', previous_position_3)
    print('p4', previous_position_4)
    print('p5', previous_position_5)

    page.locator("//address//button").click()
    email_element = page.locator("//a[@data-anonymize='email']")
    email = email_element.inner_text() if email_element.count() > 0 else ''
    page.locator("(//button[@aria-label='Dismiss'])[1]").click()

    print(email)

    # Compnay section
    c_j_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2")
    currrent_job_titles = c_j_e_1.inner_text() if c_j_e_1.count() > 0 else ''
    # Nagivate Company Page
    company_salse_page = page.locator("((//li[@class='_experience-entry_1irc72'])[1]//a)[1]")
    if company_salse_page.count() > 0 and company_salse_page.get_attribute('href') != None:
        company_salse_page_link = company_salse_page.get_attribute('href')
        page.goto('https://www.linkedin.com' + company_salse_page_link)
        page.wait_for_load_state('load')
        sleep(3)
        current_company_element = page.locator("(//div[@data-anonymize='company-name'])[1]")
        current_company = current_company_element.inner_text() if current_company_element.count() > 0 else ''
        industry_element = page.locator("//span[@data-anonymize='industry']")
        industry = industry_element.inner_text() if industry_element.count() > 0 else ''

        All_employees_element = page.locator("//span[@data-anonymize='company-size']")
        All_employees = All_employees_element.inner_text() if All_employees_element.count() > 0 else ''

        revenue_element = page.locator("//span[@data-anonymize='revenue']")
        revenue = revenue_element.inner_text() if revenue_element.count() > 0 else ''

        more_element = page.locator("//button[@aria-label='More options']")
        if more_element.count() > 0:
            more_element.click()
            default_context.grant_permissions(permissions=["clipboard-read", "clipboard-write"], origin=page.url)
            copy_element = page.locator("//button[@data-control-name='copy_li_url']")
            if copy_element.count() > 0:
                copy_element.click()
                company_linkedin = page.evaluate("navigator.clipboard.readText()")
        else:
            company_linkedin = ''
    else:
        current_company = ''
        print("passed")
        industry = ''
        All_employees = ''
        revenue = ''
        company_linkedin = ''
    Twitter = ''


    sleep(50)

    browser.close()
    gl.stop()