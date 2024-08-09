from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

from chromedriver_py import binary_path # this will get you the path variable

def truncate(text, n):
    words = text.split()
    if len(words) <= n:
        return text
    truncated = ' '.join(words[:n])
    return truncated[:truncated.rfind('.')] + '.'


def get_input_selector(driver):
    # Pause pour que la page se charge
    time.sleep(1)

    placeholder_text = 'To rewrite text, enter or paste it here and press "Paraphrase."'
    input_selectors = [
        '#inputText',
        '#paraphraser-input-box',
        f'div[placeholder="{placeholder_text}"]'
    ]

    for selector in input_selectors:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            print(f'Success: Found element with selector {selector}')
            return selector
        except TimeoutException:
            print(f'Selector {selector} not found.')
            continue
        except Exception as e:
            print(f'Error finding selector {selector}: {e}')
            continue

    print('Error: Unable to find a valid input selector.')
    # Optionally save page source and screenshot for debugging
    with open('page_source.html', 'w') as file:
        file.write(driver.page_source)
    driver.save_screenshot('debug_screenshot.png')
    return None

def get_input_field(driver, input_selector):
    try:
        input_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, input_selector))
        )
        return input_field
    except:
        print(f'Error: Unable to find the input field with the selector: {input_selector}')
        return None

def clear_input_field(driver, input_selector):
    input_field = driver.find_element(By.CSS_SELECTOR, input_selector)
    input_field.clear()

    input_field.send_keys(Keys.CONTROL, 'a')
    input_field.send_keys(Keys.BACKSPACE)

def input_string(driver, input_selector, text):
    input_field = driver.find_element(By.CSS_SELECTOR, input_selector)
    input_field.send_keys(text)

def get_button_selector(driver):
    button_selectors = [
        'button.quillArticleBtn',
        '[aria-label="Rephrase (Cmd + Return)"] button',
        '[aria-label="Paraphrase (Cmd + Return)"] button',
        "//div[contains(text(), 'Paraphrase') or contains(text(), 'Rephrase')]/ancestor::button"
    ]
    for selector in button_selectors:
        try:
            if selector.startswith("//"):
                button = driver.find_element(By.XPATH, selector)
            else:
                button = driver.find_element(By.CSS_SELECTOR, selector)
            return selector
        except:
            continue
    print('Error: Unable to find a valid button selector.')
    return None

def click_paraphrase_button(driver, button_selector):
    try:
        if button_selector.startswith("//"):
            button = driver.find_element(By.XPATH, button_selector)
        else:
            button = driver.find_element(By.CSS_SELECTOR, button_selector)
        button.click()
        return True
    except:
        return False

def wait_for_form_submission(driver, button_selector):
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, f'{button_selector} div:nth-child(2)'))
        )
        return True
    except:
        print('Error: Process did not complete in the expected time.')
        return False

def get_output_content(driver, output_selector):
    try:
        content = driver.find_element(By.CSS_SELECTOR, output_selector).text
        if not content:
            print('Output element not found or no content.')
            return None
        return content
    except Exception as e:
        print(f'Error retrieving output content: {e}')
        return None

def quillbot(text, options=None):
    if options is None:
        options = {}

    number_of_characters = 125
    parts = []
    output = ''
    
    if len(text.split()) > number_of_characters:
        while len(text.split()) > number_of_characters:
            part = truncate(text, number_of_characters)
            text = text[len(part):].strip()
            parts.append(part)
        parts.append(text)
    else:
        parts.append(text)


    chrome_options = Options()
    headless = options['headless']
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Optional: for GPU acceleration issues
    chrome_options.add_argument("--no-sandbox")  # Optional: for sandbox issues
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: to deal with memory issues

    # Specify the path to your chromedriver if necessary
    service = Service(executable_path=binary_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)


    #driver = webdriver.Chrome()
    driver.get('https://quillbot.com/paraphrasing-tool')

    try:
        input_selector = get_input_selector(driver)
        input_field = get_input_field(driver, input_selector)

        if not input_field:
            print('Input field not found. Exiting script.')
            return

        for i, part in enumerate(parts):
            print(f'Paraphrasing part {i + 1} of {len(parts)}')

            time.sleep(1)
            clear_input_field(driver, input_selector)
            time.sleep(1)
            input_string(driver, input_selector, part)
            time.sleep(1)

            button_selector = get_button_selector(driver)
            if not click_paraphrase_button(driver, button_selector):
                print('Form submission failed. Exiting script.')
                return

            if not wait_for_form_submission(driver, button_selector):
                print('Form submission failed. Exiting script.')
                return

            output_content = get_output_content(driver, '#paraphraser-output-box')
            if output_content:
                output += output_content
            else:
                print('Output content not found. Exiting script.')
                return

            print(f'Paraphrasing complete {i + 1} of {len(parts)}')
            time.sleep(1)

        print('Paraphrasing complete')
        return output

    finally:
        driver.quit()
