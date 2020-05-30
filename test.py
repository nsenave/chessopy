# This file is part of the chessopy library.
# Copyright (C) 2020 Nicolas Sénave <email>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import chessopy
import unittest

class SquareTestCase(unittest.TestCase):

    def test_square(self):
        for rank_number in range(8) :
            for file_number in range(8) :
                square = chessopy.Square(rank_number, file_number)
                self.assertEqual(rank_number, square.get_rank())
                self.assertEqual(file_number, square.get_file())
    
    def test_square_name(self) :
        e4_square = chessopy.Square(3, 3)
        self.assertEqual('e4', e4_square.get_name())

#TODO: write the tests!!!
