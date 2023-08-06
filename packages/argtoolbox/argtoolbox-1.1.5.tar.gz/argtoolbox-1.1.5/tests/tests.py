#! /usr/bin/env python
# -*- coding: utf-8 -*-


# This file is part of argtoolbox.
#
# argtoolbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# argtoolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LinShare user cli.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2013 Frédéric MARTIN
#
# Contributors list :
#
#  Frédéric MARTIN frederic.martin.fma@gmail.com
#




import unittest
import io
import binascii
import sys
import logging
from argtoolbox import Config, Element, Base64ElementHook


# pylint: disable-msg=R0904
# (too many methods)
class TestDefaultSection(unittest.TestCase):
    """Testing options of Element class."""

# pylint: disable-msg=C0103
# (invalid method name)
    def setUp(self):
        sample_config = """[DEFAULT]
elt_type_int=5
elt_type_str=bbb
elt_type_str2=bbb
elt_type_bool=False
elt_type_bool_t=True
elt_type_float = 1.00009
elt_required=
elt_no_value=
elt_type_base64=c2VjcmV0
elt_type_not_base64=cVjcmVé
elt_hidden="do not show"
elt_list_value=test aa aarrr kkkk mmmmm

\n"""
        self.c = Config("linshare-cli",
                        config_file=io.StringIO(sample_config),
                        desc=" simple user cli for linshare")
        self.s = self.c.get_default_section()

    def test_required(self):
        """Testing if the required parameter with a missing option"""
        self.s.add_element(Element('elt_missing', conf_required=True))
        self.assertRaises(ValueError, self.c.load)

    def test_required_without_value(self):
        # pylint: disable-msg=C0301
        """Testing if the required parameter with a blank value and default parameter fill with data"""
        self.s.add_element(Element(
            'elt_required',
            default="plop",
            conf_required=True))
        self.assertRaises(ValueError, self.c.load)

    def test_required_without_value_without_default(self):
        """Testing if the required parameter with a blank value"""
        self.s.add_element(Element(
            'elt_required',
            conf_required=True))
        self.assertRaises(ValueError, self.c.load)

    def test_no_attribute(self):
        # pylint: disable-msg=C0301
        """Testing AttributeError exception when we try to access to a missing attribute"""
        def raiseAttributeErrorException():
            """This method is trying to access to a missing attribute.
            It should raise an exception"""
            # pylint: disable-msg=W0104
            self.c.default.elt_missing
        self.assertRaises(AttributeError, raiseAttributeErrorException)

    def test_not_present(self):
        """Looking for a optional missing option"""
        self.s.add_element(Element(
            'elt_missing'))
        self.c.load()
        self.assertEqual(None, self.c.default.elt_missing.value)

    def test_not_present_with_default(self):
        """Looking for a optional missing option (default value is set)"""
        self.s.add_element(Element(
            'elt_missing',
            e_type=int,
            default=8))
        self.c.load()
        self.assertEqual(8, self.c.default.elt_missing.value)

    def test_type_int(self):
        """Trying to get a integer value from a option"""
        self.s.add_element(Element(
            'elt_type_int',
            e_type=int))
        self.c.load()
        self.assertEqual(5, self.c.default.elt_type_int.value)

    def test_type_str(self):
        """Trying to get a string value from a option"""
        self.s.add_element(Element(
            'elt_type_str'))
        self.c.load()
        self.assertEqual("bbb", self.c.default.elt_type_str.value)

    def test_type_bool(self):
        """Trying to get a boolean value from a option(=False)"""
        self.s.add_element(Element(
            'elt_type_bool', e_type=bool))
        self.c.load()
        self.assertFalse(self.c.default.elt_type_bool.value)

    def test_type_bool_true(self):
        """Trying to get a boolean value from a option(=True)"""
        self.s.add_element(Element(
            'elt_type_bool_t', e_type=bool))
        self.c.load()
        self.assertTrue(self.c.default.elt_type_bool_t.value)

    def test_type_float(self):
        """Trying to get a float value from a option"""
        self.s.add_element(Element(
            'elt_type_float', e_type=float))
        self.c.load()
        self.assertEqual(1.00009, self.c.default.elt_type_float.value)

    def test_type_list(self):
        """Trying to get a list of string values from a option"""
        self.s.add_element(Element(
            'elt_list_value', e_type=list))
        list_value = ['test', 'aa', 'aarrr', 'kkkk', 'mmmmm']
        self.c.load()
        self.assertEqual(list_value, self.c.default.elt_list_value.value)
        self.assertEqual(len(list_value),
                         len(self.c.default.elt_list_value.value))

    def test_hook_base64(self):
        # pylint: disable-msg=C0301
        """Testing if the Base64ElementHook will warn you if it is not base64 option"""
        self.s.add_element(Element(
            'elt_type_base64', hooks=[Base64ElementHook(), ]))
        self.c.load()
        self.assertEqual("secret", self.c.default.elt_type_base64.value.decode('utf8'))

    def test_hook_not_base64(self):
        # pylint: disable-msg=C0301
        """Testing if the Base64ElementHook will rise an exception for non base64 option"""
        self.s.add_element(Element(
            'elt_type_not_base64', hooks=[Base64ElementHook(), ]))
        self.assertRaises(TypeError, self.c.load)

    def test_hook_not_base64_2(self):
        """Testing if the Base64ElementHook will decode base64 option"""
        self.s.add_element(Element(
            'elt_type_not_base64', hooks=[Base64ElementHook(True), ]))
        # self.assertRaises(TypeError, self.c.load)
        self.c.load()
        self.assertEqual("cVjcmVé", self.c.default.elt_type_not_base64.value)

    def test_hidden(self):
        """Testing a hidden option"""
        self.s.add_element(Element(
            'elt_hidden', hidden=True))
        self.c.load()
        # TODO : code the hidden test

    def test_type_wrong_int(self):
        """Testing string value in integer option"""
        self.s.add_element(Element(
            'elt_type_str2', e_type=int))
        self.assertRaises(ValueError, self.c.load)

    def test_without_default_without_value_str(self):
        """Testing a missing string option with no default value"""
        self.s.add_element(Element(
            'elt_no_value'))
        self.assertRaises(ValueError, self.c.load)
        self.assertEqual(None, self.c.default.elt_no_value.value)

    def test_without_default_without_value_int(self):
        """Testing a missing integer option with no default value"""
        self.s.add_element(Element(
            'elt_no_value', e_type=int))
        self.assertRaises(ValueError, self.c.load)

    def test_without_default_without_value_float(self):
        """Testing a missing float option with no default value"""
        self.s.add_element(Element(
            'elt_no_value',
            e_type=float))
        self.assertRaises(ValueError, self.c.load)

if __name__ == '__main__':
    LOG = logging.getLogger('argtoolbox')
    STREAMHANDLER = logging.StreamHandler(sys.stdout)
    STREAMHANDLER.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s:%(funcName)s:%(message)s",
            "%H:%M:%S"))
    LOG.addHandler(STREAMHANDLER)
    LOG.setLevel(logging.FATAL)
    #log.setLevel(logging.DEBUG)
    unittest.main()
