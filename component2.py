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



dicts_list = []
def profile_scrapping(browser_status, page_run, url, close_event, Output_Folder, log):
    with sync_playwright() as playwright:
        if browser_status == 'browser show':
            browser = playwright.chromium.launch(
                                                executable_path=str(chrome_path),
                                                 headless=False,
                                                 args=args,
                                                 )
        else:
            browser = playwright.chromium.launch(
                executable_path=str(chrome_path),
                args=args, )
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

            full_name = '';first_name = ''; last_name = ''
            location = ''; email = ''; sales_navi_url = ''
            normal_linkedin_url = ''; headline = ''
            about = ''; currrent_position = ''
            previous_position_1 = '';previous_position_2 = ''
            previous_position_3 = '';previous_position_4 = ''
            previous_position_5 = '';previous_position_6 = ''
            previous_position_7 = '';previous_position_8 = ''
            previous_position_9 = '';previous_position_10 = ''
            education_exprience_1 = ''; education_exprience_2 = ''
            education_exprience_3 = ''; education_exprience_4 = ''
            skills = ''; person_image = ''
            if data == True:
                
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

                 header = ['full_name', 'first_name', 'last_name', 'location', 'email', 'sales_navi_url', 'normal_linkedin_url',
                           'headline', 'about', 'currrent_position','previous_position_1',
                           'previous_position_2', 'previous_position_3', 'previous_position_4', 'previous_position_5',
                           'previous_position_6', 'previous_position_7', 'previous_position_8', 'previous_position_9',
                           'previous_position_10', 'education_exprience_1', 'education_exprience_2', 'education_exprience_3',
                           'education_exprience_4', 'skills', 'person_image']

                 with open(f'{Output_Folder}/data.csv', 'w', newline='', encoding='utf-8') as file:
                     writer = csv.DictWriter(file, fieldnames=header)
                     writer.writeheader()
                     writer.writerows(dicts_list)
        except Exception as ops:
                print(f"Error: {ops}")
                log.insert(END, f"Error: {ops}\n")
                log.see(END)
        finally:
            pass

