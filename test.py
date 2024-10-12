from time import sleep
from playwright.sync_api import sync_playwright
import os
import csv
from customtkinter import *
import json
import concurrent.futures



args=[
     '--disable-blink-features=AutomationControlled',
     '--start-maximized',
     '--disable-infobars',
     '--no-sandbox',
     '--disable-dev-shm-usage',
     '--disable-extensions',
     '--remote-debugging-port=0',
     '--disable-web-security',
     '--enable-features=WebRTCPeerConnectionWithBlockIceAddresses',
     '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
 ]

chrome_path = os.path.join(os.getcwd(), "chrome-win/chrome.exe")
storage_state_file = os.path.join(os.getcwd(), "storage_state.json")

url = "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2CrecentSearchParam%3A(id%3A3976882780%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3AFUNCTION%2Cvalues%3AList((id%3A15%2Ctext%3AMarketing%2CselectionType%3AINCLUDED)))%2C(type%3AINDUSTRY%2Cvalues%3AList((id%3A4%2Ctext%3ASoftware%2520Development%2CselectionType%3AINCLUDED)))%2C(type%3ACOMPANY_TYPE%2Cvalues%3AList((id%3AC%2Ctext%3APublic%2520Company%2CselectionType%3AINCLUDED)))%2C(type%3AREGION%2Cvalues%3AList((id%3A90000049%2Ctext%3ALos%2520Angeles%2520Metropolitan%2520Area%2CselectionType%3AINCLUDED))))%2Ckeywords%3Asearch%2520engine%2520optimization)&sessionId=KvaBGe7dQtCfZO2PYb4reA%3D%3D"



