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
            if i == 1:
                page.locator("//div[@class='relative']//ol//li[@class='artdeco-list__item pl3 pv3 '][1]//span[@data-anonymize='person-name']").click()
            page.wait_for_selector("//section[@id='profile-card-section']")
            name = page.locator("//section[@id='profile-card-section']//a[@data-anonymize='person-name']")
            name = name.inner_text() if name.count() > 0 else ''
            print(name)
            button = page.locator('//header[@class="_inline-sidesheet-header_1cn7lg"]//button[2]')
            button.click()
            if button.is_disabled():
                break
            print(i)
            i+=1


    sleep(10)

    page.close()