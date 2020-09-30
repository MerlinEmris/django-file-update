# Django image managed

This is django project with image managment. It's change image file and remove image when model object is removed. And cropper js added to it as extra tool with image compression to JPEG format.


## Installation
### Requirments
- python 3.5 +
- pip 
- Django 2.2 +
- django-cropperjs 0.0.5
- pillow 7 +

### Clone
- Clone this repo to your local machine using `https://github.com/MerlinEmris/project.git`

### Setup
> install python and pip first

```shell
$ apt get install python3
$ apt get install python3-pip
```

- Then go to project dir and install requirments

```shell
$ pip3 install -r requirments.txt
```

## Structure
```python

class Item(models.Model):
    name = models.CharField(_("name"),
                            max_length=50)
    image = CropperImageField(_("image"),
                                upload_to="item_images",
                                dimensions=(1750,1750),
                                blank=True)
    description = models.TextField(_("description"))
    timestamp = models.DateTimeField(_("timestamp"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name
        
```
-To manage file removing when item image was changed or deleted we need to add to methods there.

```python
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

```
-First method deletes image file when item obj was deleted
-Second one to remove image when item image is changed

If you are using vscode ide than you can user this snippet.
```json
{

    "delete model file on change": {
        "prefix": ["modfile", "model-file-change-delete"],
        "body": [
            "@receiver(models.signals.post_delete, sender=${1:model})",
            "def auto_delete_${1:model}_${2:field}_on_delete(sender, instance, **kwargs):",
            "    if instance.${2:field}:",
            "        try:",
            "            if os.path.isfile(instance.${2:field}.path):",
            "                os.remove(instance.${2:field}.path)",
            "        except:",
            "            ${0:pass}",
            "",
            "@receiver(models.signals.post_delete, sender=${1:model})",
            "def auto_delete_${1:model}_${2:field}_on_change(sender, instance, **kwargs):",
            "    if not instance.pk:",
            "        instance.${2:field} = compress(instance.${2:field})",
            "        return False",
            "    try:",
            "        old_file = sender.objects.get(pk=instance.pk).${2:field}",
            "    except sender.DoesNotExist:",
            "        return False",
            "    try:",
            "        new_file = instance.${2:field}",
            "        if not old_file == new_file:",
            "            if os.path.isfile(old_file.path):",
            "                os.remove(old_file.path)",
            "                instance.${2:field} = compress(instance.${2:field})",
            "    except:",
            "        ${0:pass}"
        ],
        "description": "delete models file when model file changed!"
    }

}
```

As you can see we have compress method there. This method converts image to JPEG formant and reduce quality.

```python
from PIL import Image
from io import BytesIO

from django.core.files import File


def compress(image):
    """
        Takes image and converts it to JPEG format with compession
    """
    print('image compress -> ', image.path)
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=85) 
    new_image = File(im_io, name=image.name)
    return new_image
```
