from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    """ Посты """
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.text[:20]


class Comment(MPTTModel):
    """ Комментарии """
    text = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Родительский комментарий'
    )

    def __str__(self):
        return self.text[:20]
