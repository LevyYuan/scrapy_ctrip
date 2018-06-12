# -*- coding: utf-8 -*-
# post请求 爬取携程所有特卖汇

from scrapy import FormRequest, Spider
import json
from scrapy_07_爬携程.items import GroupItem, FreeItem, TicketItem, OnedayItem, CruiseItem
from copy import deepcopy


class CtripSpider(Spider):
    name = 'ctrip'
    allowed_domains = ['vacations.ctrip.com']

    post_url = 'http://vacations.ctrip.com/Package-Booking-Promotion/jsondataprovider/Query'

    group_data = '{"GroupId":"1","ChannelId":"1","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"1","PageIndex":%d,"SaleCity":0}'
    free_data = '{"GroupId":"2","ChannelId":"2","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"2","PageIndex":%d,"SaleCity":0}'
    ticket_data = '{"GroupId":"9","ChannelId":"5","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"5","PageIndex":%d,"SaleCity":0}'
    oneday_data = '{"GroupId":"5","ChannelId":"4","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"4","PageIndex":%d,"SaleCity":0}'
    cruise_data = '{"GroupId":"4","ChannelId":"3","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"3","PageIndex":%d,"SaleCity":0}'

    # 重写start_request
    def start_requests(self):
        page = 0
        post_group_data = dict(QType='queryv3', Data=self.group_data % page)
        post_free_data = dict(QType='queryv3', Data=self.free_data % page)
        post_ticket_data = dict(QType='queryv3', Data=self.ticket_data % page)
        post_oneday_data = dict(QType='queryv3', Data=self.oneday_data % page)
        post_cruise_data = dict(QType='queryv3', Data=self.cruise_data % page)

        # 请求跟团游
        yield FormRequest(self.post_url, formdata=post_group_data, callback=self.parse_group, meta={'page': page})

        # 请求自由行
        yield FormRequest(self.post_url, formdata=post_free_data, callback=self.parse_free, meta={'page': page})

        # 请求门票
        yield FormRequest(self.post_url, formdata=post_ticket_data, callback=self.parse_ticket, meta={'page': page})

        # 请求一日游
        yield FormRequest(self.post_url, formdata=post_oneday_data, callback=self.parse_oneday, meta={'page': page})

        # 请求邮轮游
        yield FormRequest(self.post_url, formdata=post_cruise_data, callback=self.parse_cruise, meta={'page': page})

    # 解析跟团游
    def parse_group(self, response):
        res = json.loads(response.text)
        # 获取特卖会信息
        wraps = res['Pkgs']

        if wraps:
            # 事例化item对象
            groupitem = GroupItem()
            for wrap in wraps:
                groupitem['type'] = wrap['ProductTypeName']
                groupitem['title'] = wrap['ProductFromDepartCity']
                groupitem['trans'] = wrap['Highlight1']
                groupitem['hotel'] = wrap['Highlight2']
                groupitem['date'] = wrap['Highlight3']
                groupitem['img'] = wrap['CoverImageUrl']
                groupitem['seat'] = wrap['Seat']
                groupitem['discount'] = wrap['Discount']
                groupitem['price'] = wrap['SalesPrice']
                # print(groupitem)
                yield groupitem

            page = response.meta.get('page') + 1
            post_group_data = dict(QType='queryv3', Data=self.group_data % page)

            # 请求下一页
            yield FormRequest(
                self.post_url,
                formdata=post_group_data,
                callback=self.parse_group,
                meta={'page': page}
            )

    # 解析自由行
    def parse_free(self, response):
        res = json.loads(response.text)
        # print(res)
        wraps = res['Pkgs']
        if wraps:
            freeitem = FreeItem()
            for wrap in wraps:
                freeitem['type'] = wrap['ProductTypeName']
                freeitem['title'] = wrap['ProductFromDepartCity']
                freeitem['trans'] = wrap['Highlight1']
                freeitem['hotel'] = wrap['Highlight2']
                freeitem['date'] = wrap['Highlight3']
                freeitem['img'] = wrap['CoverImageUrl']
                freeitem['seat'] = wrap['Seat']
                freeitem['discount'] = wrap['Discount']
                freeitem['price'] = wrap['SalesPrice']

                # print(freeitem)
                yield freeitem

            page = response.meta.get('page') + 1
            # print(page)

            post_free_data = dict(QType='queryv3', Data=self.free_data % page)

            # 请求下一页
            yield FormRequest(
                self.post_url,
                formdata=post_free_data,
                callback=self.parse_free,
                meta={'page': page})

    # 解析门票
    def parse_ticket(self, response):
        res = json.loads(response.text)
        wraps = res['Pkgs']

        if wraps:
            ticketitem = TicketItem()
            for wrap in wraps:
                ticketitem['type'] = wrap['ProductTypeName']
                ticketitem['title'] = wrap['ProductFromDepartCity']
                ticketitem['trans'] = wrap['Highlight1']
                ticketitem['date'] = wrap['Highlight3']
                ticketitem['img'] = wrap['CoverImageUrl']
                ticketitem['seat'] = wrap['Seat']
                ticketitem['discount'] = wrap['Discount']
                ticketitem['price'] = wrap['SalesPrice']

                # print(ticketitem)
                yield ticketitem

            page = response.meta.get('page') + 1
            # print(page)

            post_ticket_data = dict(QType='queryv3', Data=self.ticket_data % page)

            # 请求下一页
            yield FormRequest(
                self.post_url,
                formdata=post_ticket_data,
                callback=self.parse_ticket,
                meta={'page': page})

    # 解析一日游
    def parse_oneday(self, response):
        res = json.loads(response.text)
        # print(res)
        wraps = res['Pkgs']
        # print(wraps)

        if wraps:
            onedayitem = OnedayItem()
            for wrap in wraps:
                onedayitem['type'] = wrap['ProductTypeName']
                onedayitem['title'] = wrap['ProductFromDepartCity']
                onedayitem['trans'] = wrap['Highlight1']
                onedayitem['date'] = wrap['Highlight3']
                onedayitem['img'] = wrap['CoverImageUrl']
                onedayitem['seat'] = wrap['Seat']
                onedayitem['discount'] = wrap['Discount']
                onedayitem['price'] = wrap['SalesPrice']

                # print(onedayitem)
                yield onedayitem

            page = response.meta.get('page') + 1
            # print(page)

            post_oneday_data = dict(QType='queryv3', Data=self.oneday_data % page)

            # 请求下一页
            yield FormRequest(
                self.post_url,
                formdata=post_oneday_data,
                callback=self.parse_oneday,
                meta={'page': page})

    # 解析邮轮游
    def parse_cruise(self, response):
        pass
        res = json.loads(response.text)
        wraps = res['Pkgs']

        if wraps:
            cruiseitem = CruiseItem()
            for wrap in wraps:
                cruiseitem['type'] = wrap['ProductTypeName']
                cruiseitem['title'] = wrap['ProductFromDepartCity']
                cruiseitem['trans'] = wrap['Highlight1']
                cruiseitem['date'] = wrap['Highlight3']
                cruiseitem['img'] = wrap['CoverImageUrl']
                cruiseitem['seat'] = wrap['Seat']
                cruiseitem['discount'] = wrap['Discount']
                cruiseitem['price'] = wrap['SalesPrice']

                print(cruiseitem)
                yield cruiseitem

            page = response.meta.get('page') + 1
            # print(page)

            post_cruise_data = dict(QType='queryv3', Data=self.cruise_data % page)

            # 请求下一页
            yield FormRequest(
                self.post_url,
                formdata=post_cruise_data,
                callback=self.parse_cruise,
                meta={'page': page})
