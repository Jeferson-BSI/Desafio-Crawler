from playwright.sync_api import sync_playwright, Page
from datetime import datetime
import requests
import hashlib
import locale
import os
import sys


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

BASE_URL = "https://www.tjro.jus.br/diario_oficial/"

def handle_calendar_title(title: str) -> tuple[str, int]:
    month = title.split()[0]
    year = int(title.split()[-1])

    return month, year


def month_to_int(month_name: str) -> int:
    return datetime.strptime(month_name.capitalize(), "%B").month


def handle_calendar_date(page: Page, publication_date: str) -> None:
    formatted_date = datetime.strptime(publication_date, "%Y-%m-%d")
    target_month = formatted_date.strftime('%B').lower()  
    target_year = formatted_date.year

    calendar_title = '.lauren-calendartitle'
    prev_button = '.lauren-prev'
    next_button = '.lauren-next'
    
    try:
        page.wait_for_selector(calendar_title)

        current_title = page.locator(calendar_title).inner_text().strip().lower()
        current_month, current_year = handle_calendar_title(current_title)
        
        while (current_month != target_month or current_year != target_year):

            if (current_year > target_year or 
               (current_year == target_year and month_to_int(current_month) > formatted_date.month)):
                page.click(prev_button)
            else:
                page.click(next_button)

            page.wait_for_timeout(500)
            current_title = page.locator(calendar_title).inner_text().strip().lower()
            current_month, current_year = handle_calendar_title(current_title)


    except TimeoutError:
        print("Erro: O calendário não foi carregado a tempo.")


def handle_pdf_url(page: Page, formatted_date: str):
    day_button_selected = page.locator(f"button[data-date='{formatted_date}'][data-url]")
    
    if day_button_selected:
        pdf_url = day_button_selected.get_attribute("data-url")


        if pdf_url:
            full_pdf_url = f"https://www.tjro.jus.br{pdf_url}"

            return full_pdf_url
        else:
            print("Nenhum PDF encontrado para a data fornecida.")

            return None
    else:
        print(f"Nenhum diário encontrado para a data {formatted_date}.")

        return None


def search_diaries(publication_date: str, base_url: str) -> str | None:
    year, month, day = map(int, publication_date.split('-'))
    formatted_date = f"{year}-{month-1}-{day}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url)

        page.wait_for_timeout(5000)

        handle_calendar_date(page, publication_date)


        try:
            pdf_url = handle_pdf_url(page, formatted_date)
            return pdf_url  
            
        except Exception as error:
            print(f"Erro ao buscar o diário: {error}")
            return None
        
        finally:
            browser.close()


def download_pdf(response: requests.Response, output_folder: str , pdf_filename: str ) -> str | None:
    try:
        os.makedirs(output_folder, exist_ok=True)

        pdf_path = os.path.join(output_folder, f'{pdf_filename}.pdf')

        
        response.raise_for_status()  

        with open(pdf_path, "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)

        return pdf_path

    except requests.exceptions.RequestException as error:
        print(f"Erro ao baixar o PDF: {error}")
        return None


def handle_hash_md5(pdf_url: str) -> str:
    response = requests.get(pdf_url, stream=True)
    
    hash_md5 = hashlib.md5(response.content).hexdigest()
    download_pdf(response, 'pdf', hash_md5)

    return hash_md5


def main():
    if len(sys.argv) != 2:
        print("Uso: python script.py <data>")
        sys.exit(1)

    data = sys.argv[1]
    
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Data inválida. Use o formato YYYY-MM-DD.")
        sys.exit(1)


    url = search_diaries(data, BASE_URL)

    if url:
       hash_md5 = handle_hash_md5(url)
       
       if hash_md5:
            print(f"Hash MD5 do diário: {hash_md5}")


if __name__ == "__main__":
    main()