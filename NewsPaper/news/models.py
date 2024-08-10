import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User

from .resources import POST_TYPE


class Author(models.Model):
    # Cвязь «один к одному» с встроенной моделью пользователей User;
    author = models.OneToOneField(django.contrib.auth.models.User, on_delete=models.CASCADE, primary_key=True)
    # Рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    raiting = models.IntegerField(default=0)

    # Метод update_rating() модели Author, который обновляет рейтинг текущего автора (метод принимает в качестве аргумента только self).
    # Он состоит из следующего:
    # суммарный рейтинг каждой статьи автора умножается на 3;
    # суммарный рейтинг всех комментариев автора;
    # суммарный рейтинг всех комментариев к статьям автора.
    def update_raiting(self):
        # Собрать сложную схему по получению рейтинга
        final = 0
        # a_raiting
        elems = Post.objects.all().filter(author=self).values('raiting')
        # <QuerySet [{'raiting_post': -1}, {'raiting_post': 0}, {'raiting_post': 0}]>
        post_raiting = 0

        for elem in elems:
            post_raiting += elem['raiting']

        # comments_raitings Комментариев автора
        user = User.objects.all().filter(author=self).first()
        elems = Comment.objects.all().filter(user=user)

        comments_raiting = 0
        for elem in elems:
            comments_raiting += elem.raiting

        # Комментарии постов автора
        posts = Post.objects.filter(author=self)
        comments_post = 0
        for post in posts:
            comments = Comment.objects.filter(post=post)
            for comment in comments:
                comments_post += comment.raiting

        final += comments_raiting
        final += post_raiting * 3
        final += comments_post

        self.raiting = final
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    # Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    # Имеет единственное поле: название категории.
    # Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).


class Post(models.Model):
    # Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    # Каждый объект может иметь одну или несколько категорий.
    # Соответственно, модель должна включать следующие поля:
    # связь «один ко многим» с моделью Author;
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # поле с выбором — «статья» или «новость»;
    post_type = models.CharField(default="news", max_length=255)
    # автоматически добавляемая дата и время создания;
    datetime_in = models.DateTimeField(auto_now=True)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    categories = models.ManyToManyField(Category, through='PostCategory')
    # заголовок статьи/новости;
    post_name = models.CharField(max_length=255)
    # текст статьи/новости;
    post_body = models.CharField(max_length=255)
    # рейтинг статьи/новости.
    raiting = models.IntegerField(default=0)

    # Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.

    # Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр)
    # длиной 124 символа и добавляет многоточие в конце.
    def like(self):
        current_raiting = self.raiting
        self.raiting = int(current_raiting) + 1
        self.save()

    def dislike(self):
        current_raiting = self.raiting
        self.raiting = int(current_raiting) - 1
        self.save()

    def preview(self):
        data = self.post_body
        return f'{data[0:124]}...'


    def __str__(self):
        return f'{self.post_name.title()}: {self.post_body[:20]}'

class PostCategory(models.Model):
    # Промежуточная модель для связи «многие ко многим»:
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    # Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    # Модель будет иметь следующие поля:
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    # текст комментария;
    text = models.CharField(max_length=255)
    # дата и время создания комментария;
    datetime_comment_ad = models.DateTimeField(auto_now=True)
    # рейтинг комментария.
    raiting = models.IntegerField(default=0)

    # Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        current_raiting = self.raiting
        self.raiting = int(current_raiting) + 1
        self.save()

    def dislike(self):
        current_raiting = self.raiting
        self.raiting = int(current_raiting) - 1
        self.save()



# Что вы должны сделать в консоли Django?
#
# + Создать двух пользователей (с помощью метода User.objects.create_user('username')).
# + Создать два объекта модели Author, связанные с пользователями.
# + Добавить 4 категории в модель Category.
# + Добавить 2 статьи и 1 новость.
# + Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
# + Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
# + Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
#
# + Обновить рейтинги пользователей.
# + Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
# Вывести дату добавления, username автора, рейтинг
# # заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.