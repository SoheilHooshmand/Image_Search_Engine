from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image
from . import clip
from . import milvus

@receiver(post_save, sender=Image)
def embedding_images(sender, instance, created, **kwargs):
    if created:
        image = instance
        cl = clip.Clip()
        embedding = cl.image_embeding(image.url)
        mil = milvus.Milvus()
        collection_name = mil.create_or_get_name_of_collection()
        mil.insert(collection_name, [[image.id], [embedding]])



