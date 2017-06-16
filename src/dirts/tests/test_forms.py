
from django.test import SimpleTestCase

from ..forms import CreateDefectForm
from ..models import Defect, Priority, Status


class DefectFormTests(SimpleTestCase):
    @staticmethod
    def _test_form_data_with_comments():
        return {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
            'comments': 'some comments',
        }

    @staticmethod
    def _test_form_data_without_comments():
        return {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
        }
    
    def _assert_empty_field_fail_form(self, field_name, value):
        kwargs = self._test_form_data_with_comments()
        kwargs[field_name] = value
        form = CreateDefectForm(data=kwargs)
        self.assertEqual(form.is_valid(), False)
        
    def test_should_fail_valid_create_defect_form_with_empty_project_code(self):
        self._assert_empty_field_fail_form('project_code', '')
        
    def test_should_fail_valid_create_defect_form_with_empty_release_id(self):
        self._assert_empty_field_fail_form('release_id', '')
        
    def test_should_fail_valid_create_defect_form_with_empty_priority(self):
        self._assert_empty_field_fail_form('priority', None)
    
    def test_should_fail_valid_create_defect_form_with_empty_reference(self):
        self._assert_empty_field_fail_form('reference', '')
    
    def test_should_fail_valid_create_defect_form_with_empty_description(self):
        self._assert_empty_field_fail_form('description', '')
    
    def test_should_pass_valid_create_defect_form_with_comments(self):
        form = CreateDefectForm(data=self._test_form_data_with_comments())
        self.assertEqual(form.is_valid(), True)
    
    def test_should_pass_valid_create_defect_form_without_comments(self):
        form = CreateDefectForm(data=self._test_form_data_without_comments())
        self.assertEqual(form.is_valid(), True)
