import requests
from bs4 import BeautifulSoup

def parse_git_docs():
    url = "https://devdocs.io/git/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Парсинг заголовка
        title = soup.find('title').get_text()
        print(f"Documentation: {title}")
        
        # Парсинг быстрых ссылок
        quickref = soup.find('div', class_='callout quickref')
        if quickref:
            print("\nQuick Reference Guides:")
            for link in quickref.find_all('a'):
                print(f"  - {link.get_text(strip=True)}: {link['href']}")
        
        # Парсинг основных команд
        print("\nMain Commands:")
        sections = soup.find_all('div', class_=['column-left', 'column-right'])
        
        for section in sections:
            section_title = section.find('h3').get_text(strip=True)
            print(f"\n  {section_title}:")
            
            commands = section.find_all('a')
            for cmd in commands:
                cmd_name = cmd.get_text(strip=True)
                cmd_link = "https://devdocs.io" + cmd['href'] if cmd['href'].startswith('/') else cmd['href']
                print(f"    - {cmd_name}: {cmd_link}")
        
        # Парсинг атрибуции
        attribution = soup.find('div', class_='_attribution')
        if attribution:
            print("\nAttribution:")
            print("  " + attribution.get_text(separator='\n  ', strip=True))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_git_docs()