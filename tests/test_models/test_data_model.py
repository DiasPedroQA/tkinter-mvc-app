# from src.models.data_model import DataModel
# import unittest

# class TestDataModel(unittest.TestCase):

#     def setUp(self):
#         self.data_model = DataModel()

#     def test_initial_state(self):
#         self.assertEqual(self.data_model.data, [])

#     def test_add_data(self):
#         self.data_model.add_data('test_item')
#         self.assertIn('test_item', self.data_model.data)

#     def test_remove_data(self):
#         self.data_model.add_data('test_item')
#         self.data_model.remove_data('test_item')
#         self.assertNotIn('test_item', self.data_model.data)

#     def test_get_data(self):
#         self.data_model.add_data('test_item')
#         data = self.data_model.get_data()
#         self.assertEqual(data, ['test_item'])

#     def test_clear_data(self):
#         self.data_model.add_data('test_item')
#         self.data_model.clear_data()
#         self.assertEqual(self.data_model.data, [])

# if __name__ == '__main__':
#     unittest.main()
