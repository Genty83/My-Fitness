from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, SubCategory
from .forms import ProductForm
from reviews.models import ProductReview


class ProductViewsTest(TestCase):

    def setUp(self):
        """
        Set up the test client and create initial data for testing.
        """
        self.client = Client()
        self.category = Category.objects.create(name='Category 1')
        self.sub_category = SubCategory.objects.create(
            name='SubCategory 1', category_id=self.category)
        self.product = Product.objects.create(
            name='Product 1',
            category_id=self.category,
            subcategory_id=self.sub_category,
            price=100.00
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.product_review = ProductReview.objects.create(
            product=self.product,
            username='testuser',
            title='Great product',
            review='This is a great product!',
            rating=4
        )

    def test_all_products_view(self):
        """
        Test the all_products view to ensure it returns a 200 status code and 
        uses the correct template.
        """
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/all_products.html')

    def test_product_detail_view(self):
        """
        Test the product_detail view to ensure it returns a 200 status code, 
        uses the correct template, and contains the product name.
        """
        response = self.client.get(
            reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, self.product.name)

    def test_add_product_view_get(self):
        """
        Test the add_product view (GET request) to ensure it returns a 200 
        status code and uses the correct template. Requires user login.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_add_product_view_post(self):
        """
        Test the add_product view (POST request) to ensure a product is 
        successfully added and the user is redirected to the product detail 
        page. Requires user login.
        """
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'name': 'Product 2',
            'category_id': self.category.id,
            'subcategory_id': self.sub_category.id,
            'price': 150.00
        }
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_detail', args=[2]))

    def test_edit_product_view_get(self):
        """
        Test the edit_product view (GET request) to ensure it returns a 200 
        status code and uses the correct template. Requires user login.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_edit_product_view_post(self):
        """
        Test the edit_product view (POST request) to ensure the product is 
        successfully updated and the user is redirected to the product detail 
        page. Requires user login.
        """
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'name': 'Product 1 Updated',
            'category_id': self.category.id,
            'subcategory_id': self.sub_category.id,
            'price': 200.00
        }
        response = self.client.post(
            reverse('edit_product', args=[self.product.id]), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            reverse('product_detail', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Product 1 Updated')

    def test_delete_product_view_post(self):
        """
        Test the delete_product view (POST request) to ensure the product is 
        successfully deleted and the user is redirected to the all products 
        page. Requires user login.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('all_products'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_sale_products_view(self):
        """
        Test the sale_products view to ensure it returns a 200 status code and 
        uses the correct template.
        """
        response = self.client.get(reverse('sale_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/sale_products.html')
