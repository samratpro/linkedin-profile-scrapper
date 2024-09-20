from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDMwOTJjNGI3MWE5ODA1NDc3MzBkZGMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NDMwYWEwMmM0NTRiZDE4MTY3YjBkMTQifQ.8Q6PhxlSBksH69FDYs0QmC5UFGGag8AK5tAJjCDkZ4o"
profile_id = "66bf0e8f80ea8e8bbe7b21f2"


gl = GoLogin(
    {
        "token": api_key,
        "profile_id": profile_id
    }
)
test_page = "https://www.linkedin.com/sales/lead/ACwAAAC-ZAsB7KbI93Alb-LQzQW-1Hvug2IsSSg,NAME_SEARCH,Y5c0?_ntb=2Coso1WRQY2frK4vh%2F8BFA%3D%3D"
with sync_playwright() as p:
    debugger_address = gl.start()
    browser = p.chromium.connect_over_cdp("http://" + debugger_address)
    default_context = browser.contexts[0]
    page = default_context.pages[0]

    # Go to the initial URL and wait for the final redirection
    page.goto(test_page)
    page.wait_for_url('https://www.linkedin.com/sales/lead/*')
    sleep(3)
    page.goto(test_page)
    sleep(2)

    volunteer_ele = page.locator(
        "//section[@class='JXXObeeEdgbIezcXzWodRoNsVtFolqJMzCcZ _card_yg4u9b _container_iq15dg _lined_1aegh9']//button")
    volunteer_ele.click() if volunteer_ele.count() > 0 else None

    element = page.locator("(//div[@class='SNhUKTOjVnymxNtvKOiguBSekuvumwLHdA']//ul/li)[1]")
    print(element.inner_text().strip().replace('\n',''))

    sleep(50)

    browser.close()
    gl.stop()