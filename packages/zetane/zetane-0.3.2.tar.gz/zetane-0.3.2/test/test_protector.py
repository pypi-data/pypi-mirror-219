import zetane
import unittest

URL = 'http://localhost:8000/api/'
# For running tests, need to generate a local protector API key
# set it with an env var `ZETANE_API_KEY`

class API_Test(unittest.TestCase):
    def test_auth(self):
        zetane.config()
        self.assertIsNotNone(zetane.default_client.user)

    def test_default_org(self):
        zetane.config()
        self.assertIsNotNone(zetane.default_client.org)

    def test_create_project(self):
        zetane.config()
        res = zetane.create_project("Test Project 1")
        self.assertEqual(res.status_code, 201)
        res = zetane.delete_project("Test Project 1")
        self.assertEqual(res.status_code, 200)

    def test_upload_dataset(self):
        zetane.config()
        zetane.delete_project("Birds")
        zetane.create_project("Birds")
        res = zetane.upload_dataset('test/data/birds.zip', project="Birds")
        json_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_res['name'], 'birds.zip')
        self.assertEqual(json_res['upload_status'], {'status': 'Ready'})
        res = zetane.delete_project("Birds")
        self.assertEqual(res.status_code, 200)

    def test_upload_model(self):
        zetane.config()
        zetane.create_project("Birds")
        res = zetane.upload_model('test/data/model.pt', project="Birds")
        json_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_res['name'], 'model.pt')
        self.assertEqual(json_res['upload_status'], {'status': 'Ready'})
        res = zetane.delete_project("Birds")
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()



