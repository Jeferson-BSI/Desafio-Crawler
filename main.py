from datetime import datetime
import sys

from diaries_crawler.crawler import DiaryCrawler
from diaries_crawler.hash_md5 import HashMd5Handle


BASE_URL = "https://www.tjro.jus.br/diario_oficial/"


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

    crawler = DiaryCrawler(BASE_URL)
    url = crawler.run(data)


    md5 = HashMd5Handle()

    if url:
       hash_md5 = md5.run(url)
       
       if hash_md5:
            print(f"Hash MD5 do diário: {hash_md5}")


if __name__ == "__main__":
    main()