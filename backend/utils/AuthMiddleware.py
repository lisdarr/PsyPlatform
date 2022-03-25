from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from database.models import Consultant, Director, Visitor


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/login/' or request.path == '/user/regist/':
            return None
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect('/login/')

        user = ''
        if Visitor.objects.filter(u_ticket=ticket).exits():
            user = Visitor.objects.get(u_ticket=ticket)
        if Consultant.objects.filter(u_ticket=ticket).exits():
            user = Consultant.objects.get(u_ticket=ticket)
        if Director.objects.filter(u_ticket=ticket).exists():
            user = Director.objects.get(u_ticket=ticket)
        if user == '':
            return HttpResponseRedirect('/login/')
