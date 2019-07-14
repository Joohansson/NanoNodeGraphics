# -*- coding: utf-8 -*-
# Description: NanoNode netdata python.d module
# Author: Joohansson
# SPDX-License-Identifier: GPL-3.0-or-later
# Updated: 2019-02-08

from bases.FrameworkServices.UrlService import UrlService
import json
from collections import deque #for array shifting

# default module values (can be overridden per job in `config`)
update_every = 6 #update chart every 6 second (changing this will change TPS Ave interval to interval*50 sec)
priority = 1000 #where it will appear on the main stat page and menu (60000 will place it last)
#retries = 60

# default job configuration (overridden by python.d.plugin)
# config = {'local': {
#             'update_every': update_every,
#             'retries': retries,
#             'priority': priority,
#             'url': 'http://localhost/api.php'
#          }}

# charts order (can be overridden if you want less charts, or different order)

#ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'tps_50', 'cps', 'cps_50', 'confirmations', 'weight', 'delegators', 'block_sync', 'account_balance', 'uptime']
ORDER = ['block_count', 'unchecked', 'peers', 'tps', 'tps_50', 'confirmations', 'block_sync', 'uptime']

CHARTS = {
    'block_count': {
        'options': [None, 'Block Count', 'blocks', 'Blocks','nano.blocks', 'area'],
        'lines': [
            ["saved_blocks", "saved", None, 'absolute'],
            ["confirmed_blocks", "conf", None, 'absolute']
        ]
    },
    'unchecked': {
        'options': [None, 'Unchecked Blocks', 'blocks', 'Unchecked','nano.unchecked', 'line'],
        'lines': [
            ["unchecked", None, 'absolute']
        ]
    },
    'peers': {
        'options': [None, 'Peers', 'peers', 'Peers','nano.peers', 'line'],
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
            ["bps", None, 'absolute', 1 , 1000],
            ["cps", None, 'absolute', 1 , 1000]
        ]
    },
    'tps_50': {
        'options': [None, 'Node TPS Ave', 'tx/s', 'TPS Ave 5 min','nano.tps50', 'line'],
        'lines': [
            ["bps_50", None, 'absolute', 1, 1000],
            ["cps_50", None, 'absolute', 1 , 1000]
        ]
    },
    'confirmations': {
        'options': [None, 'Confirmation Time', 'ms', 'Conf-Time Max 5min/2048tx','nano.conf', 'line'],
        'lines': [
            ["average", None, 'absolute'],
            ["perc_50", None, 'absolute'],
            ["perc_75", None, 'absolute'],
            ["perc_90", None, 'absolute'],
            #["perc_95", None, 'absolute'],
            ["perc_99", None, 'absolute']
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
        self.cemented_old = 0 #cemented count previous poll
        self.cps_old = deque([0]*50) #cps history last 50 polls, init with 50 zeroes

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
        apiKeys = [('saved_blocks','currentBlock',int,1),('confirmed_blocks','cementedBlocks',int,1),('unchecked','uncheckedBlocks',int,1),('peers','numPeers',int,1),
            ('weight','votingWeight',float,1000),('block_sync','blockSync',float,1000),('account_balance','accBalanceMnano',float,1000)]
        apiKeysNinja = [('delegators','delegators',int,1),('uptime','uptime',float,1000)]
        apiKeysConf = [('average','average',int,1),('perc_50','percentile50',int,1),('perc_75','percentile75',int,1),('perc_90','percentile90',int,1),('perc_95','percentile95',int,1),('perc_99','percentile99',int,1)]
        r = dict()

        #Extract data from json based on default node monitor keys
        for new_key, orig_key, keytype, mul in apiKeys:
            try:
                r[new_key] = keytype(mul * parsed[orig_key])
            except Exception:
                r[new_key] = 0 #replace with 0 if value missing from API
                continue

        #Extract data from json based on NinjaKeys
        for new_key, orig_key, keytype, mul in apiKeysNinja:
            try:
                r[new_key] = keytype(mul * parsed['nodeNinja'][orig_key])
            except Exception:
                r[new_key] = 0 #replace with 0 if value missing from API
                continue

        #Extract data from json based on confirmationInfo
        for new_key, orig_key, keytype, mul in apiKeysConf:
            try:
                r[new_key] = keytype(mul * parsed['confirmationInfo'][orig_key])
            except Exception:
                r[new_key] = 0 #replace with 0 if value missing from API
                continue


        #Replace values with zero if missing
        #try:
        #    val = r['uptime']
        #except Exception:
        #    r['uptime'] = 0

        #Calculate bps based on previous block read
        if (self.blocks_old == 0):
            self.blocks_old = r['saved_blocks'] #Initialize with block count first time to not get large tps before running one iteration
        r['bps'] = 1000 * (r['saved_blocks']-self.blocks_old) / update_every #use previous iteration (multiply 1000 and divide with 1000 in chart to get decimals)
        self.blocks_old = r['saved_blocks'] #update for next iteration
        self.tps_old.append(r['bps'])
        self.tps_old.popleft()

        #Calculate bps past 50 iterations based on average tps
        sum = 0
        for tps in self.tps_old:
            sum = sum + tps
        r['bps_50'] = sum / len(self.tps_old)

        #Calculate cps based on previous block read
        if (self.cemented_old == 0):
            self.cemented_old = r['confirmed_blocks'] #Initialize with block count first time to not get large tps before running one iteration
        r['cps'] = 1000 * (r['confirmed_blocks']-self.cemented_old) / update_every #use previous iteration (multiply 1000 and divide with 1000 in chart to get decimals)
        self.cemented_old = r['confirmed_blocks'] #update for next iteration
        self.cps_old.append(r['cps'])
        self.cps_old.popleft()

        #Calculate tps past 50 iterations based on average tps
        sum = 0
        for cps in self.cps_old:
            sum = sum + cps
        r['cps_50'] = sum / len(self.cps_old)

        return r or None
