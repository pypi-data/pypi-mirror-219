# -*- coding: utf-8 -*-
"""
DO NOT FORGET to change back the relative import of db_utils in analy_utils

@author: FranciscoPena
"""

import pandas as pd, numpy as np
import analy_utils, db_utils

# GET CREDENTIALS ++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os, sys, git
git_root = git.Repo(os.path.abspath(__file__),
                    search_parent_directories=True).git.rev_parse('--show-toplevel')
cred_path = os.path.join(git_root, '../credentials')
sys.path.append(cred_path)
import credentials as cred

db_dict = {'hkiweb' : cred.hkiweb,
           'hkimarket' : cred.hkimarket,
           'hkisocial' : cred.hkisocial,
           'hkiads' : cred.hkiads}

#%% FETCH DATA ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
query= """
select *
from visits
where "date" > '2021-04-01' and "date" < '2023-04-02'
"""
cursor, conn = db_utils.database_connect('hkisocial', db_dict)
visit= pd.read_sql(query, conn)
cursor.close()
conn.close()

visit= analy_utils.clean_visits(visit, db_dict)

analy_utils.clean_standalone_action(visit, 'pageview', 1)

engagement = analy_utils.assign_cluster(visit)
engagement = engagement.reset_index().merge(
    analy_utils.get_cluster_grades(), how='left', on='engagement_type')
visit = visit.merge(engagement, how='inner', on='visit_id')
