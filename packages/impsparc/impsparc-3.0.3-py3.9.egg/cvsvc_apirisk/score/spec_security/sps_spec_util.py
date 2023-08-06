#!/usr/bin/python

import sys
from argparse import ArgumentParser
from configparser import ConfigParser

import networkit as nk


PATH_OPS_v2 = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch']


class QuerySpec(object):

    def __init__(self, spec_obj, openapi_ver):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        self.ROOT_NODE = '#'
        self.spec_obj = spec_obj
        self.G = nk.Graph(directed=True)
        self.node_id_mapping = dict()
        self.openapi_ver = openapi_ver

        node_name_sp = self.G.attachNodeAttribute('nodenamesp', str)
        node_name_raw = self.G.attachNodeAttribute('nodenameraw', str)
        child_type = self.G.attachNodeAttribute('childtype', str)

        self.node_attributes = {'node_name_sp': node_name_sp,
                                'node_name_raw': node_name_raw,
                                'child_type': child_type}

        self.load_spec2graph()

        self.create_node_id_key_mapping()
        # this variable to passed in get node index while querying node-id-mapping variable
        self.total_node_plus_ten = self.G.numberOfNodes() + 10

    def create_node_id_key_mapping(self):
        for node in self.G.iterNodes():
            self.node_id_mapping[self.node_attributes['node_name_sp'][node]] = node

    def get_desc_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'description':
                node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def get_param_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        data_types = {}
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'parameters':
                for param_obj_node in self.G.iterNeighbors(node):
                    node_names.append(self.node_attributes['node_name_sp'][param_obj_node])
                    for param_list in self.G.iterNeighbors(param_obj_node):
                        if self.openapi_ver == 'v3':
                            if self.node_attributes['node_name_raw'][param_list] == 'schema':
                                for _type in self.G.iterNeighbors(param_list):
                                    if self.node_attributes['node_name_raw'][_type] == 'type':
                                        for param_type_o3 in self.G.iterNeighbors(_type):
                                            param_type = self.node_attributes['node_name_sp'][param_type_o3]
                                            p_type = param_type.split('->')[-1]
                                            if p_type in data_types:
                                                data_types[p_type] = data_types[p_type] + 1
                                            else:
                                                data_types[p_type] = 1
                        elif self.openapi_ver == 'v2':
                            if self.node_attributes['node_name_raw'][param_list] == 'type':
                                for _type in self.G.iterNeighbors(param_list):
                                    param_type = self.node_attributes['node_name_sp'][_type]
                                    p_type = param_type.split('->')[-1]
                                    if p_type in data_types:
                                        data_types[p_type] = data_types[p_type] + 1
                                    else:
                                        data_types[p_type] = 1
        return node_names, data_types

    def get_op_objs_list(self):
        method_set = set()
        methods = self.get_op_objs()
        for method in methods:
            method_set.add(method.split('->')[-1])
        return list(method_set)

    def get_method_objs(self):
        node_names = {}
        for node in self.G.iterNodes():
            nodename = self.node_attributes['node_name_raw'][node]
            if nodename in self.get_op_objs_list():
                if nodename in node_names:
                    node_names[nodename] = node_names[nodename] + 1
                else:
                    node_names[nodename] = 1
        return node_names


    def get_header_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'headers':
                node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def get_item_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'items':
                node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def get_schema_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'schema':
                # Check if 'allOf'/'anyof'/'oneOf' operator is being invoked
                # in a schema. Note that the schema operations are not
                # applicable to items.
                opnode_present = False
                for schma_op in {'allOf', 'anyOf', 'oneOf'}:
                    schma_op_node = '%s->%s' % (node, schma_op)
                    if self.G.hasNode(self.node_id_mapping.get(schma_op_node, self.total_node_plus_ten)):
                        opnode_present = True
                        break

                if opnode_present and self.node_id_mapping.get(schma_op_node, None):
                    for idx_node in self.G.iterNeighbors(self.node_id_mapping[schma_op_node]):
                        node_names.append(self.node_attributes['node_name_sp'][idx_node])
                else:
                    node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def get_response_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        response_code_count = {}
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'responses':
                for n in self.G.iterNeighbors(node):
                    node_names.append(self.node_attributes['node_name_sp'][n])
                    response_code = self.node_attributes['node_name_raw'][n]
                    if response_code in response_code_count:
                        response_code_count[response_code] = response_code_count[response_code] + 1
                    else:
                        response_code_count[response_code] = 1

        return node_names, response_code_count

    def incorrect_securityreq_node(self, nodenamesp):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        global_security_node = '%s->security' % self.ROOT_NODE
        if nodenamesp == global_security_node:
            return False

        fields = nodenamesp.split('->')
        if ((len(fields) >= 5) and (fields[0] == self.ROOT_NODE)
                and (fields[1] == 'paths') and (fields[4] == 'security')):
            return False

        return True

    def get_security_objs(self, child_only=False):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        global_security_node = '%s->security' % self.ROOT_NODE

        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == 'security':
                if child_only and (node == global_security_node):
                    continue

                # Apply node filtering before checking
                nodenamesp = self.node_attributes['node_name_sp'][node]
                if self.incorrect_securityreq_node(nodenamesp):
                    continue

                node_names.append(nodenamesp)

        return node_names

    def get_securitydefn_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        global_secdefn_node = '%s->securityDefinitions' % self.ROOT_NODE

        node_names = []
        if self.node_id_mapping.get(global_secdefn_node, None):
            for node in self.G.iterNeighbors(self.node_id_mapping[global_secdefn_node]):
                node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def get_op_objs(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        node_names = []
        paths_node = '%s->paths' % self.ROOT_NODE
        if self.G.hasNode(self.node_id_mapping.get(paths_node, self.total_node_plus_ten)):
            for pathitem_node in self.G.iterNeighbors(self.node_id_mapping[paths_node]):
                for op in PATH_OPS_v2:
                    op_node = '%s->%s' % (self.node_attributes['node_name_sp'][pathitem_node], op)
                    if self.G.hasNode(self.node_id_mapping.get(op_node, self.total_node_plus_ten)):
                        node_names.append(op_node)

        return node_names

    def get_keyword_objs(self, keyword):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        if keyword == 'operation':
            return self.get_op_objs()
        if keyword == 'schema':
            return self.get_schema_objs()

        node_names = []
        for node in self.G.iterNodes():
            if self.node_attributes['node_name_raw'][node] == keyword:
                node_names.append(self.node_attributes['node_name_sp'][node])

        return node_names

    def build_graph_recurse(self, root_node, attr_name_sp_val_root, obj):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """

        def helper(created_graph, previous_node, attr_name_sp_val, obj):
            if obj == {}:
                obj = 'circular_ref'

            if type(obj) in {str, int, float}:
                # Add the value
                attr_name_sp_val_curr_node = '%s->%s' % (attr_name_sp_val, obj)
                curr_node = created_graph.addNode()
                created_graph.addEdge(previous_node, curr_node)
                self.node_attributes['node_name_sp'][curr_node] = attr_name_sp_val_curr_node
                self.node_attributes['node_name_raw'][curr_node] = str(obj)
                self.node_attributes['child_type'][curr_node] = 'null'

            elif type(obj) == dict:
                for k, v in obj.items():
                    attr_name_sp_val_curr_node = '%s->%s' % (attr_name_sp_val, k)
                    curr_node = created_graph.addNode()
                    created_graph.addEdge(previous_node, curr_node)
                    self.node_attributes['node_name_sp'][curr_node] = attr_name_sp_val_curr_node
                    self.node_attributes['node_name_raw'][curr_node] = k
                    self.node_attributes['child_type'][curr_node] = str(type(v))

                    helper(created_graph, curr_node, attr_name_sp_val_curr_node, v)

            elif type(obj) == list:
                for idx, elem in enumerate(obj):
                    attr_name_sp_val_curr_node = '%s->%d' % (attr_name_sp_val, idx)
                    curr_node = created_graph.addNode()
                    created_graph.addEdge(previous_node, curr_node)
                    self.node_attributes['node_name_sp'][curr_node] = attr_name_sp_val_curr_node
                    self.node_attributes['node_name_raw'][curr_node] = str(idx)
                    self.node_attributes['child_type'][curr_node] = str(type(elem))

                    helper(created_graph, curr_node, attr_name_sp_val_curr_node, elem)

            return created_graph

        self.G = helper(self.G, root_node, attr_name_sp_val_root, obj)

    def load_spec2graph(self):
        node = self.G.addNode()
        self.node_attributes['node_name_sp'][node] = self.ROOT_NODE
        self.node_attributes['node_name_raw'][node] = self.ROOT_NODE
        self.node_attributes['child_type'][node] = str(type(self.spec_obj))
        self.build_graph_recurse(
            root_node=node,
            attr_name_sp_val_root=self.ROOT_NODE,
            obj=self.spec_obj)

    def get_node_value(self, node_key):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        if node_key.endswith('__key__'):
            node_key = node_key[:-len('__key__')]
            node = self.node_id_mapping[node_key]
        else:
            for n in self.G.iterNeighbors(self.node_id_mapping[node_key]):
                node = n
                break

        return self.node_attributes['node_name_raw'][node]


def main(argv=sys.argv):
    apar = ArgumentParser()
    apar.add_argument('-c', dest='cfg_file')
    args = apar.parse_args()

    cpar = ConfigParser()
    cpar.read(args.cfg_file)


if __name__ == '__main__':
    sys.exit(main())
