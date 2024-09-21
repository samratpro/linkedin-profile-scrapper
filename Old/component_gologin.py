from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright
import os
import csv
from customtkinter import *


# Define a function that opens the browser and returns the browser and contex

def scrapper_loop(api_key, profile_id, url, start_page_number, end_page_number, Output_Folder, log):
    if not os.path.exists(Output_Folder.strip()):
        os.mkdir(Output_Folder.strip())

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

    dicts_list = []

    page_run = start_page
    while page_run <= end_page:
        gl = GoLogin({"token": api_key, "profile_id": profile_id})
        with sync_playwright() as p:
            debugger_address = gl.start()
            browser = p.chromium.connect_over_cdp("http://" + debugger_address)
            default_context = browser.contexts[0]
            page = default_context.pages[0]

            print('Running Page Number : ', page_run)
            log.insert(END, f'Running Page Number : {str(page_run)}\n\n')
            log.see(END)
            page.goto(url.strip().replace('query=', f'page={str(page_run)}&query='))
            page.wait_for_load_state('load')

            scroll = 3
            while scroll < 26:
                try:
                    locator = page.locator(f"(//li[contains(@class,'artdeco-list__item pl3 pv3')])[{str(scroll)}]")
                    locator.click()
                except Exception as e:
                    print(f"Error during scrolling: {e}")
                    log.insert(END, f"Error during scrolling: {e}\n")
                    log.see(END)
                scroll += 3

            all_element_links = page.locator("//a[@data-view-name='search-results-lead-name']")
            all_links = all_element_links.element_handles()
            get_profile_list = ['https://www.linkedin.com' + str(link.get_attribute('href')) for link in all_links]

            browser.close()
            gl.stop()
            log.insert(END, f'No. {str(page_run)}. Page\'s all profile Link has been scrapped\n')
            log.see(END)
            sleep(5)

        data_test = 25
        profile_number = 0
        all_page_scrapped = True
        while profile_number < len(get_profile_list[:data_test]):

            gl = GoLogin({"token": api_key, "profile_id": profile_id})
            with sync_playwright() as p:
                debugger_address = gl.start()
                browser = p.chromium.connect_over_cdp("http://" + debugger_address)
                default_context = browser.contexts[0]
                page = default_context.pages[0]


                while True:
                    print(profile_number+1)
                    log.insert(END,f'Data No. {str(profile_number+1)}\n')
                    log.see(END)
                    sales_navi_url = get_profile_list[profile_number]

                    try:
                        page.goto(sales_navi_url)
                        page.wait_for_url('https://www.linkedin.com/sales/lead/*')
                        sleep(7)

                        # Collect profile data
                        full_name = page.locator("(//h1[@class='_headingText_e3b563 _default_1i6ulk _sizeXLarge_e3b563'])[1]").inner_text(timeout=5000) or ''
                        if full_name != None:
                            first_name = full_name.split(' ')[0]
                            last_name = full_name.split(' ')[1]
                        else:
                            first_name = ''
                            last_name = ''

                        normal_linkedin_url = ''
                        toggle_button = page.locator("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n']")
                        if toggle_button.count() > 0:
                            toggle_button.click()
                            linkedin_link_element = page.locator("//a[@class='ember-view _item_1xnv7i']")
                            if linkedin_link_element.count() > 0:
                                normal_linkedin_url = linkedin_link_element.get_attribute('href') or ''

                        headline = page.locator("//span[@data-anonymize='headline']").inner_text() or ''

                        location_element = page.locator("((//section[@class='_header_sqh8tm']//div)[9]//div)[1]")
                        location = location_element.inner_text() if location_element.count() > 0 else ''

                        email_element = page.locator("span[data-anonymize='email']")
                        email = email_element.inner_text() if email_element.count() > 0 else ''

                        about_element = page.locator("//section[@id='about-section']/div")
                        about = about_element.get_attribute("title") if about_element.count() > 0 else ''

                        # Click on expriment element
                        exprience_element = page.locator("//section[@id='scroll-to-experience-section']//button")
                        exprience_element.click() if exprience_element.count() > 0 else None

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
                        edu_element.click() if edu_element.count() > 0 else None

                        edu_1 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul//li)[1]")
                        education_exprience_1 = edu_1.inner_text().strip().replace('\n','') if edu_1.count() > 0 else ''

                        edu_2 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul//li)[1]")
                        education_exprience_2 = edu_2.inner_text().strip().replace('\n','') if edu_2.count() > 0 else ''

                        edu_3 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul//li)[1]")
                        education_exprience_3 = edu_3.inner_text().strip().replace('\n','') if edu_3.count() > 0 else ''

                        edu_4 = page.locator("(//section[@data-sn-view-name='feature-lead-education']//ul//li)[1]")
                        education_exprience_4 = edu_4.inner_text().strip().replace('\n','') if edu_4.count() > 0 else ''

                        # Volunteer expriment
                        voleenteer_class = "//section[@class='MJYNFcHquGiozqlNSusqqnLmXGfMKEpMkaA _card_yg4u9b _container_iq15dg _lined_1aegh9']"
                        volunteer_ele = page.locator(f"{voleenteer_class}//button")
                        volunteer_ele.click() if volunteer_ele.count() > 0 else None

                        v_e_1 = page.locator(f"({voleenteer_class}//ul/li)[1]")
                        Volunteering_1 = v_e_1.inner_text().strip().replace('\n','') if v_e_1.count() > 0 else ''

                        v_e_2 = page.locator(f"({voleenteer_class}//ul/li)[2]")
                        Volunteering_2 = v_e_2.inner_text().strip().replace('\n','') if v_e_2.count() > 0 else ''

                        v_e_3 = page.locator(f"({voleenteer_class}//ul/li)[3]")
                        Volunteering_3 = v_e_3.inner_text().strip().replace('\n','') if v_e_3.count() > 0 else ''

                        v_e_4 = page.locator(f"({voleenteer_class}//ul/li)[4]")
                        Volunteering_4 = v_e_4.inner_text().strip().replace('\n','') if v_e_4.count() > 0 else ''

                        v_e_5 = page.locator(f"({voleenteer_class}//ul/li)[5]")
                        Volunteering_5 = v_e_5.inner_text().strip().replace('\n','') if v_e_5.count() > 0 else ''

                        skills = ''
                        get_all_skills = page.locator("//section[@id='skills-section']//li/p")
                        all_skill_elements = get_all_skills.element_handles()
                        for skill in all_skill_elements:
                            skills += skill.inner_text().strip() + ','

                        person_img_ele = page.locator("(//img[@data-anonymize='headshot-photo'])[3]")
                        person_image = person_img_ele.get_attribute("src") if person_img_ele.count() > 0 else ''


                        # Compnay section
                        c_j_e_1 = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2")
                        currrent_job_titles = c_j_e_1.inner_text() if c_j_e_1.count() > 0 else ''
                        # Nagivate Company Page
                        company_salse_page = page.locator("((//li[@class='_experience-entry_1irc72'])[1]//a)[1]")
                        if company_salse_page.count() > 0 and company_salse_page.get_attribute('href') != None:
                            company_salse_page_link = company_salse_page.get_attribute('href')
                            page.goto('https://www.linkedin.com'+company_salse_page_link)
                            page.wait_for_load_state('load')
                            sleep(4)
                            current_company_element = page.locator("(//div[@data-anonymize='company-name'])[1]")
                            current_company = current_company_element.inner_text() if current_company_element.count() > 0 else ''
                            industry_element = page.locator("//span[@data-anonymize='industry']")
                            industry = industry_element.inner_text() if industry_element.count() > 0 else ''

                            All_employees_element = page.locator("//span[@data-anonymize='company-size']")
                            All_employees = All_employees_element.inner_text() if All_employees_element.count() > 0 else ''

                            revenue_element = page.locator("//span[@data-anonymize='revenue']")
                            revenue = revenue_element.inner_text() if revenue_element.count() > 0 else ''


                            company_website = '';
                            company_linkedin = '';founded = '';type = '';Headquarters = '';
                            more_element = page.locator("//button[@aria-label='More options']")
                            if more_element.count() > 0:
                                more_element.click()
                                default_context.grant_permissions(permissions=["clipboard-read", "clipboard-write"],
                                                                  origin=page.url)
                                copy_element = page.locator("//button[@data-control-name='copy_li_url']")
                                if copy_element.count() > 0:
                                    copy_element.click()
                                    company_linkedin = page.evaluate("navigator.clipboard.readText()")

                            if more_element.count() > 0:
                                more_element.click()
                                details_panel = page.locator("//button[@data-control-name='open_account_details']")
                                if details_panel.count() > 0:
                                    details_panel.click()
                                    sleep(1)
                                    company_website_e = page.locator("span[data-anonymize='url']")
                                    company_website = company_website_e.inner_text() if company_website_e.count() > 0 else ''
                                    Headquarters_e = page.locator("dd[data-anonymize='address']")
                                    Headquarters = Headquarters_e.inner_text() if Headquarters_e.count() > 0 else ''
                                    type_e = page.locator("//dd[@class='company-details-panel__content company-details-panel-type t-black--light']")
                                    type = type_e.inner_text() if type_e.count() > 0 else ''
                                    founded_e = page.locator("//dd[@class='company-details-panel__content company-details-panel-founded t-black--light']")
                                    founded = founded_e.inner_text() if founded_e.count() > 0 else ''

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
                            'company_website':company_website,
                            'Headquarters':Headquarters,
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

                        header = ['full_name','first_name','last_name','location','email','sales_navi_url','normal_linkedin_url',
                                  'headline','about','currrent_job_titles','current_company','company_website','Headquarters',
                                  'industry','founded','type','company_linkedin','All_employees','revenue','previous_position_1',
                                  'previous_position_2','previous_position_3','previous_position_4','previous_position_5',
                                  'previous_position_6','previous_position_7','previous_position_8','previous_position_9',
                                  'previous_position_10','education_exprience_1','education_exprience_2','education_exprience_3',
                                  'education_exprience_4','Volunteering_1','Volunteering_2','Volunteering_3','Volunteering_4',
                                  'Volunteering_5','skills','person_image']

                        with open(f'{Output_Folder}/data.csv', 'w', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=header)
                            writer.writeheader()
                            writer.writerows(dicts_list)

                        sleep(3)
                        profile_number += 1
                        if profile_number == data_test:
                            break

                    except Exception as ops:
                        print(f"Error: {ops}")
                        log.insert(END, f"Error: {ops}\n")
                        log.see(END)
                        log.insert(END, f"Don't worry! please wait,,browser is opening again...\n")
                        log.see(END)
                        sleep(5)
                        all_page_scrapped = False
                        break
                try:
                    browser.close()
                    gl.stop()
                except Exception as ops:
                    log.insert(END, f'Browser Close error : {str(ops)}\n')
                    log.see(END)
                sleep(3)
                if(all_page_scrapped==True):
                    log.insert(END, f'No. {str(page_run)}. Page\'s all data has been scrapped\n\n')
                log.see(END)
        page_run += 1
    print(f'Done.. All {str(end_page)} Pages Processed..\n\n')
    log.insert(END, f'Done.. All {str(end_page)} Pages Processed..\n\n')
    log.see(END)