import webbrowser

# Open URL in default browser
webbrowser.open("https://stackoverflow.com")

# Open URL in a new window
webbrowser.open_new("https://stackoverflow.com")

# Open URL in a new tab
webbrowser.open_new_tab("https://stackoverflow.com")

# Open URL using a specific browser (if registered)
chrome = webbrowser.get('chrome')
chrome.open("https://stackoverflow.com")
