import aiohttp
import requests

class Article:
    def __init__(self, articleName, floorInfo, dealOrWarrantPrc, areaName, direction, articleConfirmYmd,
                 articleFeatureDesc, tagList, buildingName, cpName, cpPcArticleUrl):
        self.articleName = articleName
        self.floorInfo = floorInfo
        self.dealOrWarrantPrc = dealOrWarrantPrc
        self.areaName = areaName
        self.direction = direction
        self.articleConfirmYmd = articleConfirmYmd
        self.articleFeatureDesc = articleFeatureDesc
        self.tagList = tagList
        self.buildingName = buildingName
        self.cpName = cpName
        self.cpPcArticleUrl = cpPcArticleUrl

    def __str__(self):
        return (f'Article Name: {self.articleName}, Floor Info: {self.floorInfo}, Price: {self.dealOrWarrantPrc}, '
                f'Area: {self.areaName}, Direction: {self.direction}, Confirm Date: {self.articleConfirmYmd}, '
                f'Features: {self.articleFeatureDesc}, Tags: {self.tagList}, Building: {self.buildingName}, '
                f'CP Name: {self.cpName}, URL: {self.cpPcArticleUrl}')

class NaverLandApi:
    def __init__(self, apt_id, area, trade_type):
        self.apt_name = None
        self.apt_id = apt_id
        self.area = area
        self.trade_type = trade_type
        self.cookies = {
            'NNB': 'P5NZPDJIFBBWM',
            'ASID': '7db0cd8a0000018fbdd04b850000005d',
            'ba.uuid': '3f412a06-c9cc-4cba-9acf-509ceb91756e',
            '_fbp': 'fb.1.1724024692515.337641061116852553',
            'naverfinancial_CID': '7e1d8c56cc184b5481090593f6d65338',
            '_tt_enable_cookie': '1',
            '_ttp': 'KJFqmJZx-MdLHmAmw4y2Ez7QJ-Y',
            '_ga_Q7G1QTKPGB': 'GS1.1.1727686246.2.1.1727686304.0.0.0',
            'NV_WETR_LAST_ACCESS_RGN_M': '"V0RKUE4wMDI4NQ=="',
            'NV_WETR_LOCATION_RGN_M': '"V0RKUE4wMDI4NQ=="',
            'NFS': '2',
            '_ga': 'GA1.2.885400896.1724024692',
            '_ga_EFBDNNF91G': 'GS1.1.1732664627.1.0.1732664629.0.0.0',
            '_gcl_au': '1.1.993435243.1732698094',
            'V2.RECENT_KEYWORD.LIST': '%5B%7B%22keyword%22%3A%22%ED%8B%B0%EC%96%B4%22%7D%2C%7B%22keyword%22%3A%22%EA%B3%BC%EA%B8%88%22%7D%2C%7B%22keyword%22%3A%22%EB%85%B8%EA%B0%80%EB%8B%A4%22%7D%2C%7B%22keyword%22%3A%22%EC%9E%A5%EB%B9%84%20%ED%92%88%EC%A7%88%22%7D%2C%7B%22keyword%22%3A%22%EB%AC%B4%EA%B3%BC%EA%B8%88%22%7D%2C%7B%22keyword%22%3A%22%EC%B4%88%EB%B3%B4%22%7D%5D',
            'BNB_FINANCE_HOME_TOOLTIP_STOCK': 'true',
            'BNB_FINANCE_HOME_TOOLTIP_ESTATE': 'true',
            '_fwb': '196EB6x3XKXtDAqLRuBOlAG.1736931281302',
            'NAC': 'SHOnBQQfBk4XB',
            'NACT': '1',
            'nid_inf': '17475917',
            'NID_AUT': '7e+SIzejCfXBcRtP6GgUInARu5MKW2j1m6Kw7MONQFejEHY09UGEzXVh0wBWxeo4',
            'NID_JKL': '30jA6TwQRlcWn22rrTizm9nHwX+sz/8JBmj2Ee6JKn0=',
            'page_uid': 'iG2x0sqVN8ossPTEJl4ssssstKR-422059',
            'NID_SES': 'AAABx+4Sx9KDqmu0lzwoUnyO+kegqDnwLTEsETewMt8AX3Izt9WFXwIAeoun8BEVJFgCAWSpcXNYcCqsEx8q1ZS7eYicywAfYQ+1or2gbKnb1TA07yd6EzyGrMLSustwqp9AZpJJ+WCQDsOxcn9MdBtEBuVxrUh0NW2/cjrDvNqcOpRqcu6Wp0WkGKXOZ8p5FQqvG3bTIIZvyLY8OYp5YM5BfNhyrvW7ATY6OiyF8/CpCohYYvyOneukGHnb+pAtGSSohiXmR6/kig+XhSFy/V/Ro5FBIP6wAGtCthnJe+Z8uNiDK2zT8zSh27L9GPO0UGJBrBqw84xUEU147N25j90st02S50ASqq3/yrKAZVLC5TCbdj2M3gKc6MZqpZ5+DBiaV1zmU5egXL+f3xP51qICnN4zbuidKKOMi1lpIX+EJS2KLsLlUVqsuav11Iivlhx5iw7/jH2Px5AkdM4aVkRWRKPiLy7/EIxdvczbpsPe3CHzEZQSSLcYgYDJeEjhmtMraS3kIyKhyHo8t//JEjlO/UF4oH4XFbfAN1YgN0YxZ482blrBMHxDZrYKJyyN0vm9MNZZ4la8922I7soHMknxX1+Xnr3QipE1ff5KOMhY8YhR',
            'REALESTATE': 'Mon%20Jan%2020%202025%2012%3A29%3A37%20GMT%2B0900%20(Korean%20Standard%20Time)',
            'BUC': '6hQbULln81LhQUwWXmWx8iScgMDODD1NIVHoC7hfQnw=',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MzczNDM3NzcsImV4cCI6MTczNzM1NDU3N30.A2hAfoO6NEsQcI-uqUO8ysceDxoFhD-dGZ5SjVvkNag',
            'priority': 'u=1, i',
            'referer': 'https://new.land.naver.com/complexes/117329?ms=37.5140382,126.8572939,16&a=APT:ABYG:JGC:PRE&e=RETAIL',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers=self.headers,
            cookies=self.cookies
        )

    async def get_apt_name(self):
        try:
            url = f'https://new.land.naver.com/api/articles/complex/{self.apt_id}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType={self.trade_type}&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&complexNo={self.apt_id}&buildingNos=&areaNos={self.area}&type=list&order=rank'
            resp = await self.session.get(
                url=url
            )
            resp.raise_for_status()
            result = await resp.json()
            self.apt_name = result['articleList'][0]
            return self.apt_name
        except Exception as ex:
            raise ex

    async def fetch_articles(self, page):
        try:
            url = f'https://new.land.naver.com/api/articles/complex/{self.apt_id}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType={self.trade_type}&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo={self.apt_id}&buildingNos=&areaNos={self.area}&type=list&order=rank'
            resp = await self.session.get(
                url=url
            )
            resp.raise_for_status()
            result = await resp.json()
            return result['articleList']
        except Exception as ex:
            raise ex

    async def get_all_articles(self):
        all_articles = []
        page = 1
        while True:
            articles = await self.fetch_articles(page)
            if len(articles) == 0:
                break
            for article in articles:
                try:
                    all_articles.append(Article(
                        articleName=article['articleName'],
                        floorInfo=article['floorInfo'],
                        dealOrWarrantPrc=article['dealOrWarrantPrc'],
                        areaName=article['areaName'],
                        direction=article['direction'],
                        articleConfirmYmd=article['articleConfirmYmd'],
                        articleFeatureDesc=article.get('articleFeatureDesc', ''),
                        tagList=article['tagList'],
                        buildingName=article['buildingName'],
                        cpName=article['cpName'],
                        cpPcArticleUrl=article['cpPcArticleUrl']
                    ))
                except KeyError as e:
                    print(f"Missing key {e} in article: {article}")
                    continue
            page += 1
        return all_articles
