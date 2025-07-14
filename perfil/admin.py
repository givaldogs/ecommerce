from django.contrib import admin
# from . import models   # essa opcao importa toda a models.py
from .models import Perfil

# Register your models here.

#admin.site.register(models.Perfil)
from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome_completo', 'cpf_formatado', 'cep_formatado', 'cidade', 'estado')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'cpf')
    list_filter = ('estado',)

    @admin.display(description='Nome Completo')
    def nome_completo(self, obj):
        first_name = (obj.usuario.first_name or '').strip()
        last_name = (obj.usuario.last_name or '').strip()
        return f'{first_name} {last_name}'.strip() or obj.usuario.username

    @admin.display(description='CPF')
    def cpf_formatado(self, obj):
        cpf = obj.cpf
        if len(cpf) == 11 and cpf.isdigit():
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    @admin.display(description='CEP')
    def cep_formatado(self, obj):
        cep = obj.cep
        if len(cep) == 8 and cep.isdigit():
            return f'{cep[:5]}-{cep[5:]}'
        return cep
