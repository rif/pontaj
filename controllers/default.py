# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from datetime import date, timedelta
import calendar

def _prev_month(intai):
    pe = intai - timedelta(days=1)
    return date(pe.year, pe.month, 1)

def _next_month(intai):
    ultima = calendar.monthrange(intai.year, intai.month)[1]
    u = date(intai.year, intai.month, ultima)
    return u + timedelta(days=1)

def index():
    today = date.today()
    if len(request.args) > 0: an = int(request.args[0])
    else: an = today.year
    if len(request.args) > 1: luna = int(request.args[1])
    else: luna = today.month
    intai = date(an, luna, 1)

    tcs = db(db.tip_concediu.id>0)
    angajati = db((db.angajat.activ==True)&(db.angajat.firma==session.firma_id)).select(orderby=db.angajat.nume|db.angajat.prenume)
    session.firma_id = (session.firma_id or 1)
    firma = db.firma(session.firma_id)
    c = calendar.Calendar()
    for a in angajati:
        if not db.pontaj((db.pontaj.angajat==a) &
                         (db.pontaj.luna==intai)):
            pontaje = []
            for zi in c.itermonthdays2(an, luna):
                if zi[0] == 0: continue # skip start and end 0s
                if zi[1] in (5,6): # if weekend
                    pontaje.append(0)
                else:
                    pontaje.append(a.norma)
            db.pontaj.insert(angajat=a, luna=intai,
                             zile=pontaje, concedii=[0]* tcs.count())
            db.commit() 

    return dict(angajati=angajati,
                an=an,
                luna=luna,
                tcs=tcs,
                intai=intai,
                firma=firma,
                inapoi=_prev_month(intai),
                inainte=_next_month(intai))

def angajati():
    angajati = db().select(db.angajat.ALL,
                           orderby=db.angajat.nume|db.angajat.prenume)
    if len(request.args) == 0:
        form = crud.create(db.angajat,
                           next=URL(), message="Angajat introdus")
    else:
        form = crud.update(db.angajat, request.args[0], deletable=False, 
                           next=URL(), message="Angajat actualizat")
    return dict(angajati=angajati, form=form)

def firme():
    firme = db().select(db.firma.ALL, orderby=db.firma.nume)
    if len(request.args) == 0:
        form = crud.create(db.firma,
                           next=URL(), message="Firma introdusa")
    else:
        form = crud.update(db.firma, request.args[0], deletable=False, 
                           next=URL(), message="Firma actualizata")
    return dict(firme=firme, form=form)


def urmatoarea_firma():
    session.firma_id = (session.firma_id or 0) + 1
    if session.firma_id > db(db.firma.id>0).count():
        session.firma_id = 1
    return redirect(URL('index'))
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


