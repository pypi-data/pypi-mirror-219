import json

"""
This Class is used for maintaining all the query fields
"""
class QueryBuilder:

    def __init__(self, tenant_id, query_params):
        self.tenant_id = tenant_id
        self.object_type = None
        self.filter_criteria = None
        self.fields = None
        self.group_by = None
        self.agg_function = None
        self.sort_by = None
        self.sort_order = 'ASC'
        self.page_no = 1
        self.page_size = 100
        self.prepare_builder(tenant_id, query_params)

    def prepare_builder(self, tenant_id, query_params):
        if query_params is None:
            return
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if 'object_type' in query_params and query_params['object_type'] is not None:
            self.object_type = query_params['object_type']
        if 'filter_criteria' in query_params and query_params['filter_criteria'] is not None:
            self.filter_criteria = query_params['filter_criteria']
        if 'fields' in query_params and query_params['fields'] is not None:
            self.fields = query_params['fields']
        if 'group_by' in query_params and query_params['group_by'] is not None:
            self.group_by = query_params['group_by']
        if 'agg_function' in query_params and query_params['agg_function'] is not None:
            self.agg_function = query_params['agg_function']
        if 'sort_by' in query_params and query_params['sort_by'] is not None:
            self.sort_by = query_params['sort_by']
        if 'sort_order' in query_params and query_params['sort_order'] is not None:
            self.sort_order = query_params['sort_order']
        if 'page_no' in query_params and query_params['page_no'] is not None:
            self.page_no = query_params['page_no']
        if 'page_size' in query_params and query_params['page_size'] is not None:
            self.page_size = query_params['page_size']


    def set_property(self, props):
        self.props = props

    def get_property(self, key, default_value):
        if key is None:
            return default_value
        if self.props is None and self.props[key] is None:
            return default_value
        if self.props[key] and self.props[key]:
            return self.props[key]

    def get_query(self):
        query = {}
        if self.object_type is not None:
            query['objectType'] = self.object_type
        if self.filter_criteria is not None:
            query['filterCriteria'] = self.filter_criteria
        if self.fields is not None:
            query['fields'] = self.fields
        if self.group_by is not None:
            query['groupBy'] = self.group_by
        if self.agg_function is not None:
            query['aggregateFunction'] = self.agg_function
        if self.sort_by is not None:
            query['sortBy'] = self.sort_by
        if self.sort_order is not None:
            query['sortByOrder'] = self.sort_order
        if self.page_no is not None:
            query['pageNo'] = self.page_no
        if self.page_size is not None:
            query['pageSize'] = self.page_size
        return query

    def set_page_no(self, page_no):
        self.page_no = page_no

    def set_page_size(self, page_size):
        self.page_size = page_size