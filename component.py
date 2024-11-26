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
# Define a function that opens the browser and returns the browser and contex
storage_state_file = os.path.join(os.getcwd(), "storage_state.json")
def is_storage_state_valid(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return bool(data)  # true false depend data exist
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return False
    else:
        open(file_path, 'w').close()  # Create an empty file
        return False

def cookie_save(login_status, log, close_event):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=str(chrome_path),
            headless=False,
            args=args,
        )
        if is_storage_state_valid(storage_state_file):
            context = browser.new_context(storage_state=storage_state_file, no_viewport=True)
        else:
            # If storage state is not valid, create a new context
            context = browser.new_context(no_viewport=True)

        page = context.new_page()
        page.goto("https://www.linkedin.com/")

        # Check periodically whether the close_event is set
        while not close_event.is_set():
            # Perform any additional actions here if necessary
            pass
        # Save the storage state (including cookies)
        context.storage_state(path=storage_state_file)
        login_status.configure(text='Login Status : True')
        print("Login Data saved...")
        log.insert(END, "Login Data saved...\n")
        log.see(END)
        browser.close()


def stop_check(event, log) -> bool:
    if event:
        print("⏹️ Stoped...")
        log.insert(END, f"⏹️ Stoped...\n\n")
        log.see(END)
        return True
    else:
        return False

