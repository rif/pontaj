# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Pontajul angazatilor')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Fericean'
response.meta.description = 'Aplicatie pentru pontarea angazilor intr-o firma din Romania'
response.meta.keywords = 'pontaj, pontare, ore, timp, lucru, firma'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2011'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Pontaj'), False, URL(request.application,'default','index'), []),
    (T('Angajati'), False, URL('angajati'), []),
    (T('Firme'), False, URL('firme'), [])
    ]
