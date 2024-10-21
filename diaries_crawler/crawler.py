from playwright.sync_api import sync_playwright, Page
from datetime import datetime
import locale


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class DiaryCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url


    def handle_calendar_title(self, title: str) -> tuple[str, int]:
        month = title.split()[0]
        year = int(title.split()[-1])

        return month, year


    def month_to_int(self, month_name: str) -> int:
        return datetime.strptime(month_name.capitalize(), "%B").month


    def handle_calendar_date(self, page: Page, publication_date: str) -> None:
        formatted_date = datetime.strptime(publication_date, "%Y-%m-%d")
        target_month = formatted_date.strftime('%B').lower()  
        target_year = formatted_date.year

        calendar_title = '.lauren-calendartitle'
        prev_button = '.lauren-prev'
        next_button = '.lauren-next'
        
        try:
            page.wait_for_selector(calendar_title)

            current_title = page.locator(calendar_title).inner_text().strip().lower()
            current_month, current_year = self.handle_calendar_title(current_title)
            
            while (current_month != target_month or current_year != target_year):

                if (current_year > target_year or 
                (current_year == target_year and self.month_to_int(current_month) > formatted_date.month)):
                    page.click(prev_button)
                else:
                    page.click(next_button)

                page.wait_for_timeout(500)
                current_title = page.locator(calendar_title).inner_text().strip().lower()
                current_month, current_year = self.handle_calendar_title(current_title)


        except TimeoutError:
            print("Erro: O calendário não foi carregado a tempo.")


    def handle_pdf_url(self, page: Page, formatted_date: str):
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


    def search_diaries(self, publication_date: str) -> str | None:
        year, month, day = map(int, publication_date.split('-'))
        formatted_date = f"{year}-{month-1}-{day}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.base_url)

            page.wait_for_timeout(5000)

            self.handle_calendar_date(page, publication_date)


            try:
                pdf_url = self.handle_pdf_url(page, formatted_date)
                return pdf_url  
                
            except Exception as error:
                print(f"Erro ao buscar o diário: {error}")
                return None
            
            finally:
                browser.close()


    def run(self, publication_date: str):

        url = self.search_diaries(publication_date)

        return url


