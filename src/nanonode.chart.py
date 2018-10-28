# -*- coding: utf-8 -*-
# Description: NanoNode netdata python.d module
# Author: Joohansson
# SPDX-License-Identifier: GPL-3.0-or-later
# Updated: 2018-10-27

from bases.FrameworkServices.UrlService import UrlService
import json
from collections import deque #for array shifting

# default module values (can be overridden per job in `config`)
update_every = 6 #update chart every 6 second (changing this will change TPS Ave interval to interval*50 sec)
priority = 1000 #where it will appear on the main stat page and menu (60000 will place it last)
retries = 60

# default job configuration (overridden by python.d.plugin)
# config = {'local': {
#             'update_every': update_every,
#             'retries': retries,
#             'priority': priority,
#             'url': 'http://localhost/api.php'
#          }}

# charts order (can be overridden if you want less charts, or different order)

#ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'tps_50', 'weight', 'delegators', 'block_sync', 'account_balance', 'uptime']
ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'tps_50', 'block_sync', 'uptime']

CHARTS = {
    'block_count': {
        'options': [None, 'Block Count', 'Blocks', 'Blocks','nano.blocks', 'area'],
        'lines': [
            ["blocks", None, 'absolute']
        ]
    },
    'unchecked': {
        'options': [None, 'Unchecked Blocks', 'Blocks', 'Unchecked','nano.unchecked', 'line'],
        'lines': [
            ["unchecked", None, 'absolute']
        ]
    },
    'peers': {
        'options': [None, 'Peers', 'Peers', 'Peers','nano.peers', 'line'],
        'lines': [
            ["peers", None, 'absolute']
        ]
    },
    'weight': {
        'options': [None, 'Voting Weight', 'nano', 'Weight','nano.weight', 'line'],
        'lines': [
            ["weight", None, 'absolute', 1, 1000]
        ]
    },
    'delegators': {
        'options': [None, 'Delegators', 'accounts', 'Delegators','nano.delegators', 'line'],
        'lines': [
            ["delegators", None, 'absolute']
        ]
    },
    'block_sync': {
        'options': [None, 'Block Sync', '%', 'Sync','nano.sync', 'line'],
        'lines': [
            ["block_sync", None, 'absolute', 1, 1000]
        ]
    },
    'account_balance': {
        'options': [None, 'Account Balance', 'nano', 'Balance','nano.balance', 'line'],
        'lines': [
            ["account_balance", None, 'absolute', 1, 1000]
        ]
    },
    'uptime': {
        'options': [None, 'Node Uptime', '%', 'Uptime','nano.uptime', 'line'],
        'lines': [
            ["uptime", None, 'absolute', 1, 1000]
        ]
    },
    'tps': {
        'options': [None, 'Node TPS', 'tx/s', 'TPS','nano.tps', 'line'],
        'lines': [
            ["tps", None, 'absolute',1 , 1000]
        ]
    },
    'tps_50': {
        'options': [None, 'Node TPS Ave', 'tx/s', 'TPS Ave 5 min','nano.tps50', 'line'],
        'lines': [
            ["tps_50", None, 'absolute', 1, 1000]
        ]
    }
}

class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.url = self.configuration.get('url', 'http://localhost/api.php')
        self.order = ORDER
        self.definitions = CHARTS
        self.blocks_old = 0 #block count previous poll
        self.tps_old = deque([0]*50) #tps history last 50 polls, init with 50 zeroes

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """

        #Convert raw api data to json
        try:
            raw = self._get_raw_data()
            parsed = json.loads(raw)
        except AttributeError:
            return None

        #Keys to read from api data with the first entry is keys used by the charts
        apiKeys = [('blocks','currentBlock',int,1),('unchecked','uncheckedBlocks',int,1),('peers','numPeers',int,1),
            ('weight','votingWeight',float,1000),('block_sync','blockSync',float,1000),('account_balance','accBalanceMnano',float,1000)]
        apiKeysNinja = [('delegators','delegators',int,1),('uptime','uptime',float,1000)]
        r = dict()

        #Extract data from json based on default node monitor keys
        for new_key, orig_key, keytype, mul in apiKeys:
            try:
                r[new_key] = keytype(mul * parsed[orig_key])
            except Exception:
                continue

        #Extract data from json based on NinjaKeys
        for new_key, orig_key, keytype, mul in apiKeysNinja:
            try:
                r[new_key] = keytype(mul * parsed['nodeNinja'][orig_key])
            except Exception:
                continue

        #Calculate tps based on previous block read
        if (self.blocks_old == 0):
            self.blocks_old = r['blocks'] #Initialize with block count first time to not get large tps before running one iteration
        r['tps'] = 1000 * (r['blocks']-self.blocks_old) / update_every #use previous iteration (multiply 1000 and divide with 1000 in chart to get decimals)
        self.blocks_old = r['blocks'] #update for next iteration
        self.tps_old.append(r['tps'])
        self.tps_old.popleft()

        #Calculate tps past 50 iterations based on average tps
        sum = 0
        for tps in self.tps_old:
            sum = sum + tps
        r['tps_50'] = sum / len(self.tps_old) 

        return r or None
