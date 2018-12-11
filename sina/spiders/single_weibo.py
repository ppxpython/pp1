
import re
from lxml import etree
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from sina.spiders.utils import time_fix
import time
from sina.items import TweetsItem, CommentItem


class SingleWeibo(Spider):
    name='single'
    base_url = 'https//weibo.cn'


    def start_requests(self):
        start_urls = [
            # 'https://weibo.cn/5063744248/Ezb63iprj',
            # 'https://weibo.cn/5063744248/H6rI0wVZf'
            # 'https://weibo.cn/5063744248/H6D4hpULk'  # 人民日报某积极微博
            'https://weibo.cn/5063744248/H6yI2cMyN'  # 消极微博
        ]

        for url in start_urls:
            yield Request(url=url, callback=self.parse_tweet)

    def parse_tweet(self, response):
        page_url = response.url
        tweet_item = TweetsItem()
        tree_node = etree.HTML(response.body)
        tweet_content_node = tree_node.xpath('.//span[@class="ctt"]')[0]
        all_content = tweet_content_node.xpath('string(.)').strip('\u200b')
        tweet_item['content'] = all_content
        tweet_item['crawl_time'] = int(time.time())

        user_tweet_id = re.search(r'https://weibo.cn/(\d+)/(.*)', page_url)
        tweet_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(1),
                                                                   user_tweet_id.group(2))
        tweet_item['user_id'] = user_tweet_id.group(1)
        tweet_item['_id'] = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
        create_time_info = tree_node.xpath('.//span[@class="ct" and contains(text(),"来自")]/text()')[0]
        tweet_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
        like_num = tree_node.xpath('.//a[contains(text(),"赞[")]/text()')[0]
        tweet_item['like_num'] = int(re.search('\d+', like_num).group())
        repost_num = tree_node.xpath('.//a[contains(text(),"转发[")]/text()')[0]
        tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())
        comment_num = tree_node.xpath('.//span[@class="pms" and contains(text(),"评论[")]/text()')[0]
        tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())
        yield tweet_item
        comment_url = page_url + '?page=1'
        yield Request(url=comment_url, callback=self.parse_comment, meta={'weibo_url': page_url})

    def parse_comment(self, response):
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_comment, dont_filter=True, meta=response.meta)

        selector = Selector(response)
        comment_nodes = selector.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href').extract_first()
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = int(time.time())
            comment_item['weibo_url'] = response.meta['weibo_url']
            comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url).group(1)
            comment_item['content'] = comment_node.xpath('.//span[@class="ctt"]').xpath('string(.)').extract_first()
            comment_item['_id'] = comment_node.xpath('./@id').extract_first()
            created_at = comment_node.xpath('.//span[@class="ct"]/text()').extract_first()
            comment_item['created_at'] = time_fix(created_at.split('\xa0')[0])
            comment_like = comment_node.xpath('.//span[@class="cc"]/a[contains(text(),"赞[")]/text()').extract_first()
            comment_item['like'] = int(re.search('\d+', comment_like).group())
            yield comment_item

    if __name__ == "__main__":
        process = CrawlerProcess(get_project_settings())
        process.crawl('single_weibo')
        process.start()

