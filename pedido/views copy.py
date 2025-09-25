from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao

# Create your views here.

class Pagar(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer o Login.'
            )
            return redirect('perfil:criar')

        carrinho = self.request.session.get('carrinho', {})

        if not carrinho:
            messages.error(
                self.request,
                'Carrinho está vazio'
            )
            return redirect('produto:lista')

        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in = carrinho_variacao_ids)
        )
        
        for variacao in bd_variacoes:
            vid = str(variacao.id)  # type: ignore[attr-defined]

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque =''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_unitario'] = estoque * preco_unt
                carrinho[vid]['preco_unitario_promocional'] = estoque * \
                preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho' \
                    'Reduzimos a quantidade desses produtos. Por favor, verifique ' \
                    'os produtos que foram alterados a quantidade'
            
                if error_msg_estoque:
                    messages.error(
                        self.request,
                        error_msg_estoque
                    )
                
                self.request.session['carrinho'] = carrinho
                self.request.session.modified = True
                self.request.session.save() # por seguranca, porque o comando 
                                            # self.request.session.modified = True
                                            # Informar o Django que a sessão 
                                            # foi modificada (modified = True)

                return redirect('produto:carrinho')

        contexto = {
            # Você pode adicionar dados para o template aqui depois
        }

        return render(
            self.request,
            self.template_name,
            contexto
        )



class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Salvar o Pedido')


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe do Pedido')

