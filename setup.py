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
import setuptools

setuptools.setup(
    name="chessopy",
    version=chessopy.__version__,
    author=chessopy.__author__,
    # author_email=chessopy.__email__,
    description=chessopy.__doc__.replace("\n", " ").strip(),
    license="GPL-3.0+",
    keywords="chessopy chess opening learn train training gui graphical interface",
    url="https://github.com/nsenave/chessopy",
    packages=["chessopy"],
    test_suite="test",
    python_requires=">=3.6",
    classifiers=[ # https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent", # TODO: not so shure
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)