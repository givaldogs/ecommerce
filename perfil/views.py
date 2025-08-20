from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import copy

from django.contrib.auth.models import User

from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args: Any, **kwargs: Any):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(usuario=self.request.user).first()

            # Trocar template se tiver perfil
            if self.perfil:
                self.template_name = 'perfil/atualizar.html'

            self.userform = forms.UserForm(
                data=self.request.POST or None,
                usuario=self.request.user,
                instance=self.request.user,
            )
            self.perfilform = forms.PerfilForm(
                data=self.request.POST or None,
                instance=self.perfil,
            )
        else:
            self.userform = forms.UserForm(data=self.request.POST or None)
            self.perfilform = forms.PerfilForm(data=self.request.POST or None)

        self.contexto = {
            'userform': self.userform,
            'perfilform': self.perfilform,
            'senha_obrigatoria': not self.request.user.is_authenticated,
        }

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = models.Perfil.objects.filter(usuario=request.user).first()
            if perfil:
                return redirect('perfil:atualizar')
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        username = self.userform.cleaned_data.get('username') or ''
        password = self.userform.cleaned_data.get('password') or ''
        email = self.userform.cleaned_data.get('email') or ''
        first_name = self.userform.cleaned_data.get('first_name') or ''
        last_name = self.userform.cleaned_data.get('last_name') or ''

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username
            if password:
                usuario.set_password(password)
                update_session_auth_hash(self.request, usuario)
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            user = authenticate(username=usuario.username, password=password)
            if user:
                login(self.request, user)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar


class Atualizar(BasePerfil):
    def setup(self, *args: Any, **kwargs: Any):
        super().setup(*args, **kwargs)
        self.template_name = 'perfil/atualizar.html'

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        usuario = self.userform.save(commit=False)
        if self.userform.cleaned_data.get('password'):
            usuario.set_password(self.userform.cleaned_data.get('password'))
            update_session_auth_hash(self.request, usuario)
        usuario.save()

        perfil = self.perfilform.save(commit=False)
        perfil.usuario = usuario
        perfil.save()

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        return self.renderizar


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
