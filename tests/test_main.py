import pytest
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal

from src.main import get_columns_last_path_component, get_linked_columns, do_self_merge


# #####################################################################################################################
class TestGetColumnsWithIds(object):
    def test_on_empty_terms(self):
        test_argument_1 = pd.DataFrame({'A': [1, 2]})
        test_argument_2 = []
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == []

    def test_on_non_existent_terms(self):
        test_argument_1 = pd.DataFrame({'A': [1, 2], 'B': ['a', 'b']})
        test_argument_2 = ['id']
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == []

    def test_on_repeated_terms(self):
        test_argument_1 = pd.DataFrame({'A.id': [1, 2], 'B.di': ['a', 'b']})
        test_argument_2 = ['cy', 'id', 'id']
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == ['A.id']

    def test_on_not_exact_match(self):
        test_argument_1 = pd.DataFrame({'A.id': [1, 2], 'B.di': ['a', 'b']})
        test_argument_2 = ['ids']
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == []

    def test_on_terms_not_at_the_end(self):
        test_argument_1 = pd.DataFrame({'A.id': [1, 2, 3], 'B.id.source': [False, True, True], 'C.id': [12, 'e', None],
                                        'D.source.id': [2.4, 0, 'q'], 'E.identification': [3, 3, 45]})
        test_argument_2 = ['id']
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == ['A.id', 'C.id', 'D.source.id']

    def test_on_normal_arguments(self):
        test_argument_1 = pd.DataFrame({'A.b.id': [1, 2], 'B.cy': [3, 4], 'C.ids': [12, 'e'], 'D.dis': [2.4, 0]})
        test_argument_2 = ['id', 'ids']
        assert get_columns_last_path_component(test_argument_1, test_argument_2) == ['A.b.id', 'C.ids']


# #####################################################################################################################
class TestGetLinkedColumns(object):
    def test_on_empty_list(self):
        test_argument = []
        assert get_linked_columns(test_argument) == ([], [])

    def test_on_one_element_list(self):
        test_argument = ['source.@id']
        assert get_linked_columns(test_argument) == ([], [])

    def test_on_two_element_list(self):
        test_argument = ['source.cycle.@id', 'cycle.@id']
        assert get_linked_columns(test_argument) == (['cycle.@id'], ['source.cycle.@id'])

    def test_on_unlinked(self):
        test_argument = ['source.@id', 'cycle.@id']
        assert get_linked_columns(test_argument) == ([], [])

    def test_on_path_not_at_the_end(self):
        test_argument = ['source.@id', 'source.@id.Assessent.@id']
        assert get_linked_columns(test_argument) == ([], [])

    def test_on_repeated_elements(self):
        test_argument = ['source.@id', 'source.@id', 'cycle.source.@id']
        assert get_linked_columns(test_argument) == (['source.@id'], ['cycle.source.@id'])

    def test_on_normal_argument(self):
        test_argument = ['source.@id', 'cycle.source.@id', 'Assessment.source.@id', 'site.cycle.@id', 'site.@id',
                         'Assessment.site.@id']
        expected_output = (['source.@id', 'site.@id'],
                           ['cycle.source.@id', 'Assessment.source.@id', 'Assessment.site.@id'])
        assert get_linked_columns(test_argument) == expected_output


# #####################################################################################################################
class TestDoSelfMerge(object):
    def test_merge_on_empty_first_list(self):
        test_argument_1 = pd.DataFrame({'A.id': [1, 2, 3], 'B.id.source': [False, True, True], 'C.id': [12, 'e', None],
                                        'D.source.id': [2.4, 0, 'q'], 'E.identification': [3, 3, 45]})
        test_argument_2 = []
        test_argument_3 = ['D.source.id', 'B.id.source']
        assert_frame_equal(do_self_merge(test_argument_1, test_argument_2, test_argument_3), test_argument_1)

    def test_merge_on_empty_second_list(self):
        test_argument_1 = pd.DataFrame({'A.id': [1, 2, 3], 'B.id.source': [False, True, True], 'C.id': [12, 'e', None],
                                        'D.source.id': [2.4, 0, 'q'], 'E.identification': [3, 3, 45]})
        test_argument_2 = ['A.id']
        test_argument_3 = []
        assert_frame_equal(do_self_merge(test_argument_1, test_argument_2, test_argument_3), test_argument_1)

    def test_merge_on_empty_lists(self):
        test_argument_1 = pd.DataFrame(
            {'A.id': [1, 2, 3], 'B.id.source': [False, True, True], 'C.id': [12, 'e', None],
             'D.source.id': [2.4, 0, 'q'], 'E.identification': [3, 3, 45]})
        test_argument_2 = []
        test_argument_3 = []
        assert_frame_equal(do_self_merge(test_argument_1, test_argument_2, test_argument_3), test_argument_1)

    def test_merge_on_empty_lists(self):
        test_argument_1 = pd.DataFrame(
            {'A.id': [1, 2, 3], 'B.id.source': [False, True, True], 'C.id': [12, 'e', None],
             'D.source.id': [2.4, 0, 'q'], 'E.identification': [3, 3, 45]})
        test_argument_2 = []
        test_argument_3 = []
        assert_frame_equal(do_self_merge(test_argument_1, test_argument_2, test_argument_3), test_argument_1)

    def test_merge_on_normal_data(self):
        test_argument_1 = pd.DataFrame(
            {'A.id': [np.nan, np.nan, 3.0], 'B.id.source': [np.nan, np.nan, True], 'C.id': [12.0, 23.0, np.nan],
             'D.source.id': [4.0, 0, np.nan], 'E.A.id': [3.0, 3.0, np.nan]})
        test_argument_2 = ['A.id']
        test_argument_3 = ['E.A.id']
        expected_output = pd.DataFrame(
            {'A.id': [3.0, 3.0], 'B.id.source': [True, True], 'C.id': [12.0, 23.0],
             'D.source.id': [4.0, 0], 'E.A.id': [3.0, 3.0]})
        assert_frame_equal(do_self_merge(test_argument_1, test_argument_2, test_argument_3), expected_output)
