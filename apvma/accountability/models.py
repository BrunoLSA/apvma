from django.core.validators import FileExtensionValidator
from django.db import models


class Accountability(models.Model):
    date = models.DateField('mês de referência')
    file = models.FileField(upload_to='accountability/',
                            validators=[FileExtensionValidator(['pdf'], 'O sistema só permite o upload de arquivos PDF.')])

    class Meta:
        verbose_name = 'prestação de conta'
        verbose_name_plural = 'prestações de contas'
        ordering = ('-date',)

    def __str__(self):
        import locale
        locale.setlocale(locale.LC_ALL, '')
        return self.date.strftime('%Y/%B')