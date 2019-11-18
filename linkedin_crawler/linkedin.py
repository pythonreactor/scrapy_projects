import csv
import params
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Open a CSV file and write the header line
writer = csv.writer(open(params.result_file, 'w'))
writer.writerow(['name', 'job_title', 'schools', 'location', 'profile_url'])

# Start the chrome driver
driver = webdriver.Chrome('/path/to/chrome/driver')
driver.maximize_window()
# Allow the driver to load the max window
sleep(0.5)

# Get our LinkedIn page
driver.get('https://www.linkedin.com/')
# Allow the driver to sleep so it can properly load everything
sleep(5)

# Now we need to click the 'Sign in' button
driver.find_element_by_xpath('//a[text()="Sign in"]').click()
# Let Selenium load after clicking the Sign in button
sleep(3)

# Enter information into the Email & password field
username_input = driver.find_element_by_name('session_key')
passwd_input = driver.find_element_by_name('session_password')
username_input.send_keys(params.username)
sleep(0.5)
passwd_input = driver.find_element_by_name('session_password')
passwd_input.send_keys(params.passwd)
sleep(0.5)

# Click on the sign in button
driver.find_element_by_xpath('//button[text()="Sign in"]').click()
# Wait for the home page to load
sleep(5)

# We are now going to find profiles to scrape on Google
# Let's get the Google site loaded, and then grab the search input element
driver.get('https://www.google.com')
# Let Google load
sleep(5)

# Now we will grab the search input
search_input = driver.find_element_by_xpath('//input[@name="q"]')

# With the input field, we can input what we want to search
search_input.send_keys(params.search_query)

# Get the search button element and click it
# We need to use '.submit()' because the search button is actually an input, not a button
driver.find_element_by_xpath('//input[@value="Google Search"]').submit()
# OR if we wanted, we could send a 'RETURN' key to press enter for us
# search_input.send_keys(Keys.RETURN)  # But we won't use this here

# We will now grab each profile found in the returned results
# We are grabbing [1] because there are 2 'a' tags associated with each result
profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
# And we will break out the HREF URLs for these profiles
profiles = [profile.get_attribute('href') for profile in profiles]
# Now iterate over each profile and get it, sleep, then scrape
for profile in profiles:
    driver.get(profile)
    sleep(5)
    
    # Create a selector with the profile page's source code
    sel = Selector(text=driver.page_source)
    
    name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
    job_title = sel.xpath('//h2/text()').extrat_first().strip()
    
    schools = ', '.join(sel.xpath('//*[contains('@class, "pv-entity__school-name"')]/text()').extract())
    
    location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
    
    profile_url = driver.current_url
    
    # Try to connect with the account
    try:
        # Connecting with an account that uses the 'more' dropdown to hold 'connect'
        driver.find_element_by_xpath('//*[text()="More..."]').click()
        sleep(1)
        
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(1)
        
        driver.find_element_by_xpath('//*[text()="Send now"]').click()
        sleep(1)
    
    except:
        pass
    
    # Write each data point out (1 row per profile)
    writer.writerow([name, job_title, schools, location, profile_url])


# Close the driver when done
driver.quit()
