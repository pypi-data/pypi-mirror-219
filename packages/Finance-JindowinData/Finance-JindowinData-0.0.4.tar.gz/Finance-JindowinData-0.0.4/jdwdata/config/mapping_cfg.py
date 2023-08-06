# -*- coding: utf-8 -*-

import yaml
import os, six
from jdwdata.kdutils.singleton import *


@six.add_metaclass(Singleton)
class MappingCfg(object):

    def __init__(self):
        self.mapping_cfg = {}
        if 'MAPPING_CFG_PATH' in os.environ.keys():
            with open(os.environ['MAPPING_CFG_PATH'], 'r',
                      encoding='utf8') as y:
                self.mapping_cfg = yaml.safe_load(y)

    def get_mapping_by_cols(self, cols, mapping):
        tbalis_cfg = self.mapping_cfg['table_alias'].copy()
        colalis_cfg = self.mapping_cfg['column_alias'].copy()
        if isinstance(mapping, dict) and len(mapping) > 0:
            colalis_cfg.update(mapping)
        data_dict = {}
        for col in cols:
            if col in colalis_cfg:
                data_dict[col] = colalis_cfg[col]
            else:
                tmp_map = {}
                strs = col.split('_')
                if len(strs) == 1:
                    raise ValueError(
                        " no table configured in table_alias, column alias:" +
                        col)
                tb = strs[0]
                if tb not in tbalis_cfg:
                    raise ValueError(tb +
                                     " not in table_alias, column alias:" +
                                     col)
                tmp_map['table'] = tbalis_cfg[tb]
                tmp_map['column'] = strs[1]
                if len(strs) == 3:
                    tmp_map['cond'] = {'PNQ': int(strs[2])}
                data_dict[col] = tmp_map
        return data_dict
