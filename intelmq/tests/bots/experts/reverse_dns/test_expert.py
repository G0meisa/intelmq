# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.reverse_dns.expert import ReverseDnsExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.0.43.7",  # icann.org
                 "destination.ip": "192.0.43.8",  # iana.org
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.0.43.7",
                  "source.reverse_domain_name": "icann.org.",
                  "destination.ip": "192.0.43.8",
                  "destination.reverse_domain_name": "icann.org.",
                  # manual verfication shows another result:
                  # "destination.reverse_domain_name": "43-8.any.icann.org.",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.reverse_domain_name": "",
                   }


class TestReverseDnsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = ReverseDnsExpertBot
        self.default_input_message = json.dumps({'__type': 'Report'})

    def test_ipv4_lookup(self):
        self.input_message = json.dumps(EXAMPLE_INPUT)
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_OUTPUT)

    @unittest.expectedFailure
    def test_ipv6_lookup(self):
        self.input_message = json.dumps(EXAMPLE_INPUT6)
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_OUTPUT6)


if __name__ == '__main__':
    unittest.main()