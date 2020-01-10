import selenium.webdriver as driver

driver_path = "D:\Mike_workshop\driver\geckodriver.exe"
headless = driver.FirefoxOptions()
headless.add_argument("-headless")  # 無頭模式
headless.set_preference('permissions.default.image', 2)
profile = driver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", '127.0.0.1')
profile.set_preference("network.proxy.socks_port", 9150)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()

url = "https://tw.nextmgz.com/realtimenews/news/488156"
browser = driver.Firefox(executable_path=driver_path, firefox_profile=profile, options=headless)
browser.get(url)

print(browser.page_source)

browser.close()
browser.quit()