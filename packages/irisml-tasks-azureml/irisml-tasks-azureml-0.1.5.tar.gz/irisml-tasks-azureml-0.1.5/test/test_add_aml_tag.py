import unittest
from unittest.mock import patch
from irisml.tasks.add_aml_tag import Task


class TestAddAMLTag(unittest.TestCase):
    def test_add_aml_tag(self):
        """Test add_aml_tag function."""

        with patch('irisml.tasks.add_aml_tag.Run') as m_Run:
            tag, value = 'test_tag', 'test_value'
            Task(Task.Config(tag, value)).execute()
            m_Run.get_context().tag.assert_called_once_with(tag, value)

    def test_add_aml_tag_with_no_value(self):
        with patch('irisml.tasks.add_aml_tag.Run') as m_Run:
            tag = 'test_tag'
            Task(Task.Config(tag)).execute()
            m_Run.get_context().tag.assert_called_once_with(tag, None)