dicts_list = []
def quick_scrapping(browser_status, page_run, url, close_event, Output_Folder, delay, log):
    with sync_playwright() as playwright:
        if browser_status == 'show':
            browser = playwright.chromium.launch(executable_path=str(chrome_path),headless=False,args=args,)
        else:
            browser = playwright.chromium.launch(executable_path=str(chrome_path),args=args, )
        context = browser.new_context(storage_state=storage_state_file, no_viewport=True)
        page = context.new_page()

        print('Running Page Number : ', page_run)
        log.insert(END, f'Running Page Number : {str(page_run)}\n\n')
        log.see(END)

        page.goto(url.strip().replace('query=', f'page={str(page_run)}&query='), timeout=60000)

        page.wait_for_url('https://www.linkedin.com/sales/search/*')
        data = True
        try:
            page.wait_for_selector("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]//span[@data-anonymize='person-name']")
        except:
            data = False
        if data:
            i = 1
            while True:
                if stop_check(close_event.is_set(), log):
                    break  # Stop if the close_event is triggered
                print(f'Profile Data No. {str(i)} ( page {str(page_run)} )\n\n')
                log.insert(END, f'Profile Data No. {str(i)} ( page {str(page_run)} )\n\n')
                log.see(END)
                try:
                    if i == 1:
                        page.locator("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]//span[@data-anonymize='person-name']").click()
                    page.wait_for_selector("//section[@id='profile-card-section']")
                    unlock = page.locator("(//div[@class='_profile-unlock_1xow7n'])[1]")
                    if unlock.count() == 0:
                        full_name = page.locator("//section[@id='profile-card-section']//a[@data-anonymize='person-name']").first
                        full_name = full_name.inner_text() if full_name.count() > 0 else ''
                        if full_name != None:
                            first_name = full_name.split(' ')[0]
                            last_name = full_name.split(' ')[1]
                        toggle_button = page.locator("(//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n'])[2]")
                        if toggle_button.count() > 0:
                            toggle_button.click()
                            profile_link_element = page.locator("(//a[@class='ember-view _item_1xnv7i'])[2]").first
                            if profile_link_element.count() > 0:
                                normal_linkedin_url = profile_link_element.get_attribute('href') or ''
                            sales_navi_url_element = page.locator("(//a[@class='ember-view _item_1xnv7i'])[1]").first
                            if sales_navi_url_element.count() > 0:
                                sales_navi_url = 'https://www.linkedin.com' + sales_navi_url_element.get_attribute('href') or ''

                        headline = page.locator("//span[@data-anonymize='headline']").inner_text() or ''

                        about_element = page.locator("//section[@id='about-section']/div").first
                        about = about_element.get_attribute("title") if about_element.count() > 0 else ''

                        location_element = page.locator("((//section[@class='_header_sqh8tm']//div)[9]//div)[1]").first
                        location = location_element.inner_text() if location_element.count() > 0 else ''

                        email_element = page.locator("span[data-anonymize='email']").first
                        email = email_element.inner_text() if email_element.count() > 0 else ''

                        exprience_element = page.locator("//section[@id='scroll-to-experience-section']//button").first
                        if exprience_element.count() > 0:
                            exprience_element.click()

                        c_p_e = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2").first
                        c_c_e = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//p[@data-anonymize='company-name']").first
                        c_c_t_e = page.locator("((//li[@class='_experience-entry_1irc72'])[1]//span)[1]").first
                        currrent_position = c_p_e.inner_text() if c_p_e.count() > 0 else ''
                        currrent_position += ', ' + c_c_e.inner_text() if c_c_e.count() > 0 else ''
                        currrent_position += ', ' + c_c_t_e.inner_text() if c_c_t_e.count() > 0 else ''

                        p_p_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[2]//h2").first
                        p_c_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[2]//p[@data-anonymize='company-name']").first
                        p_c_t_e_1 = page.locator("((//li[@class='_experience-entry_1irc72'])[2]//span)[1]").first
                        previous_position_1 = p_p_e_1.inner_text() if p_p_e_1.count() > 0 else ''
                        previous_position_1 += ', ' + p_c_e_1.inner_text() if p_c_e_1.count() > 0 else ''
                        previous_position_1 += ', ' + p_c_t_e_1.inner_text() if p_c_t_e_1.count() > 0 else ''

                        p_p_e_2 = page.locator("(//li[@class='_experience-entry_1irc72'])[3]//h2").first
                        p_c_e_2 = page.locator("(//li[@class='_experience-entry_1irc72'])[3]//p[@data-anonymize='company-name']").first
                        p_c_t_e_2 = page.locator("((//li[@class='_experience-entry_1irc72'])[3]//span)[1]").first
                        previous_position_2 = p_p_e_2.inner_text() if p_p_e_2.count() > 0 else ''
                        previous_position_2 += ', ' + p_c_e_2.inner_text() if p_c_e_2.count() > 0 else ''
                        previous_position_2 += ', ' + p_c_t_e_2.inner_text() if p_c_t_e_2.count() > 0 else ''

                        p_p_e_3 = page.locator("(//li[@class='_experience-entry_1irc72'])[4]//h2").first
                        p_c_e_3 = page.locator("(//li[@class='_experience-entry_1irc72'])[4]//p[@data-anonymize='company-name']").first
                        p_c_t_e_3 = page.locator("((//li[@class='_experience-entry_1irc72'])[4]//span)[1]").first
                        previous_position_3 = p_p_e_3.inner_text() if p_p_e_3.count() > 0 else ''
                        previous_position_3 += ', ' + p_c_e_3.inner_text() if p_c_e_3.count() > 0 else ''
                        previous_position_3 += ', ' + p_c_t_e_3.inner_text() if p_c_t_e_3.count() > 0 else ''

                        p_p_e_4 = page.locator("(//li[@class='_experience-entry_1irc72'])[5]//h2").first
                        p_c_e_4 = page.locator("(//li[@class='_experience-entry_1irc72'])[5]//p[@data-anonymize='company-name']").first
                        p_c_t_e_4 = page.locator("((//li[@class='_experience-entry_1irc72'])[5]//span)[1]").first
                        previous_position_4 = p_p_e_4.inner_text() if p_p_e_4.count() > 0 else ''
                        previous_position_4 += ', ' + p_c_e_4.inner_text() if p_c_e_4.count() > 0 else ''
                        previous_position_4 += ', ' + p_c_t_e_4.inner_text() if p_c_t_e_4.count() > 0 else ''

                        p_p_e_5 = page.locator("(//li[@class='_experience-entry_1irc72'])[6]//h2").first
                        p_c_e_5 = page.locator("(//li[@class='_experience-entry_1irc72'])[6]//p[@data-anonymize='company-name']").first
                        p_c_t_e_5 = page.locator("((//li[@class='_experience-entry_1irc72'])[6]//span)[1]").first
                        previous_position_5 = p_p_e_5.inner_text() if p_p_e_5.count() > 0 else ''
                        previous_position_5 += ', ' + p_c_e_5.inner_text() if p_c_e_5.count() > 0 else ''
                        previous_position_5 += ', ' + p_c_t_e_5.inner_text() if p_c_t_e_5.count() > 0 else ''

                        p_p_e_6 = page.locator("(//li[@class='_experience-entry_1irc72'])[7]//h2").first
                        p_c_e_6 = page.locator("(//li[@class='_experience-entry_1irc72'])[7]//p[@data-anonymize='company-name']").first
                        p_c_t_e_6 = page.locator("((//li[@class='_experience-entry_1irc72'])[7]//span)[1]").first
                        previous_position_6 = p_p_e_6.inner_text() if p_p_e_6.count() > 0 else ''
                        previous_position_6 += ', ' + p_c_e_6.inner_text() if p_c_e_6.count() > 0 else ''
                        previous_position_6 += ', ' + p_c_t_e_6.inner_text() if p_c_t_e_6.count() > 0 else ''

                        p_p_e_7 = page.locator("(//li[@class='_experience-entry_1irc72'])[8]//h2").first
                        p_c_e_7 = page.locator("(//li[@class='_experience-entry_1irc72'])[8]//p[@data-anonymize='company-name']").first
                        p_c_t_e_7 = page.locator("((//li[@class='_experience-entry_1irc72'])[8]//span)[1]").first
                        previous_position_7 = p_p_e_7.inner_text() if p_p_e_7.count() > 0 else ''
                        previous_position_7 += ', ' + p_c_e_7.inner_text() if p_c_e_7.count() > 0 else ''
                        previous_position_7 += ', ' + p_c_t_e_7.inner_text() if p_c_t_e_7.count() > 0 else ''

                        p_p_e_8 = page.locator("(//li[@class='_experience-entry_1irc72'])[9]//h2").first
                        p_c_e_8 = page.locator("(//li[@class='_experience-entry_1irc72'])[9]//p[@data-anonymize='company-name']").first
                        p_c_t_e_8 = page.locator("((//li[@class='_experience-entry_1irc72'])[9]//span)[1]").first
                        previous_position_8 = p_p_e_8.inner_text() if p_p_e_8.count() > 0 else ''
                        previous_position_8 += ', ' + p_c_e_8.inner_text() if p_c_e_8.count() > 0 else ''
                        previous_position_8 += ', ' + p_c_t_e_8.inner_text() if p_c_t_e_8.count() > 0 else ''

                        p_p_e_9 = page.locator("(//li[@class='_experience-entry_1irc72'])[10]//h2").first
                        p_c_e_9 = page.locator("(//li[@class='_experience-entry_1irc72'])[10]//p[@data-anonymize='company-name']").first
                        p_c_t_e_9 = page.locator("((//li[@class='_experience-entry_1irc72'])[10]//span)[1]").first
                        previous_position_9 = p_p_e_9.inner_text() if p_p_e_9.count() > 0 else ''
                        previous_position_9 += ', ' + p_c_e_9.inner_text() if p_c_e_9.count() > 0 else ''
                        previous_position_9 += ', ' + p_c_t_e_9.inner_text() if p_c_t_e_9.count() > 0 else ''

                        p_p_e_10 = page.locator("(//li[@class='_experience-entry_1irc72'])[11]//h2").first
                        p_c_e_10 = page.locator("(//li[@class='_experience-entry_1irc72'])[11]//p[@data-anonymize='company-name']").first
                        p_c_t_e_10 = page.locator("((//li[@class='_experience-entry_1irc72'])[11]//span)[1]").first
                        previous_position_10 = p_p_e_10.inner_text() if p_p_e_10.count() > 0 else ''
                        previous_position_10 += ', ' + p_c_e_10.inner_text() if p_c_e_10.count() > 0 else ''
                        previous_position_10 += ', ' + p_c_t_e_10.inner_text() if p_c_t_e_10.count() > 0 else ''

                        # Education expriments
                        edu_element = page.locator("//section[@data-sn-view-name='feature-lead-education']//button").first
                        if edu_element.count() > 0:
                            edu_element.click()

                        edu_inst_1 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]//h3").first
                        edu_duration_1 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]/div/p[2]").first
                        education_exprience_1 = edu_inst_1.inner_text() if edu_inst_1.count() > 0 else ''
                        education_exprience_1 += edu_duration_1.inner_text() if edu_duration_1.count() > 0 else ''

                        edu_inst_2 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]//h3").first
                        edu_duration_2 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]/div/p[2]").first
                        education_exprience_2 = edu_inst_2.inner_text() if edu_inst_2.count() > 0 else ''
                        education_exprience_2 += edu_duration_2.inner_text() if edu_duration_2.count() > 0 else ''

                        edu_inst_3 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]//h3").first
                        edu_duration_3 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]/div/p[2]").first
                        education_exprience_3 = edu_inst_3.inner_text() if edu_inst_3.count() > 0 else ''
                        education_exprience_3 += edu_duration_3.inner_text() if edu_duration_3.count() > 0 else ''

                        edu_inst_4 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]//h3").first
                        edu_duration_4 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]/div/p[2]").first
                        education_exprience_4 = edu_inst_4.inner_text() if edu_inst_4.count() > 0 else ''
                        education_exprience_4 += edu_duration_4.inner_text() if edu_duration_4.count() > 0 else ''

                        skills = ''
                        get_all_skills = page.locator("//section[@data-sn-view-name='feature-lead-skills']//li/p")
                        all_skill_elements = get_all_skills.element_handles()
                        for skill in all_skill_elements:
                            skills += skill.inner_text().strip() + ','

                        person_img_ele = page.locator("(//img[@data-anonymize='headshot-photo'])[3]")
                        person_image = person_img_ele.get_attribute("src") if person_img_ele.count() > 0 else ''

                        dicts = {
                            'full_name': full_name,
                            'first_name': first_name,
                            'last_name': last_name,
                            'location': location,
                            'email': email,
                            'sales_navi_url': sales_navi_url,
                            'normal_linkedin_url': normal_linkedin_url,
                            'headline': headline,
                            'about': about,
                            'currrent_job_titles': currrent_position,
                            'previous_position_1': previous_position_1,
                            'previous_position_2': previous_position_2,
                            'previous_position_3': previous_position_3,
                            'previous_position_4': previous_position_4,
                            'previous_position_5': previous_position_5,
                            'previous_position_6': previous_position_6,
                            'previous_position_7': previous_position_7,
                            'previous_position_8': previous_position_8,
                            'previous_position_9': previous_position_9,
                            'previous_position_10': previous_position_10,
                            'education_exprience_1': education_exprience_1,
                            'education_exprience_2': education_exprience_2,
                            'education_exprience_3': education_exprience_3,
                            'education_exprience_4': education_exprience_4,
                            'skills': skills,
                            'person_image': person_image,
                        }

                        dicts_list.append(dicts)

                        header = ['full_name', 'first_name', 'last_name', 'location', 'email', 'sales_navi_url',
                                  'normal_linkedin_url',
                                  'headline', 'about', 'currrent_job_titles', 'previous_position_1',
                                  'previous_position_2', 'previous_position_3', 'previous_position_4', 'previous_position_5',
                                  'previous_position_6', 'previous_position_7', 'previous_position_8', 'previous_position_9',
                                  'previous_position_10', 'education_exprience_1', 'education_exprience_2',
                                  'education_exprience_3',
                                  'education_exprience_4', 'skills', 'person_image']

                        with open(f'{Output_Folder}/data.csv', 'w', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=header)
                            writer.writeheader()
                            writer.writerows(dicts_list)
                    else:
                        pass

                    i += 1
                    # Page Break Condition
                    button = page.locator('//header[@class="_inline-sidesheet-header_1cn7lg"]//button[2]')
                    button.click()
                    if button.is_disabled():
                        break

                except Exception as ops:
                    print(f"Error: {ops}")
                    log.insert(END, f"Error: {ops}\n")
                    log.see(END)
                finally:
                    pass
                sleep(int(delay))
            try:
                page.close()
            except Exception as ops:
                ops = ops
            finally:
                pass



