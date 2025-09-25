from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido
from utils import utils

# Create your views here.

class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar o Pedido')
   
   
class SalvarPedido(View):    
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer o Login.')
            return redirect('perfil:criar')

        # Obtém o carrinho da sessão (ou um dicionário vazio)
        carrinho = self.request.session.get('carrinho', {})

        # Se carrinho estiver vazio, redireciona com mensagem
        if not carrinho:
            messages.error(self.request, 'Carrinho está vazio')
            return redirect('produto:lista')

        # Lista dos IDs das variações presentes no carrinho (chaves são strings)
        carrinho_variacao_ids = list(carrinho.keys())

        # Busca no banco as variações correspondentes, já puxando o produto relacionado
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )
        
        # Verifica estoque e ajusta carrinho, se necessário
        for variacao in bd_variacoes:
            vid = str(variacao.id) # type: ignore[attr-defined]
                                   # chave como string para acessar 
                                   # o dicionário

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            if estoque < qtd_carrinho:
                # Ajusta quantidade e preços no carrinho
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_unitario'] = estoque * preco_unt
                carrinho[vid]['preco_unitario_promocional'] = estoque * preco_unt_promo

                # Envia mensagem de erro para o usuário
                messages.error(
                    self.request,
                    'Estoque insuficiente para alguns produtos do seu carrinho. '
                    'Reduzimos a quantidade desses produtos. Por favor, verifique '
                    'os produtos que foram alterados a quantidade.'
                )

                # Atualiza a sessão com as modificações feitas no carrinho
                self.request.session['carrinho'] = carrinho
                self.request.session.modified = True
                self.request.session.save()  # Garante salvamento imediato

                return redirect('produto:carrinho')

        # Caso tudo esteja ok, renderiza o template da página pagar
        contexto = {
            # Adicione variáveis para o template aqui, se necessário
        }

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido (
            usuario = self.request.user,
            total = valor_total_carrinho,
            qtd_total =  qtd_total_carrinho,
            status = 'C'
        )
    
        pedido.save()

        ItemPedido.objects.bulk_create(
            ItemPedido (
                pedido = pedido,
                produto = v['produto_nome'],
                produto_id =  v['produto_id'],
                variacao = v['variacao_nome'],
                variacao_id =  v['variacao_id'],
                preco =  v['preco_quantitativo'],
                preco_promocional =  v['preco_quantitativo_promocional'],
                quantidade =  v['quantidade'],
                imagem =  v['imagem'],


            ) for v in carrinho.values()
        )

        del self.request.session['carrinho']
        return redirect('pedido:lista')
        # return render(self.request, self.template_name, contexto)


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe do Pedido')
    

class Lista(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Lista de Pedido')


