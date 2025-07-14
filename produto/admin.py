from django.contrib import admin
from . import models

class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    @admin.display(description='Preço')
    def get_preco_formatado(self, obj):
        return obj.get_preco_formatado()
    

    @admin.display(description='Preço Promo.')
    def get_preco_promocional_formatado(self, obj):
        return obj.get_preco_promocional_formatado()
    
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado',
                    'get_preco_promocional_formatado'
                    ]
    inlines = [
        VariacaoInline
    ]


# Register your models here.

admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
 