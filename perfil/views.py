from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import copy

from django.contrib.auth.models import User

from . import models
from . import forms
# <a class="dropdown-item" href="{% url 'pedido:lista' %}">Meus pedidos</a>

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

    def renderizar_pagina(self):
        return render(self.request, self.template_name, self.contexto)
    
    def get(self, *args, **kwargs):
        return self.renderizar_pagina()


class Criar(BasePerfil):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = models.Perfil.objects.filter(usuario=request.user).first()
            if perfil:
                return redirect('perfil:atualizar')
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )
            return self.renderizar_pagina()

        username = self.userform.cleaned_data.get('username') or ''
        password = self.userform.cleaned_data.get('password') or ''
        email = self.userform.cleaned_data.get('email') or ''
        first_name = self.userform.cleaned_data.get('first_name') or ''
        last_name = self.userform.cleaned_data.get('last_name') or ''

        novo_login = False  # ✅ variável declarada aqui

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
                novo_login = True  # ✅ se login ocorrer, seta como True

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
                self.request,
                'Seu cadastro foi criado ou atualizado com sucesso'
        )

        if novo_login:
            messages.success(
                self.request,
                'Você fez login e pode concluir sua compra'
            )

        return redirect('produto:carrinho')
        return self.renderizar_pagina()


class Atualizar(BasePerfil):
    def setup(self, *args: Any, **kwargs: Any):
        super().setup(*args, **kwargs)
        self.template_name = 'perfil/atualizar.html'

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar_pagina()

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

        return self.renderizar_pagina()


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if not username or not password:
            messages.error(
            self.request,
            'Usuário ou senha invalidos'
            )
            return redirect('perfil:criar')
        
        user = authenticate(self.request,
            username=username, password=password)
        
        if not user:
            messages.error(
            self.request,
            'Usuário ou senha invalidos'
            )
            return redirect('perfil:criar')
           
        login(self.request, user)
        
        messages.success(
            self.request,
            'Você fez login no sistema e pode concluir a compra'
            )
        return redirect('produto:carrinho')


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')
