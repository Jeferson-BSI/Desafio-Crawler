import requests
import hashlib
import os


class HashMd5Handle():

    def download_pdf(self, response: requests.Response, output_folder: str , pdf_filename: str ) -> str | None:
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


    def handle_hash_md5(self, pdf_url: str) -> str:
        response = requests.get(pdf_url, stream=True)
        
        hash_md5 = hashlib.md5(response.content).hexdigest()
        self.download_pdf(response, 'pdf', hash_md5)

        return hash_md5


    def run(self, url: str):
        return self.handle_hash_md5(url)

