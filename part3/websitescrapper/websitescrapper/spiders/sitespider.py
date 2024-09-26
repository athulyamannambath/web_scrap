import scrapy
import json

class SitespiderSpider(scrapy.Spider):
    name = "sitespider"
    allowed_domains = ["bhhsamb.com"]

    # Start URL for the API
    api_url = "https://www.bhhsamb.com/CMS/CmsRoster/RosterSearchResults"
    page_number = 1
    page_size = 100
    total_pages = 10  # Update this once you know the total number of pages

    def start_requests(self):
        # Build the API request for the first page
        url = f"{self.api_url}?layoutID=963&pageSize={self.page_size}&pageNumber={self.page_number}&sortBy=random"
        
        headers = {
            'Cookie': 'culture=en',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6',
            'Referer': 'https://www.bhhsamb.com/roster/agents',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': 'Chromium;v=128, Not',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
        }

        yield scrapy.Request(url=url, headers=headers, callback=self.parse_api_response)

    def parse_api_response(self, response):
        # Load the JSON response
        data = json.loads(response.text)
        
        # Extract each agent’s information from the JSON response
        for agent in data.get('rosterSearchResults', []):
            yield {
                'name': agent.get('name'),
                'job_title': agent.get('jobTitle'),
                'image_url': agent.get('imageUrl'),
                'address': agent.get('officeAddress'),
                'contact_details': {
                    'Office': agent.get('officePhone'),
                    'Cell': agent.get('cellPhone'),
                    'Fax': agent.get('faxNumber'),
                },
                'social_accounts': {
                    'facebook': agent.get('facebookUrl'),
                    'twitter': agent.get('twitterUrl'),
                    'linkedin': agent.get('linkedinUrl'),
                    'youtube': agent.get('youtubeUrl'),
                    'pinterest': agent.get('pinterestUrl'),
                    'instagram': agent.get('instagramUrl'),
                },
                'offices': agent.get('officeNames'),
                'languages': agent.get('languages'),
                'description': agent.get('agentDescription'),
            }

        # Handle pagination: check if more pages exist
        self.page_number += 1
        if self.page_number <= self.total_pages:
            # Request the next page
            next_page_url = f"{self.api_url}?layoutID=963&pageSize={self.page_size}&pageNumber={self.page_number}&sortBy=random"
            yield scrapy.Request(url=next_page_url, callback=self.parse_api_response)

    