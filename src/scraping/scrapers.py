class WebScraper:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch_data(self):
        import requests
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.text
        else:
            raise Exception(f"Failed to fetch data from {self.url}")

    def parse_data(self):
        from bs4 import BeautifulSoup
        if self.data is None:
            raise Exception("No data to parse. Please fetch data first.")
        soup = BeautifulSoup(self.data, 'html.parser')
        # Example parsing logic (to be customized based on the target website)
        parsed_data = []
        for item in soup.find_all('div', class_='item'):
            title = item.find('h2').text
            link = item.find('a')['href']
            parsed_data.append({'title': title, 'link': link})
        return parsed_data