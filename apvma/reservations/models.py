from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from apvma.reservations.manager import ValidReservationManager


class Reservation(models.Model):
    SPOTS = (
        ('TP', 'Tapiri'),
        ('SF', 'Salão de Festas'),
        ('TA', 'Tapiri das Árvores'),
    )

    user = models.ForeignKey(User,verbose_name='apartamento', on_delete=models.CASCADE)
    date = models.DateField('data solicitada')
    spot = models.CharField('ambiente', max_length=2, choices=SPOTS)
    created_on = models.DateTimeField('data da solicitação', auto_now_add=True)
    paid = models.BooleanField('pago', default=False)
    canceled = models.BooleanField('cancelado', default=False)
    canceled_on = models.DateTimeField('cancelado em', blank=True, null=True)
    expires_on = models.DateTimeField('expira em', editable=False)

    def save(self, *args, **kwargs):
        '''Defines expires_on datetime when creating a reservation'''
        if not self.pk:
            days_valid = 1
            self.expires_on = timezone.now() + timedelta(days=days_valid)
        if self.canceled:
            self.canceled_on = timezone.now()

        return super(Reservation, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ('date',)

    def __str__(self):
        return '{} - {} - {}'.format(self.user.username, self.date, self.spot)

    def pay(self):
        """Changes the value of paid when the user pays the reservation. This will be
        set by the admin"""
        self.paid = True
        self.save()

    def cancel(self):
        """Changes the value of canceled to True when the user cancels the reservation"""
        self.canceled = True
        self.canceled_on = timezone.now()
        self.save()

    def get_color(self):
        """Defines the background color of each reservation line in the table"""
        if self.canceled or self.expired():
            return '#FF9A84' #red
        if self.paid:
            return '#9FFF99'  # green
        else:
            return 'white'

    def expired(self):
        """Returns True if reservation expires and no payment is done"""
        if self.paid:
            return False
        else:
            return self.expires_on < timezone.now()

    objects = models.Manager() # the default manager
    valid_reservations = ValidReservationManager() # valid reservation manager

    @property
    def status(self):
        """Defines the status of the reservation:
        when a reservation is created, it returns 'aguardando pagamento'
        when a reservation is canceled, it returns 'cancelada em '+ data de cancelamento'
        when a reservation is expired, it returns 'expirada por falta de pagamento'
        when a reservation is paid, it returns 'reserva confirmada'"""
        if self.canceled:
            return 'cancelada em {}'.format(self.canceled_on.date().strftime('%d/%m/%Y'))
        elif self.paid:
            return 'confirmada'
        elif self.expired():
            return 'expirada por falta de pagamento'
        else:
            return 'aguardando pagamento'


class TermsOfUse(models.Model):
    file = models.FileField(upload_to='reservations/termsofuse/',
                            validators=[FileExtensionValidator(['pdf'], 'O sistema só permite o upload de arquivos PDF.')])
    uploaded_on = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Regras de Uso de Ambiente'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """It must exist only one file of Terms of Use"""
        if TermsOfUse.objects.exists() and not self.pk:
            raise ValidationError('Só pode existir 1 arquivo de Termos de Uso de Ambiente.')
        self.uploaded_on = timezone.now()
        return super(TermsOfUse, self).save(*args, **kwargs)