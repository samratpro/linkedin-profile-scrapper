import asyncio
from playwright.async_api import async_playwright

semaphore = asyncio.Semaphore(2)  # Create a semaphore to limit concurrency
async def visit_link(semaphore, context, link):
    async with semaphore:  # Limit the number of concurrent tasks
        try:
            page = await context.new_page()  # Create a new page (tab) for each link
            await page.goto(link)
            print(f"Visited: {link}")
            await page.close()  # Close the page after visiting
        except Exception as e:
            print(f"Error visiting {link}: {e}")
async def main(links):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)  # Change to headless=True if needed
        context = await browser.new_context()
        tasks = []
        for link in links:
            task = visit_link(semaphore, context, link)  # Pass semaphore to the visit function
            tasks.append(task)
        # Run tasks concurrently
        await asyncio.gather(*tasks)
        await context.close()  # Close the context after all tasks are done
        await browser.close()  # Close the browser

links = ["https://www.linkedin.com/","https://www.linkedin.com/help/linkedin","https://www.linkedin.com/feed/",]
asyncio.run(main(links))