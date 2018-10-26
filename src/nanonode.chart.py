# -*- coding: utf-8 -*-
# Description: NanoNode netdata python.d module
# Author: Joohansson
# SPDX-License-Identifier: GPL-3.0-or-later

from bases.FrameworkServices.UrlService import UrlService
import json

# default module values (can be overridden per job in `config`)
update_every = 5 #update chart every x second
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

#ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'weight', 'delegators', 'block_sync', 'account_balance', 'uptime']
ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'block_sync', 'uptime']

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
            ["weight", None, 'absolute']
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
            ["block_sync", None, 'absolute']
        ]
    },
    'account_balance': {
        'options': [None, 'Account Balance', 'nano', 'Balance','nano.balance', 'line'],
        'lines': [
            ["account_balance", None, 'absolute']
        ]
    },
    'uptime': {
        'options': [None, 'Node Uptime', '%', 'Uptime','nano.uptime', 'line'],
        'lines': [
            ["uptime", None, 'absolute']
        ]
    },
    'tps': {
        'options': [None, 'Node TPS', 'tx/s', 'TPS','nano.tps', 'line'],
        'lines': [
            ["tps", None, 'absolute']
        ]
    }
}

class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.url = self.configuration.get('url', 'http://localhost/api.php')
        self.order = ORDER
        self.definitions = CHARTS
        self.blocks_old = 0

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
        apiKeys = [('blocks','currentBlock',int),('unchecked','uncheckedBlocks',int),('peers','numPeers',int),('weight','votingWeight',float),('block_sync','blockSync',float),('account_balance','accBalanceMnano',float)]
        apiKeysNinja = [('delegators','delegators',int),('uptime','uptime',float)]
        r = dict()

        #Extract data from json based on default node monitor keys
        for new_key, orig_key, keytype in apiKeys:
            try:
                r[new_key] = keytype(parsed[orig_key])
            except Exception:
                continue

        #Extract data from json based on NinjaKeys
        for new_key, orig_key, keytype in apiKeysNinja:
            try:
                r[new_key] = keytype(parsed['nodeNinja'][orig_key])
            except Exception:
                continue

        #Calculate tps based on previous block read
        r['tps'] = (r['blocks']-self.blocks_old) / update_every
        self.blocks_old = r['blocks'] #update for next iteration

        return r or None
