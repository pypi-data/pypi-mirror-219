import random

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from blog.models import Category, Blog, Tag

UserModel = get_user_model()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.lazy_attribute(
        lambda obj: '{}.{}.{}'.format(obj.first_name, obj.last_name, random.randrange(1, 1000)))
    email = factory.lazy_attribute(lambda obj: '{}@email.com'.format(obj.username))
    password = factory.PostGenerationMethodCall('set_password', 'secret')


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
