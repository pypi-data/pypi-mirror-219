# -*- coding: utf-8 -*-
import random
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


# @implementer(IExpandableElement)
# @adapter(Interface, Interface)
# class Widget(object):

#     def __init__(self, context, request):
#         self.context = context.aq_explicit
#         self.request = request

#     def __call__(self, expand=False):
#         result = {
#             'widget': {
#                 '@id': '{}/@widget'.format(
#                     self.context.absolute_url(),
#                 ),
#             },
#         }
    #     if not expand:
    #         return result

    #     # === Your custom code comes here ===

    #     # Example:
    #     try:
    #         subjects = self.context.Subject()
    #     except Exception as e:
    #         print(e)
    #         subjects = []
    #     query = {}
    #     query['portal_type'] = "All in One Accessibility"
    #     query['Subject'] = {
    #         'query': subjects,
    #         'operator': 'or',
    #     }
    #     brains = api.content.find(**query)
        # items = []
    #     for brain in brains:
    #         # obj = brain.getObject()
    #         # parent = obj.aq_inner.aq_parent
        # print(self.context.aioa_key)
        # print(self.context.portal_type)
        # items.append({
        #     'title': 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}'.format(self.context.aioa_color,self.context.aioa_key,str(random.randint(0,999999)),self.context.aioa_place)
            
        # })
        # result['widget']['items'] = items
        # return result


class WidgetGet(Service):

    def reply(self):
        print(self.context.portal_type)
        print(self.context.aioa_key)
        # value = ""
        # if self.context.aioa_key == None:
            
        value = {"url": "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}".format(self.context.aioa_color,self.context.aioa_key,str(random.randint(0,999999)),self.context.aioa_place)}
        
        
        #base_URL = str(value)
        # value = '{"url":"https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode=420083&token=DRUPAL6CQ9-00H7-QXQS-30ZN-KA45-KTNL&t=0.5294880354467668&position=bottom_right"}'
        
        # value = '{"test":"demo"}'

        return value