def profile_scrapping(browser_status, page_run, url, close_event, Output_Folder, delay, log):
    with sync_playwright() as playwright:
        if browser_status == 'show':
            browser = playwright.chromium.launch(executable_path=str(chrome_path),headless=False,args=args,)
        else:
            browser = playwright.chromium.launch(executable_path=str(chrome_path),args=args, )
        context = browser.new_context(storage_state=storage_state_file, no_viewport=True)
        page = context.new_page()
        print('Running Page Number : ', page_run)
        log.insert(END, f'Running Page Number : {str(page_run)}\n\n')
        log.see(END)
        try:
            page.goto(url.strip().replace('query=', f'page={str(page_run)}&query='))

            page.wait_for_url('https://www.linkedin.com/sales/search/*')
            data = True
            try:
                page.wait_for_selector("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]")
            except:
                data = False

            if data == True:
                scroll = 3
                while scroll < 26:
                    if stop_check(close_event.is_set(), log):
                        break  # if stop event break loop
                    sleep(1)
                    try:
                        page.wait_for_selector(
                            f"//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][{str(scroll)}]")
                        scroll_e = page.locator(
                            f"//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][{str(scroll)}]")
                        if scroll_e.count() > 0:
                            scroll_e.click()
                    except Exception as ops:
                        print("Scroll error : ", ops)
                    scroll += 3
                sleep(1)
                all_element_links = page.locator("//a[@data-view-name='search-results-lead-name']")
                all_links = all_element_links.element_handles()
                get_profile_list = ['https://www.linkedin.com' + str(link.get_attribute('href')) for link in all_links]
            else:
                get_profile_list = []
        except Exception as ops:
            print(f'Page {str(page_run)} Search Page navigate error:', ops)
            get_profile_list = []

        log.insert(END, f'No. {str(page_run)}. Page\'s all profile Link has been scrapped\n\n')
        log.see(END)
        sleep(3)

        all_profile_number = len(get_profile_list)
        print('all_profile_number : ', all_profile_number, 'page : ', page_run)
        log.insert(END, f'Founded : {str(all_profile_number)} profiles ( page {str(page_run)} )\n\n')
        log.see(END)
        profile_number = 0
        while profile_number < all_profile_number:
            if stop_check(close_event.is_set(), log):
                break  # if stop event break loop
            print(profile_number + 1)
            log.insert(END, f'Profile Data No. {str(profile_number + 1)} ( page {str(page_run)} )\n\n')
            log.see(END)

            sales_navi_url = get_profile_list[profile_number]
            try:
                 profile_page = context.new_page()
                 profile_page.goto(sales_navi_url)
                 profile_page.wait_for_load_state('load')
                 profile_page.wait_for_url('https://www.linkedin.com/sales/lead/*')
                 profile_page.wait_for_selector("(//h1[@class='_headingText_e3b563 _default_1i6ulk _sizeXLarge_e3b563'])[1]",
                                                timeout=60000)

                 # Collect profile data
                 full_name = profile_page.locator("(//h1[@class='_headingText_e3b563 _default_1i6ulk _sizeXLarge_e3b563'])[1]").inner_text(timeout=60000) or ''
                 if full_name != None:
                     first_name = full_name.split(' ')[0]
                     last_name = full_name.split(' ')[1]
                 else:
                     first_name = ''
                     last_name = ''

                 normal_linkedin_url = ''
                 toggle_button = profile_page.locator("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n']").first
                 if toggle_button.count() > 0:
                     toggle_button.click()
                     linkedin_link_element = profile_page.locator("//a[@class='ember-view _item_1xnv7i']").first
                     if linkedin_link_element.count() > 0:
                         normal_linkedin_url = linkedin_link_element.get_attribute('href') or ''

                 headline = profile_page.locator("//span[@data-anonymize='headline']").inner_text() or ''

                 location_element = profile_page.locator("((//section[@class='_header_sqh8tm']//div)[9]//div)[1]").first
                 location = location_element.inner_text() if location_element.count() > 0 else ''

                 email_element = profile_page.locator("span[data-anonymize='email']").first
                 email = email_element.inner_text() if email_element.count() > 0 else ''

                 about_element = profile_page.locator("//section[@id='about-section']/div").first
                 about = about_element.get_attribute("title") if about_element.count() > 0 else ''

                 # Click on expriment element
                 exprience_element = page.locator("//section[@id='scroll-to-experience-section']//button").first
                 if exprience_element.count() > 0:
                     exprience_element.click()

                 p_p_e_1 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[2]//h2").first
                 p_c_e_1 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[2]//p[@data-anonymize='company-name']").first
                 p_c_t_e_1 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[2]//span)[1]").first
                 previous_position_1 = p_p_e_1.inner_text() if p_p_e_1.count() > 0 else ''
                 previous_position_1 += ', ' + p_c_e_1.inner_text() if p_c_e_1.count() > 0 else ''
                 previous_position_1 += ', ' + p_c_t_e_1.inner_text() if p_c_t_e_1.count() > 0 else ''

                 p_p_e_2 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[3]//h2").first
                 p_c_e_2 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[3]//p[@data-anonymize='company-name']").first
                 p_c_t_e_2 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[3]//span)[1]").first
                 previous_position_2 = p_p_e_2.inner_text() if p_p_e_2.count() > 0 else ''
                 previous_position_2 += ', ' + p_c_e_2.inner_text() if p_c_e_2.count() > 0 else ''
                 previous_position_2 += ', ' + p_c_t_e_2.inner_text() if p_c_t_e_2.count() > 0 else ''

                 p_p_e_3 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[4]//h2").first
                 p_c_e_3 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[4]//p[@data-anonymize='company-name']").first
                 p_c_t_e_3 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[4]//span)[1]").first
                 previous_position_3 = p_p_e_3.inner_text() if p_p_e_3.count() > 0 else ''
                 previous_position_3 += ', ' + p_c_e_3.inner_text() if p_c_e_3.count() > 0 else ''
                 previous_position_3 += ', ' + p_c_t_e_3.inner_text() if p_c_t_e_3.count() > 0 else ''

                 p_p_e_4 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[5]//h2").first
                 p_c_e_4 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[5]//p[@data-anonymize='company-name']").first
                 p_c_t_e_4 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[5]//span)[1]").first
                 previous_position_4 = p_p_e_4.inner_text() if p_p_e_4.count() > 0 else ''
                 previous_position_4 += ', ' + p_c_e_4.inner_text() if p_c_e_4.count() > 0 else ''
                 previous_position_4 += ', ' + p_c_t_e_4.inner_text() if p_c_t_e_4.count() > 0 else ''

                 p_p_e_5 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[6]//h2").first
                 p_c_e_5 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[6]//p[@data-anonymize='company-name']").first
                 p_c_t_e_5 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[6]//span)[1]").first
                 previous_position_5 = p_p_e_5.inner_text() if p_p_e_5.count() > 0 else ''
                 previous_position_5 += ', ' + p_c_e_5.inner_text() if p_c_e_5.count() > 0 else ''
                 previous_position_5 += ', ' + p_c_t_e_5.inner_text() if p_c_t_e_5.count() > 0 else ''

                 p_p_e_6 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[7]//h2").first
                 p_c_e_6 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[7]//p[@data-anonymize='company-name']").first
                 p_c_t_e_6 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[7]//span)[1]").first
                 previous_position_6 = p_p_e_6.inner_text() if p_p_e_6.count() > 0 else ''
                 previous_position_6 += ', ' + p_c_e_6.inner_text() if p_c_e_6.count() > 0 else ''
                 previous_position_6 += ', ' + p_c_t_e_6.inner_text() if p_c_t_e_6.count() > 0 else ''

                 p_p_e_7 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[8]//h2").first
                 p_c_e_7 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[8]//p[@data-anonymize='company-name']").first
                 p_c_t_e_7 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[8]//span)[1]").first
                 previous_position_7 = p_p_e_7.inner_text() if p_p_e_7.count() > 0 else ''
                 previous_position_7 += ', ' + p_c_e_7.inner_text() if p_c_e_7.count() > 0 else ''
                 previous_position_7 += ', ' + p_c_t_e_7.inner_text() if p_c_t_e_7.count() > 0 else ''

                 p_p_e_8 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[9]//h2").first
                 p_c_e_8 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[9]//p[@data-anonymize='company-name']").first
                 p_c_t_e_8 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[9]//span)[1]").first
                 previous_position_8 = p_p_e_8.inner_text() if p_p_e_8.count() > 0 else ''
                 previous_position_8 += ', ' + p_c_e_8.inner_text() if p_c_e_8.count() > 0 else ''
                 previous_position_8 += ', ' + p_c_t_e_8.inner_text() if p_c_t_e_8.count() > 0 else ''

                 p_p_e_9 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[10]//h2").first
                 p_c_e_9 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[10]//p[@data-anonymize='company-name']").first
                 p_c_t_e_9 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[10]//span)[1]").first
                 previous_position_9 = p_p_e_9.inner_text() if p_p_e_9.count() > 0 else ''
                 previous_position_9 += ', ' + p_c_e_9.inner_text() if p_c_e_9.count() > 0 else ''
                 previous_position_9 += ', ' + p_c_t_e_9.inner_text() if p_c_t_e_9.count() > 0 else ''

                 p_p_e_10 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[11]//h2").first
                 p_c_e_10 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[11]//p[@data-anonymize='company-name']").first
                 p_c_t_e_10 = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[11]//span)[1]").first
                 previous_position_10 = p_p_e_10.inner_text() if p_p_e_10.count() > 0 else ''
                 previous_position_10 += ', ' + p_c_e_10.inner_text() if p_c_e_10.count() > 0 else ''
                 previous_position_10 += ', ' + p_c_t_e_10.inner_text() if p_c_t_e_10.count() > 0 else ''

                 # Education expriments
                 edu_element = profile_page.locator("//section[@data-sn-view-name='feature-lead-education']//button").first
                 if edu_element.count() > 0:
                     edu_element.click() 

                 edu_inst_1 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]//h3").first
                 edu_duration_1 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[1]/div/p[2]").first
                 education_exprience_1 = edu_inst_1.inner_text() if edu_inst_1.count() > 0 else ''
                 education_exprience_1 += edu_duration_1.inner_text() if edu_duration_1.count() > 0 else ''

                 edu_inst_2 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]//h3").first
                 edu_duration_2 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[2]/div/p[2]").first
                 education_exprience_2 = edu_inst_2.inner_text() if edu_inst_2.count() > 0 else ''
                 education_exprience_2 += edu_duration_2.inner_text() if edu_duration_2.count() > 0 else ''

                 edu_inst_3 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]//h3").first
                 edu_duration_3 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[3]/div/p[2]").first
                 education_exprience_3 = edu_inst_3.inner_text() if edu_inst_3.count() > 0 else ''
                 education_exprience_3 += edu_duration_3.inner_text() if edu_duration_3.count() > 0 else ''

                 edu_inst_4 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]//h3").first
                 edu_duration_4 = profile_page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul/li)[4]/div/p[2]").first
                 education_exprience_4 = edu_inst_4.inner_text() if edu_inst_4.count() > 0 else ''
                 education_exprience_4 += edu_duration_4.inner_text() if edu_duration_4.count() > 0 else ''

                 # Volunteer expriment
                 voleenteer_class = "//section[@class='MJYNFcHquGiozqlNSusqqnLmXGfMKEpMkaA _card_yg4u9b _container_iq15dg _lined_1aegh9']"
                 volunteer_ele = profile_page.locator(f"{voleenteer_class}//button").first
                 volunteer_ele.click() if volunteer_ele.count() > 0 else None

                 v_e_1 = profile_page.locator(f"({voleenteer_class}//ul/li)[1]").first
                 Volunteering_1 = v_e_1.inner_text().strip().replace('\n', '') if v_e_1.count() > 0 else ''

                 v_e_2 = profile_page.locator(f"({voleenteer_class}//ul/li)[2]").first
                 Volunteering_2 = v_e_2.inner_text().strip().replace('\n', '') if v_e_2.count() > 0 else ''

                 v_e_3 = profile_page.locator(f"({voleenteer_class}//ul/li)[3]").first
                 Volunteering_3 = v_e_3.inner_text().strip().replace('\n', '') if v_e_3.count() > 0 else ''

                 v_e_4 = profile_page.locator(f"({voleenteer_class}//ul/li)[4]").first
                 Volunteering_4 = v_e_4.inner_text().strip().replace('\n', '') if v_e_4.count() > 0 else ''

                 v_e_5 = profile_page.locator(f"({voleenteer_class}//ul/li)[5]").first
                 Volunteering_5 = v_e_5.inner_text().strip().replace('\n', '') if v_e_5.count() > 0 else ''

                 skills = ''
                 get_all_skills = profile_page.locator("//section[@id='skills-section']//li/p")
                 all_skill_elements = get_all_skills.element_handles()
                 for skill in all_skill_elements:
                     skills += skill.inner_text().strip() + ','

                 person_img_ele = profile_page.locator("(//img[@data-anonymize='headshot-photo'])[3]").first
                 person_image = person_img_ele.get_attribute("src") if person_img_ele.count() > 0 else ''

                 # Compnay section
                 c_j_e_1 = profile_page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2").first
                 currrent_job_titles = c_j_e_1.inner_text() if c_j_e_1.count() > 0 else ''
                 # Nagivate Company Page
                 current_company, company_website, Headquarters, industry = '', '', '', ''
                 founded, type, company_linkedin, All_employees, revenue = '', '', '', '', ''
                 company_salse_page = profile_page.locator("((//li[@class='_experience-entry_1irc72'])[1]//a)[1]")
                 if company_salse_page.count() > 0 and company_salse_page.get_attribute('href') != None:
                     company_salse_page_link = company_salse_page.get_attribute('href')
                     profile_page.goto('https://www.linkedin.com' + company_salse_page_link)
                     profile_page.wait_for_load_state('load')
                     sleep(4)
                     current_company_element = profile_page.locator("(//div[@data-anonymize='company-name'])[1]").first
                     current_company = current_company_element.inner_text() if current_company_element.count() > 0 else ''


                     industry_element = profile_page.locator("//span[@data-anonymize='industry']")
                     industry = industry_element.inner_text() if industry_element.count() > 0 else ''

                     All_employees_element = profile_page.locator("//span[@data-anonymize='company-size']").first
                     All_employees = All_employees_element.inner_text() if All_employees_element.count() > 0 else ''

                     revenue_element = profile_page.locator("//span[@data-anonymize='revenue']").first
                     revenue = revenue_element.inner_text() if revenue_element.count() > 0 else ''


                     company_linkedin = '';
                     founded = '';
                     type = '';
                     Headquarters_e = page.locator("(//div[@data-anonymize='location'])[1]")
                     Headquarters = Headquarters_e.inner_text() if Headquarters_e.count() > 0 else ''
                     company_website_e = page.locator("//a[@data-control-name='visit_company_website']")
                     company_website = company_website_e.inner_text() if company_website_e.count() > 0 else ''

                     more_element = profile_page.locator("//button[@aria-label='More options']").first
                     if more_element.count() > 0:
                         more_element.click()
                         context.grant_permissions(permissions=["clipboard-read", "clipboard-write"],
                                                   origin=profile_page.url)
                         copy_element = profile_page.locator("//button[@data-control-name='copy_li_url']").first
                         if copy_element.count() > 0:
                             copy_element.click()
                             company_linkedin = profile_page.evaluate("navigator.clipboard.readText()")


                 dicts = {
                     'full_name': full_name,
                     'first_name': first_name,
                     'last_name': last_name,
                     'location': location,
                     'email': email,
                     'sales_navi_url': sales_navi_url,
                     'normal_linkedin_url': normal_linkedin_url,
                     'headline': headline,
                     'about': about,
                     'currrent_job_titles': currrent_job_titles,
                     'current_company': current_company,
                     'company_website': company_website,
                     'Headquarters': Headquarters,
                     'industry': industry,
                     'founded': founded,
                     'type': type,
                     'company_linkedin': company_linkedin,
                     'All_employees': All_employees,
                     'revenue': revenue,
                     'previous_position_1': previous_position_1,
                     'previous_position_2': previous_position_2,
                     'previous_position_3': previous_position_3,
                     'previous_position_4': previous_position_4,
                     'previous_position_5': previous_position_5,
                     'previous_position_6': previous_position_6,
                     'previous_position_7': previous_position_7,
                     'previous_position_8': previous_position_8,
                     'previous_position_9': previous_position_9,
                     'previous_position_10': previous_position_10,
                     'education_exprience_1': education_exprience_1,
                     'education_exprience_2': education_exprience_2,
                     'education_exprience_3': education_exprience_3,
                     'education_exprience_4': education_exprience_4,
                     'Volunteering_1': Volunteering_1,
                     'Volunteering_2': Volunteering_2,
                     'Volunteering_3': Volunteering_3,
                     'Volunteering_4': Volunteering_4,
                     'Volunteering_5': Volunteering_5,
                     'skills': skills,
                     'person_image': person_image,
                 }

                 dicts_list.append(dicts)

                 header = ['full_name', 'first_name', 'last_name', 'location', 'email', 'sales_navi_url', 'normal_linkedin_url',
                           'headline', 'about', 'currrent_job_titles', 'current_company', 'company_website', 'Headquarters',
                           'industry', 'founded', 'type', 'company_linkedin', 'All_employees', 'revenue', 'previous_position_1',
                           'previous_position_2', 'previous_position_3', 'previous_position_4', 'previous_position_5',
                           'previous_position_6', 'previous_position_7', 'previous_position_8', 'previous_position_9',
                           'previous_position_10', 'education_exprience_1', 'education_exprience_2', 'education_exprience_3',
                           'education_exprience_4', 'Volunteering_1', 'Volunteering_2', 'Volunteering_3', 'Volunteering_4',
                           'Volunteering_5', 'skills', 'person_image']

                 with open(f'{Output_Folder}/data.csv', 'w', newline='', encoding='utf-8') as file:
                     writer = csv.DictWriter(file, fieldnames=header)
                     writer.writeheader()
                     writer.writerows(dicts_list)
                 profile_page.close()
            except Exception as ops:
                 print(f"Error: {ops}")
                 log.insert(END, f"Error: {ops}\n")
                 log.see(END)
            finally:
                pass
            profile_number+=1
            sleep(int(delay))


