from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import copy
     
from django.contrib.auth.models import User

from . import models
from . import forms


# Create your views here.

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args: Any, **kwargs: Any):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            # Cria os atributos para os forms
            self.userform = forms.UserForm(
                data=self.request.POST or None,
                usuario=self.request.user,
                instance=self.request.user,
            )
            self.perfilform = forms.PerfilForm(
                data=self.request.POST or None
            )
        else:
            self.userform = forms.UserForm(data=self.request.POST or None)
            self.perfilform = forms.PerfilForm(data=self.request.POST or None)
            
            
        self.contexto = {
        'userform': self.userform,
        'perfilform': self.perfilform,
        'senha_obrigatoria': not self.request.user.is_authenticated,
        }
        
        self.renderizar = render(self.request, self.template_name, 
                                 self.contexto)


    def get(self, *args, **kwargs):
        return self.renderizar  


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        print(self.perfil)
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username') or ''
        password = self.userform.cleaned_data.get('password') or ''
        email = self.userform.cleaned_data.get('email') or ''
        first_name = self.userform.cleaned_data.get('first_name') or ''
        last_name = self.userform.cleaned_data.get('last_name') or ''

        # Usuário Logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()
            if password:
                # Atualiza a sessão para manter o login após alterar a senha
                update_session_auth_hash(self.request, usuario)
        else:
        # Usuário não Logado
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            # Login automático após criação de conta
            user = authenticate(username=usuario.username, password=password)
            if user:
                login(self.request, user)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar


class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
