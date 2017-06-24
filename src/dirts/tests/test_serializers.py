from django.test import TransactionTestCase

from ..api.serializers import CreateDefectSerializer


class SerializerTests(TransactionTestCase):
    def test_create_new_defect(self):
        data = { 
            'project_code': 'ABC.321',
            'release_id': 'v5.79.28.815',
            'priority': 'Low',
            'reference': 'A Title',
            'description': 'A description.',
            'comments': 'A few comments.',
        }
        serializer = CreateDefectSerializer(data=data)
        self.assertEquals(serializer.is_valid(), True, "{}".format(serializer.errors))
        defect = serializer.save()
        self.assertEqual(defect.project_code, data['project_code'])
