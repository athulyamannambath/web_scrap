import scrapy


class SitespiderSpider(scrapy.Spider):
    name = "sitespider"
    allowed_domains = ["www.bhhsamb.com"]
    start_urls = ["https://www.bhhsamb.com/roster/Agents"]

   # def parse(self, response):
    

    def parse(self, response):
        # Extract all agent profile links on the page
        agent_links = response.css('a.agent-link::attr(href)').getall()
        for link in agent_links:
            # Follow each agent link
            yield response.follow(link, self.parse_agent)

        # Follow pagination to scrape all agents across all pages
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_agent(self, response):
        # Extract the required data fields
        yield {
            'name': response.css('h1.agent-name::text').get(),
            'job_title': response.css('p.agent-title::text').get(),
            'image_url': response.css('img.agent-photo::attr(src)').get(),
            'address': response.css('div.agent-address::text').get(),
            'contact_details': {
                'Office': response.xpath('//label[contains(text(),"Office")]/following-sibling::span/text()').get(),
                'Cell': response.xpath('//label[contains(text(),"Cell")]/following-sibling::span/text()').get(),
                'Fax': response.xpath('//label[contains(text(),"Fax")]/following-sibling::span/text()').get(),
            },
            'social_accounts': {
                'facebook': response.css('a.facebook::attr(href)').get(),
                'twitter': response.css('a.twitter::attr(href)').get(),
                'linkedin': response.css('a.linkedin::attr(href)').get(),
                'youtube': response.css('a.youtube::attr(href)').get(),
                'pinterest': response.css('a.pinterest::attr(href)').get(),
                'instagram': response.css('a.instagram::attr(href)').get(),
            },
            'offices': response.css('div.agent-office::text').getall(),
            'languages': response.css('div.agent-languages::text').getall(),
            'description': response.css('div.agent-description::text').get(),
        }

        

    