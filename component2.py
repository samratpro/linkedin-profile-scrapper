from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright
import os
import csv


# Define a function that opens the browser and returns the browser and contex

def scrapper_loop(api_key, profile_id, url, start_page_number, end_page_number, Output_Folder, log):
    if not os.path.exists(Output_Folder.strip()):
        os.mkdir(Output_Folder.strip())

    try:
        start_page = max(1, min(100, int(start_page_number.strip())))
    except ValueError:
        print('Invalid start Page input..\n\n')
        log.insert('1.0', 'Invalid start Page input..\n\n')
        start_page = 1

    try:
        end_page = max(start_page, min(100, int(end_page_number.strip())))
    except ValueError:
        print('Invalid End Page input..\n\n')
        log.insert('1.0', 'Invalid End Page input..\n\n')
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
            log.insert('1.0', f'Running Page Number : {str(page_run)}\n\n')
            page.goto(url.strip().replace('query=', f'page={str(page_run)}&query='), timeout=60000)
            page.wait_for_load_state('load')

            scroll = 3
            while scroll < 26:
                try:
                    locator = page.locator(f"(//li[contains(@class,'artdeco-list__item pl3 pv3')])[{str(scroll)}]")
                    locator.click()
                except Exception as e:
                    print(f"Error during scrolling: {e}")
                    log.insert('1.0', f"Error during scrolling: {e}\n")
                scroll += 3

            all_element_links = page.locator("//a[@data-view-name='search-results-lead-name']")
            all_links = all_element_links.element_handles()
            get_profile_list = ['https://www.linkedin.com' + str(link.get_attribute('href')) for link in all_links]

            sleep(2)


            number = 0
            while number < len(get_profile_list):
                print(number+1)
                log.insert('1.0',f'{str(number+1)}\n')
                sleep(2)
                sales_navi_url = get_profile_list[number]

                try:
                    page.goto(sales_navi_url, timeout=60000)  # 60 seconds timeout
                    page.wait_for_load_state("load")
                    sleep(1)

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

                    location_element = page.locator("(//div[@class='bbHcqdaCbexutPhdTQasEfJqYYXFTztTJdI']/div)[1]")
                    location = location_element.inner_text() if location_element.count() > 0 else ''

                    # connection_element = page.locator("(//div[@class='bbHcqdaCbexutPhdTQasEfJqYYXFTztTJdI']/div)[2]")
                    # connection = connection_element.inner_text() if connection_element.count() > 0 else ''
                    #
                    # facebook, twitter, website = '', '', ''
                    # contact_button = page.locator(
                    #     "//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _emphasized_ps32ck _left_ps32ck _container_iq15dg contact-info-cta _inset-none_sfmhx2']")
                    # if contact_button.count() > 0:
                    #     contact_button.click()
                    #     sleep(0.5)
                    #     get_all_links = page.locator("//a[@class='link-without-visited-state']")
                    #     all_link_elements = get_all_links.element_handles()
                    #     for link in all_link_elements:
                    #         href = link.get_attribute('href') or ''
                    #         if 'facebook' in href:
                    #             facebook = href
                    #         elif 'twitter' in href:
                    #             twitter = href
                    #         else:
                    #             website = href
                    #
                    # phone_element = page.locator("(//a[@data-anonymize='phone'])[1]")
                    # phone = phone_element.inner_text() if phone_element.count() > 0 else ''
                    #
                    # email_element = page.locator("(//a[@data-anonymize='email'])[1]")
                    # email = email_element.inner_text() if email_element.count() > 0 else ''

                    skills = ''
                    get_all_skills = page.locator("//section[@id='skills-section']//li/p")
                    all_skill_elements = get_all_skills.element_handles()
                    for skill in all_skill_elements:
                        skills += skill.inner_text().strip() + ','

                    company_name_element = page.locator("(//p[@data-anonymize='company-name'])[1]")
                    company_name = company_name_element.inner_text() if company_name_element.count() > 0 else ''

                    company_link_element = page.locator("((//li[@class='_experience-entry_1irc72'])[1]//p)[3]")
                    company_link = 'https://www.linkedin.com' + (company_link_element.get_attribute(
                        'href') or '') if company_link_element.count() > 0 else ''

                    job_role_element = page.locator("(//li[@class='_experience-entry_1irc72'])[1]//h2")
                    job_role = job_role_element.inner_text() if job_role_element.count() > 0 else ''


                    # Compnay section
                    currrent_job_titles = ''
                    current_company = ''
                    industry = ''
                    company_linkedin = ''
                    All_employees = ''
                    revenue = ''
                    Twitter = ''


                    company_location_element = page.locator("(//div[@class='TbKcSJIQUHRIWdFBbQJGxCuRBySCGgJI '])[1]//p[2]")
                    company_location = company_location_element.inner_text() if company_location_element.count() > 0 else ''


                    dicts = {
                        'full_name': full_name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'location': location,
                        'sales_navi_url': sales_navi_url,
                        'normal_linkedin_url': normal_linkedin_url,
                        'headline': headline,
                        'about': about,
                        'currrent_job_titles': currrent_job_titles,
                        'current_company': current_company,
                        'industry': industry,
                        'company_linkedin': company_linkedin,
                        'All_employees': All_employees,
                        'revenue': revenue,
                        'Twitter': Twitter,
                        'previous_position_1': previous_position_1,
                        'previous_position_2': previous_position_2,
                        'previous_position_3': previous_position_3,
                        'previous_position_4': previous_position_4,
                        'previous_position_5': previous_position_5,
                        'education_experience': education_experience,
                        'Volunteering_1': Volunteering_1,
                        'Volunteering_2': Volunteering_2,
                        'Volunteering_3': Volunteering_3,
                        'skills': skills,
                        'person_image': person_image,
                    }

                    dicts = {
                        'salse_link': salse_link,
                        'name': name,
                        'linkedin_link': linkedin_link,
                        'headline': headline,
                        'location': location,
                        'connection': connection,
                        'facebook': facebook,
                        'twitter': twitter,
                        'website': website,
                        'phone': phone,
                        'email': email,
                        'skills': skills,
                        'company_name': company_name,
                        'company_link': company_link,
                        'job_role': job_role,
                        'company_location': company_location
                    }
                    dicts_list.append(dicts)

                    header = ['full_name','first_name','last_name','location','sales_navi_url',
                              'normal_linkedin_url','headline','about','currrent_job_titles','current_company',
                              'industry','company_linkedin','All_employees','revenue','Twitter','previous_position_1',
                              'previous_position_2','previous_position_3','previous_position_4','previous_position_5',
                              'education_experience','Volunteering_1','Volunteering_2','Volunteering_3',
                              'skills','person_image']

                    header = ['salse_link', 'name', 'linkedin_link', 'headline', 'location', 'connection',
                              'facebook', 'twitter', 'website', 'phone', 'email', 'skills',
                              'company_name', 'company_link', 'job_role', 'company_location']

                    with open(f'{Output_Folder}/data.csv', 'w', newline='', encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=header)
                        writer.writeheader()
                        writer.writerows(dicts_list)

                    number += 1
                    sleep(1)

                except Exception as ops:
                    print(f"Error: {ops}")
                    log.insert('1.0', f"Error: {ops}\n")
                    sleep(1)

            browser.close()
            gl.stop()
            sleep(2)

        page_run += 1

        log.insert('1.0', f'1 second Pause..\n\n')

    print(f'Done.. All {str(end_page)} Pages Processed..\n\n')
    log.insert('1.0', f'Done.. All {str(end_page)} Pages Processed..\n\n')
