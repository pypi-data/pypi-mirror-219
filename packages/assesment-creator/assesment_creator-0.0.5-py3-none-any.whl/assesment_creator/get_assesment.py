from assesment_creator.cutom_exception import InvalidURLException
from assesment_creator.helper import output_file, create_docx
from ensure import ensure_annotations
import re
import requests
from bs4 import BeautifulSoup
from time import sleep

# url= "https://docs.google.com/forms/d/1WLfwaz1fuiueMGE8iEigwjZSP2HEUPGlyIWE9QNYhpg/edit"


@ensure_annotations
def get_data(link: str) -> list:
    page = requests.get(link)
    sleep(3)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find_all(class_="geS5n")
    content = [pair for pair in content]
    content = str(content)
    mixed_pattern = r'M7eMe">(.*?)\<|auto">(.*?)\<\/span>'
    qno_list = re.findall(mixed_pattern, content)
    if len(qno_list)==0:
        raise InvalidURLException(
                    "No data found! Please check the link provided"
                )
    else:
        return qno_list


@ensure_annotations
def create_assesment(form_link: str, file_name: str) -> str:
    try:
        if form_link and file_name is not None:
            output_file(file_name)
            content_list = get_data(form_link)
            ans = create_docx(content_list, file_name)
            if ans is not None:
                return f"Scraping done successfully! Check {file_name} 😀 Thank you!"
            else:
                raise InvalidURLException(
                    "No data found! Please check the link provided"
                )
        else:
            return "Url or file_name cannot be empty"

    except Exception as e:
        raise e
