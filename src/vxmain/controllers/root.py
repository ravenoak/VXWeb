# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from vxmain import model
from vxmain.lib.base import BaseController
from vxmain.controllers.error import ErrorController
from vxmain.controllers.image import ImageController
from vxmain.controllers.page import PageController
from vxmain.controllers.project import ProjectController
from vxmain.controllers.secure import SecureController
from vxmain.controllers.admin import VXAdminController, VXAdminConfig
from vxmain.model import DBSession, metadata
#from tgext.admin.tgadminconfig import TGAdminConfig
#from tgext.admin.controller import AdminController


__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the vxmain application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    
    #admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    admin = VXAdminController(model, DBSession, config_type = VXAdminConfig)
    error = ErrorController()
    image = ImageController()
    images = image
    page = PageController()
    pages = page
    project = ProjectController()
    projects = project
    secc = SecureController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "vxmain"

    @expose()
    def index(self):
        """Handle the front-page."""
        redirect(url('/page/Welcome'))

    @expose()
    def about(self):
        """Handle the 'about' page."""
        redirect(url('/page/About'))

    @expose()
    def contact(self):
        """Handle the 'contact' page."""
        redirect(url('/page/Contact'))


#    @expose('vxmain.templates.index')
#    def index(self):
#        """Handle the front-page."""
#        return dict(page='index')
#
#    @expose('vxmain.templates.about')
#    def about(self):
#        """Handle the 'about' page."""
#        return dict(page='about')

    @expose('vxmain.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('vxmain.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)
    @expose('vxmain.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('vxmain.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('vxmain.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
