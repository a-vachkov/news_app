from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_ratings(self):
        rate_post_author = self.post_set.all().aggregate(sum_rating=Sum('rate') * 3)['sum_rating']
        rate_comment = self.user.comment_set.all().aggregate(sum_rating=Sum('rate'))['sum_rating']
        rate_comment_post = self.user.post_set.сomment_set.all().aggregate(sum_rating=Sum('rate'))['sum_rating']
        self.rate = rate_post_author + rate_comment + rate_comment_post
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    news = 'NE'
    artikle = 'AR'

    TYPE = [
        (news, 'Новость'),
        (artikle, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE, default=artikle)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length=124):
        return f"{self.text[:length]}..." if len(str(self.text)) > length else self.text


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = + 1
        self.save()

    def dislike(self):
        self.rating = - 1
        self.save()
