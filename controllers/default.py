# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from datetime import date

def index():
    today = date.today()
    intai = date(today.year, today.month, 1)

    if len(request.args) > 0: an = request.args[0]
    else: an = today.year
    if len(request.args) > 1: luna = request.args[1]
    else: luna = today.month

    tcs = db(db.tip_concediu.id>0)
    angajati = db(db.angajat.activ==True).select(orderby=db.angajat.nume|db.angajat.prenume)
    for a in angajati:
        if not db.pontaj((db.pontaj.angajat==a) &
                         (db.pontaj.luna==intai)):
            db.pontaj.insert(angajat=a, luna=intai,
                             zile=[a.norma] * 31, concedii=[0]* tcs.count())
            db.commit() 

    return dict(angajati=angajati,
                an=an,
                luna=luna,
                tcs=tcs, intai=intai)

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