with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False,
                                        args=args,
                                        executable_path=chrome_path
        )
    context = browser.new_context(storage_state=storage_state_file, no_viewport=True)
    page = context.new_page()

    page.goto(url.strip(), timeout=600000)

    page.wait_for_url('https://www.linkedin.com/sales/search/*')
    data = True
    try:
        page.wait_for_selector("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]//span[@data-anonymize='person-name']")
    except:
        data = False
    if data:
        i = 1
        while True:
            print(i)
            if i == 1:
                page.locator("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]//span[@data-anonymize='person-name']").click()
            page.wait_for_selector("//section[@id='profile-card-section']")
            full_name = page.locator("//section[@id='profile-card-section']//a[@data-anonymize='person-name']")
            full_name = full_name.inner_text() if full_name.count() > 0 else ''
            if full_name != None:
                first_name = full_name.split(' ')[0]
                last_name = full_name.split(' ')[1]
            toggle_button = page.locator("(//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n'])[2]")
            if toggle_button.count() > 0:
                toggle_button.click()
                profile_link_element = page.locator("(//a[@class='ember-view _item_1xnv7i'])[2]")
                if profile_link_element.count() > 0:
                    normal_linkedin_url = profile_link_element.get_attribute('href') or ''
                sales_navi_url_element = page.locator("(//a[@class='ember-view _item_1xnv7i'])[1]")
                if sales_navi_url_element.count() > 0:
                    sales_navi_url = 'https://www.linkedin.com'+sales_navi_url_element.get_attribute('href') or ''

            headline = page.locator("//span[@data-anonymize='headline']").inner_text() or ''
            
            about_element = page.locator("//section[@id='about-section']/div")
            about = about_element.get_attribute("title") if about_element.count() > 0 else ''
            
            location_element = page.locator("((//section[@class='_header_sqh8tm']//div)[9]//div)[1]")
            location = location_element.inner_text() if location_element.count() > 0 else ''
            
            email_element = page.locator("span[data-anonymize='email']")
            email = email_element.inner_text() if email_element.count() > 0 else ''

            exprience_element = page.locator("//section[@id='scroll-to-experience-section']//button")
            if exprience_element.count() > 0:
                exprience_element.click()


            c_p_e = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2")
            c_c_e = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//p[@data-anonymize='company-name']")
            c_c_t_e = page.locator("((//li[@class='_experience-entry_1irc72'])[1]//span)[1]")
            currrent_position = c_p_e.inner_text() if c_p_e.count() > 0 else ''
            currrent_position += ', ' + c_c_e.inner_text() if c_c_e.count() > 0 else ''
            currrent_position += ', ' + c_c_t_e.inner_text() if c_c_t_e.count() > 0 else ''

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

            p_p_e_6 = page.locator("(//li[@class='_experience-entry_1irc72'])[7]//h2")
            p_c_e_6 = page.locator("(//li[@class='_experience-entry_1irc72'])[7]//p[@data-anonymize='company-name']")
            p_c_t_e_6 = page.locator("((//li[@class='_experience-entry_1irc72'])[7]//span)[1]")
            previous_position_6 = p_p_e_6.inner_text() if p_p_e_6.count() > 0 else ''
            previous_position_6 += ', ' + p_c_e_6.inner_text() if p_c_e_6.count() > 0 else ''
            previous_position_6 += ', ' + p_c_t_e_6.inner_text() if p_c_t_e_6.count() > 0 else ''

            p_p_e_7 = page.locator("(//li[@class='_experience-entry_1irc72'])[8]//h2")
            p_c_e_7 = page.locator("(//li[@class='_experience-entry_1irc72'])[8]//p[@data-anonymize='company-name']")
            p_c_t_e_7 = page.locator("((//li[@class='_experience-entry_1irc72'])[8]//span)[1]")
            previous_position_7 = p_p_e_7.inner_text() if p_p_e_7.count() > 0 else ''
            previous_position_7 += ', ' + p_c_e_7.inner_text() if p_c_e_7.count() > 0 else ''
            previous_position_7 += ', ' + p_c_t_e_7.inner_text() if p_c_t_e_7.count() > 0 else ''

            p_p_e_8 = page.locator("(//li[@class='_experience-entry_1irc72'])[9]//h2")
            p_c_e_8 = page.locator("(//li[@class='_experience-entry_1irc72'])[9]//p[@data-anonymize='company-name']")
            p_c_t_e_8 = page.locator("((//li[@class='_experience-entry_1irc72'])[9]//span)[1]")
            previous_position_8 = p_p_e_8.inner_text() if p_p_e_8.count() > 0 else ''
            previous_position_8 += ', ' + p_c_e_8.inner_text() if p_c_e_8.count() > 0 else ''
            previous_position_8 += ', ' + p_c_t_e_8.inner_text() if p_c_t_e_8.count() > 0 else ''

            p_p_e_9 = page.locator("(//li[@class='_experience-entry_1irc72'])[10]//h2")
            p_c_e_9 = page.locator("(//li[@class='_experience-entry_1irc72'])[10]//p[@data-anonymize='company-name']")
            p_c_t_e_9 = page.locator("((//li[@class='_experience-entry_1irc72'])[10]//span)[1]")
            previous_position_9 = p_p_e_9.inner_text() if p_p_e_9.count() > 0 else ''
            previous_position_9 += ', ' + p_c_e_9.inner_text() if p_c_e_9.count() > 0 else ''
            previous_position_9 += ', ' + p_c_t_e_9.inner_text() if p_c_t_e_9.count() > 0 else ''

            p_p_e_10 = page.locator("(//li[@class='_experience-entry_1irc72'])[11]//h2")
            p_c_e_10 = page.locator("(//li[@class='_experience-entry_1irc72'])[11]//p[@data-anonymize='company-name']")
            p_c_t_e_10 = page.locator("((//li[@class='_experience-entry_1irc72'])[11]//span)[1]")
            previous_position_10 = p_p_e_10.inner_text() if p_p_e_10.count() > 0 else ''
            previous_position_10 += ', ' + p_c_e_10.inner_text() if p_c_e_10.count() > 0 else ''
            previous_position_10 += ', ' + p_c_t_e_10.inner_text() if p_c_t_e_10.count() > 0 else ''

     
            # Education expriments
            edu_element = page.locator("//section[@data-sn-view-name='feature-lead-education']//button")
            if edu_element.count() > 0:
                edu_element.click() 

            edu_inst_1 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]//h3")
            edu_duration_1 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]/div/p[2]")
            education_exprience_1 = edu_inst_1.inner_text() if edu_inst_1.count() > 0 else ''
            education_exprience_1 += edu_duration_1.inner_text() if edu_duration_1.count() > 0 else ''

            edu_inst_2 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]//h3")
            edu_duration_2 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]/div/p[2]")
            education_exprience_2 = edu_inst_2.inner_text() if edu_inst_2.count() > 0 else ''
            education_exprience_2 += edu_duration_2.inner_text() if edu_duration_2.count() > 0 else ''

            edu_inst_3 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]//h3")
            edu_duration_3 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]/div/p[2]")
            education_exprience_3 = edu_inst_3.inner_text() if edu_inst_3.count() > 0 else ''
            education_exprience_3 += edu_duration_3.inner_text() if edu_duration_3.count() > 0 else ''

            edu_inst_4 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]//h3")
            edu_duration_4 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]/div/p[2]")
            education_exprience_4 = edu_inst_4.inner_text() if edu_inst_4.count() > 0 else ''
            education_exprience_4 += edu_duration_4.inner_text() if edu_duration_4.count() > 0 else ''

            skills = ''
            get_all_skills = page.locator("//section[@data-sn-view-name='feature-lead-skills']//li/p")
            all_skill_elements = get_all_skills.element_handles()
            for skill in all_skill_elements:
                skills += skill.inner_text().strip() + ','

            person_img_ele = page.locator("(//img[@data-anonymize='headshot-photo'])[3]")
            person_image = person_img_ele.get_attribute("src") if person_img_ele.count() > 0 else ''



            print('full_name : ', full_name)
            print('first_name : ', first_name)
            print('last_name : ', last_name)
            print('normal_linkedin_url : ', normal_linkedin_url)
            print('sales_navi_url : ', sales_navi_url)
            print('About : ', about)
            print('location : ', location)
            print('Email : ', email)
            print(' currrent_position : ', currrent_position)
            print(' previous_position_1 : ', previous_position_1)
            print(' education_exprience_1 : ', education_exprience_1)
            print(' skills : ', skills)
            print(' person_image : ', person_image)

            button = page.locator('//header[@class="_inline-sidesheet-header_1cn7lg"]//button[2]')
            button.click()
            if button.is_disabled():
                break
            i+=1


    sleep(10)

    page.close()