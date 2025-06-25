from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/',
        blank=True, null=True
    )
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    @staticmethod
    def resize_image(img, new_width=800):
        """Redimensiona imagem para no máximo `new_width` px de largura, 
           mantendo proporção."""
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        try:
            with Image.open(img_full_path) as img_pillow:
                original_width, original_height = img_pillow.size

                if original_width <= new_width:
                    #print('retornando imagem original menor que a nova largura')
                    return  # Não precisa redimensionar

                new_height = round((new_width * original_height) / original_width)
                new_image = img_pillow.resize(
                    (new_width, new_height),
                    Image.Resampling.LANCZOS
                )
                new_image.save(img_full_path, optimize=True, quality=50)
                #print('imagem foi redimensionada')

        except Exception as e:
            print(f"Erro ao abrir imagem {img_full_path}: {e}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem:
            self.resize_image(self.imagem, new_width=800)

    def __str__(self):
        return self.nome

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promociona = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.nome or self.produto.nome
    

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

