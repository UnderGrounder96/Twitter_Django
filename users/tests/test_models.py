from PIL import Image
from io import BytesIO
from pathlib import Path
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from users.models import Profile

class TestModels(TestCase):
  def setUp(self):
    self.user = User.objects.create(
      username='myusername',
      email='my@email.com',
      password='dummypass1234'
    )
    self.profile = Profile.objects.get(
      user=self.user
    )

  def test_profile_is_assigned(self):
    self.assertEqual(str(self.profile.image), 'default.jpg')
    self.assertEqual(str(self.user.profile.image), 'default.jpg')

  def image_path(self, img):
    return 'profile_pics/'+img

  def create_image(self):
    im_io = BytesIO()
    im = Image.new(mode='RGB', size=(300,300)).save(im_io, 'JPEG')
    return InMemoryUploadedFile(im_io, None, 'test_viewx.jpg',
      'image/jpeg', len(im_io.getvalue()), None).open()

  def test_profile_alter(self):
    image = self.create_image()
    self.user.profile.image = self.profile.image = image
    self.user.profile.save(); self.profile.save()
    self.assertEqual(str(self.profile.image), self.image_path(image.name))
    self.assertEqual(str(self.user.profile.image), self.image_path(image.name))
    if Path('./media/'+self.image_path(image.name)).exists():
      Path('./media/'+self.image_path(image.name)).unlink()