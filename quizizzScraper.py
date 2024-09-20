from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import undetected_chromedriver as uchr

# Initialize the Selenium WebDriver
def init_driver():
    driver = uchr.Chrome(headless=False,use_subprocess=False)
    return driver


def scrape_quizizz_quiz(url):
    driver = init_driver()

    driver.get(url)

    time.sleep(5)

    quiz_title = driver.title #get the title of the quiz

    questions = []

    #find html blocks that contain questions
    question_elements = driver.find_elements(By.CSS_SELECTOR, 'div.p-4.rounded-t-lg.shadow-sm')
    print(len(question_elements))
    for question_element in question_elements:
        try:

            question_text = question_element.find_element(By.CSS_SELECTOR, 'div.question-wrapper.text-sm.flex.overflow-hidden.w-full.text-dark-2.items-center > span > p    ').text.strip()

            choices = []
            choice_elements = question_element.find_elements(By.CSS_SELECTOR, 'span.text-sm.text-dark-2')

            for choice_element in choice_elements:
                choice_text = choice_element.text.strip()
                choices.append(choice_text)
            #get the image if exists
            try:
                image_element = question_element.find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src')
            except:
                image_url = None

            questions.append({
                'question': question_text,
                'choices': choices,
                'image': image_url
            })
        except Exception as e:
            print(f"Error extracting question: {e}")

    quiz_data = {
        'title': quiz_title,
        'questions': questions
    }

    driver.quit()
    return quiz_data


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Quiz saved to {filename}")


if __name__ == "__main__":
    quiz_url = input("Add the link to the quiz: ")
    quiz_data = scrape_quizizz_quiz(quiz_url)

    if quiz_data:
        save_to_json(quiz_data, "quizizz_quiz.json")
