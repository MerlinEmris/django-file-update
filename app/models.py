import os, logging
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from cropperjs.models import CropperImageField

from .utils import compress


logger = logging.getLogger(__name__)


class Item(models.Model):
    name = models.CharField(_("name"),
                            max_length=50)
    image = CropperImageField(_("image"),
                                upload_to='item_images',
                                dimensions=(1750,1750),
                                blank=True)
    description = models.TextField(_("description"))
    timestamp = models.DateTimeField(_("timestamp"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("item_detail", kwargs={"pk": self.pk})

@receiver(models.signals.post_delete, sender=Item)
def auto_delete_Item_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        except:
            logger.error('can not delete file on model delete')
            

@receiver(models.signals.pre_save, sender=Item)
def auto_delete_Item_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        instance.image = compress(instance.image)
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    try:
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
                instance.image = compress(instance.image)
    except:
        logger.error('can not replace file on model change')
        