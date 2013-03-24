# -*- coding: utf-8 -*-
#
# Copyright © 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
pkgdb tests for the Collection object.
'''

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from pkgdb.lib import model
from tests import Modeltests, create_collection


class Collectiontests(Modeltests):
    """ Collection tests. """

    def test_init_collection(self):
        """ Test the __init__ function of Collection. """
        create_collection(self.session)
        self.assertEqual(2, len(model.Collection.all(self.session)))

    def test_repr_collection(self):
        """ Test the __repr__ function of Collection. """
        create_collection(self.session)
        collections = model.Collection.all(self.session)
        self.assertEqual("Collection(u'Fedora', u'18', u'Active', 10, "
                         "publishurltemplate=None, pendingurltemplate=None,"
                         " summary=u'Fedora 18 release', description=None)",
                         collections[0].__repr__())
        self.assertEqual(collections[0].branchname, 'F-18')

    def test_search(self):
        """ Test the search function of Collection. """
        create_collection(self.session)

        collections = model.Collection.search(self.session, 'EPEL%')
        self.assertEqual(len(collections), 0)

        collections = model.Collection.search(self.session, 'F-%', 'Active')
        self.assertEqual("Collection(u'Fedora', u'18', u'Active', 10, "
                         "publishurltemplate=None, pendingurltemplate=None,"
                         " summary=u'Fedora 18 release', description=None)",
                         collections[0].__repr__())

    def test_api_repr(self):
        """ Test the api_repr function of Collection. """
        create_collection(self.session)
        collection = model.Collection.by_name(self.session, 'F-18')
        collection = collection.api_repr(1)
        self.assertEqual(collection.keys(), ['pendingurltemplate',
                         'publishurltemplate', 'version', 'name'])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Collectiontests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
