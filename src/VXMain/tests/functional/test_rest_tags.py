from VXMain.tests import *

class TestTagsController(TestController):

    def test_index(self):
        response = self.app.get(url('rest_tags'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_rest_tags', format='xml'))

    def test_create(self):
        response = self.app.post(url('rest_tags'))

    def test_new(self):
        response = self.app.get(url('rest_new_tag'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_rest_new_tag', format='xml'))

    def test_update(self):
        response = self.app.put(url('rest_tag', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('rest_tag', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('rest_tag', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('rest_tag', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('rest_tag', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_rest_tag', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('rest_edit_tag', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_rest_edit_tag', id=1, format='xml'))