import concurrent.futures
import os

def scrapper_loop(url, start_page_number, end_page_number, Output_Folder, browser_status, threads, log, scrapermode, start, delay, close_event):
    if not os.path.exists(Output_Folder.strip()):
        os.mkdir(Output_Folder.strip())


    # Validate start and end pages
    try:
        start_page = max(1, min(100, int(start_page_number.strip())))
    except ValueError:
        print('Invalid start Page input..\n\n')
        log.insert(END, 'Invalid start Page input..\n\n')
        log.see(END)
        start_page = 1

    try:
        end_page = max(start_page, min(100, int(end_page_number.strip())))
    except ValueError:
        print('Invalid End Page input..\n\n')
        log.insert(END, 'Invalid End Page input..\n\n')
        log.see(END)
        end_page = 100

    try:
        worker = int(threads)
    except ValueError:
        print('Invalid worker number..\n\n')
        log.insert(END, 'Invalid worker number..\n\n')
        log.see(END)
        worker = 1

    if worker >= end_page:
        log.insert(END, 'Worker can\'t higher than end page..\n\n')
        log.see(END)
        worker = end_page

        # Ensure storage state is valid
    if is_storage_state_valid(storage_state_file):
        page_run = start_page

        # Using ThreadPoolExecutor to manage parallel threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
            while page_run <= end_page:
                if stop_check(close_event.is_set(), log):
                    break  # Stop if the close_event is triggered

                # Collect tasks for the current batch of 5 pages
                futures = []
                for i in range(worker):
                    if stop_check(close_event.is_set(), log):
                        break  # if stop event break loop
                    if page_run <= end_page:
                        log.insert(END, f'Submitting task for Page Number: {page_run + i}\n\n')
                        log.see(END)
                        # Submit profile_scrapping for each page number
                        if scrapermode == "Details":
                            futures.append(executor.submit(profile_scrapping, browser_status, page_run, url, close_event, Output_Folder, delay, log))
                        else:
                            futures.append(executor.submit(quick_scrapping, browser_status, page_run, url, close_event,Output_Folder, delay, log))
                        page_run += 1

                # Wait for all tasks in the batch to complete
                for future in concurrent.futures.as_completed(futures):
                    if stop_check(close_event.is_set(), log):
                        break  # Stop all processing if needed
                    try:
                        future.result()  # Raises exception if any occurred
                    except Exception as e:
                        log.insert(END, f'Error processing page: {str(e)}\n')
                        log.see(END)


            if not close_event.is_set():
                start.configure(text="▶️ Run")
                log.insert(END, f'\nDone.. All {str(end_page)} Pages Processed..\n')
                log.see(END)
    else:
        log.insert(END, 'Please login First..')
        log.see(END)

