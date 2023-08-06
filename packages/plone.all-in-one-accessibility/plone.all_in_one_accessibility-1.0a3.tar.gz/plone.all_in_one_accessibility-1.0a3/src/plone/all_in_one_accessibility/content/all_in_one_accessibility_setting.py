# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone import api
from plone.all_in_one_accessibility import _
from plone.dexterity.content import Item

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.i18n import translate



aioa_NOTE = "<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span><script>if(document.querySelector('#form-widgets-aioa_key').value != ''){document.querySelector('.validate_pro').style.display='none';} else {document.querySelector('.validate_pro').style.display='block';}</script>"

# @provider(IContextAwareDefaultFactory)
# def translate_header(context):
#     # use zope.i18n translate and pass in the request as the translation context
#     return translate(_(u"Recently Updated Indicators"), context=context.REQUEST) 
class IAllInOneAccessibilitySetting(model.Schema):
    aioa_key = schema.TextLine(
        title='License Key',
        required=False,
        readonly=False,
        description = aioa_NOTE,
        default = u""
    )
    
    aioa_color = schema.TextLine(
        title='Hex color code',
        description='You can cutomize the ADA Widget color. For example: #FF5733',
        
       
        required=False,
        readonly=False,
    )
    
    aioa_place = schema.Choice(
        title='Where would you like to place the accessibility icon on your site',
        values=['top_left',
      'top_center',
      'top_right',
      'middel_left',
      'middel_right',
      'bottom_left',
      'bottom_center',
      'bottom_right']
    )


@implementer(IAllInOneAccessibilitySetting)
class AllInOneAccessibilitySetting(Item):
    def __init__(self, id=None, **kwargs):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='All in One Accessibility Setting')
        if brains:
            raise Exception('Only one "All in One Accessibility setting" object is allowed per Plone instance')

        super(AllInOneAccessibilitySetting, self).__init__(id, **kwargs)
        
from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(IAllInOneAccessibilitySetting, AllInOneAccessibilitySetting)
