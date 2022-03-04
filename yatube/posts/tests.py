from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Group, User


class TestPost(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Pavel",
            password="12345"
        )
        self.post = Post.objects.create(text='Test tex', author=self.user)

    def test_login_progile(self):
        """После регистрации пользователя создается его персональная страница (profile)"""
        response = self.client.get(reverse('profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_authorization_user_create_post(self):
        """Авторизованный пользователь может опубликовать пост (new)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('post_edit', kwargs=dict(username=self.user.username,
                                                                    post_id=self.post.id)))
        self.assertEqual(response.status_code, 200)

    def test_logout_post(self):
        """Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)"""
        response = self.client.get(reverse('new_post'), follow=True)
        self.assertEqual(('/auth/login/?next=/new/', 302), response.redirect_chain[0])

    def test_post_on_index(self):
        """После публикации поста новая запись появляется на главной странице сайта (index)"""
        # self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.post.text)

    def test_post_on_profile(self):
        """После публикации поста новая запись появляется на главной странице сайта (profile)"""
        response = self.client.get(reverse('profile', kwargs=dict(username=self.user.username)))
        self.assertContains(response, self.post.text)

    def test_post_on_post(self):
        """После публикации поста новая запись появляется на главной странице сайта (post)"""
        response = self.client.get(reverse('post', kwargs=dict(username=self.user.username,
                                                               post_id=self.post.id)))
        self.assertContains(response, self.post.text)


class TestPostEdit(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Pavel",
            password="12345"
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(text='Test tex', author=self.user)
        self.new_text = 'Change test text'
        self.client.post(f"/{self.user.username}/{self.post.pk}/edit/", {"text": self.new_text})

    def test_postedit_index(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на главной странице сайта (index)"""
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.new_text)

    def test_postedit_profile(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на персональной странице пользователя (profile)"""
        response = self.client.get(reverse('profile', kwargs=dict(username=self.user.username)))
        self.assertContains(response, self.new_text)

    def test_postedit_view(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на отдельной странице поста (post)"""
        response = self.client.get(reverse('post', kwargs=dict(username=self.user.username,
                                                               post_id=self.post.id)))
        self.assertContains(response, self.new_text)

    def test_page_not_found(self):
        """Возвращает ли сервер код 404, если страница не найдена."""
        import uuid
        test_uuid = uuid.uuid4()
        response = self.client.get(f'/{test_uuid}/')
        self.assertEqual(response.status_code, 404)


class TestPageImg(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Pavel",
            password="12345"
        )
