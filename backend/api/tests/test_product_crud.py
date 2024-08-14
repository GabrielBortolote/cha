from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Product
from base.serializers import ProductSerializer

class TestProductCRUD(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.p1 = Product.objects.create(name='Product 1', value=1.0, description='description 1')
    self.p2 = Product.objects.create(name='Product 2', value=2.0, description='description 2')
    self.p3 = Product.objects.create(name='Product 3', value=3.0, description='description 3')

  def test_product_list(self):
    response = self.client.get(reverse('product-list'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # assert count
    products = Product.objects.all()
    self.assertEqual(products.count(), 3)
    self.assertEqual(len(response.data), 3)

    # assert last product data
    product_1_data = ProductSerializer(self.p3)
    self.assertEqual(product_1_data.data, response.data[0])

  def test_product_retrieve(self):
    response = self.client.get(
      reverse('product-detail', kwargs={'pk': self.p1.id}),
    )
    serializer = ProductSerializer(self.p1)
    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_product_delete(self):
    response = self.client.delete(
      reverse('product-detail', kwargs={'pk': self.p2.id})
    )
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(Product.objects.filter(id=self.p2.id).exists())

  def test_product_create(self):
    new_product_data = {
      'name': 'New Test Product',
      'value': 20.00,
      'description': 'any description'
    }
    response = self.client.post(
      reverse('product-list'),
      new_product_data,
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # check if the product is present in the DB
    created_product_query = Product.objects.filter(name='New Test Product')
    self.assertTrue(created_product_query.exists())
    
    # get the product from the DB and check response data
    created_product = created_product_query.first()
    serializer = ProductSerializer(created_product)
    self.assertEqual(response.data, serializer.data)


  def test_product_update(self):
    updated_data = {
      'name': 'Product 1 Edited',
      'value': 10.0,
      'description': 'Edited',
    }
    response = self.client.put(
      reverse('product-detail', kwargs={'pk': self.p1.id}),
      updated_data,
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # check if data was edited
    self.p1.refresh_from_db()
    self.assertEqual(self.p1.name, updated_data['name'])
    self.assertEqual(self.p1.value, updated_data['value'])
    self.assertEqual(self.p1.description, updated_data['description'])