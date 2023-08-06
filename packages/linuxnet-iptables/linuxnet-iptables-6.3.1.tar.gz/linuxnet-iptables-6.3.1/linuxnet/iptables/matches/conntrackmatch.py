# Copyright (c) 2021, 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-iptables.
#
# linuxnet-iptables is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-iptables is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-iptables. If not, see
# <https://www.gnu.org/licenses/>.

"""
This module provides matching against connection tracking attributes
"""

from typing import Iterable

from ..exceptions import IptablesParsingError
from ..deps import get_logger

from .match import Match, MatchParser
from .util import GenericCriterion

_logger = get_logger('linuxnet.iptables.matches.conntrackmatch')


class CtStateCriterion(GenericCriterion):
    """Compare against the connection tracking state

    The comparison value is a string.
    """
    def __init__(self, match):
        super().__init__(match, '--ctstate')


class CtStatusCriterion(GenericCriterion):
    """Compare against the connection tracking status

    The comparison value is a string.
    """
    def __init__(self, match):
        super().__init__(match, '--ctstatus')


class ConntrackMatch(Match):
    """Match against the connection tracking attributes.
    """
    def __init__(self):
        self.__ctstate_crit = None
        self.__ctstatus_crit = None

    @staticmethod
    def get_match_name() -> str:
        """Returns the **iptables(8)** match extension name
        """
        return 'conntrack'

    def get_criteria(self) -> Iterable['Criterion']:
        """Returns the conntrack match criteria: ctstate, ctstatus
        """
        return (self.__ctstate_crit, self.__ctstatus_crit)

    def ctstate(self) -> CtStateCriterion:
        """Match against the connection tracking state
        """
        if self.__ctstate_crit is None:
            self.__ctstate_crit = CtStateCriterion(self)
        return self.__ctstate_crit

    def ctstatus(self) -> CtStatusCriterion:
        """Matching against the connection tracking status
        """
        if self.__ctstatus_crit is None:
            self.__ctstatus_crit = CtStatusCriterion(self)
        return self.__ctstatus_crit

    # pylint: disable=too-many-branches
    @classmethod
    def parse(cls, parser: MatchParser) -> Match:
        """Match against ctstate, ctstatus::

            [!] ctstate <state>
            [!] ctstatus <status>

        The ctstate/ctstatus etc. (and the optional '!') has already been
        consumed.

        :meta private:
        """
        criteria_iter = parser.get_iter()
        # Return the match_name and (optionally) negation to the iterator
        # so that we can process them as part of the for-loop below.
        # The for-loop is designed to handle all conntrack-related criteria
        # (which we expect to appear consecutively).
        # Because of the rewind, this method is now responsible for handling
        # StopIteration errors.
        parser.rewind_match()
        match = ConntrackMatch()
        criterion = None
        negation = None
        rewind = False
        for token in criteria_iter:
            try:
                if token == '!':
                    negation = token
                    is_equal = False
                    criterion = next(criteria_iter)
                else:
                    is_equal = True
                    criterion = token
                if criterion == 'ctstate':
                    crit = match.ctstate()
                    if crit.is_set():
                        rewind = True
                        break
                    crit.compare(is_equal, next(criteria_iter))
                elif criterion == 'ctstatus':
                    crit = match.ctstatus()
                    if crit.is_set():
                        rewind = True
                        break
                    crit.compare(is_equal, next(criteria_iter))
                else:
                    rewind = True
                    break
                criterion = None
                negation = None
            except StopIteration as stopiter:
                if negation is not None or criterion is not None:
                    if criterion is None:
                        raise IptablesParsingError(
                                'negation without criterion') from stopiter
                    raise IptablesParsingError(
                                f'no value for {criterion}') from stopiter
        if rewind:
            criteria_iter.put_back(criterion)
            if negation is not None:
                criteria_iter.put_back(negation)
        return match
    # pylint: enable=too-many-branches


MatchParser.register_match('ctstate', ConntrackMatch)
MatchParser.register_match('ctstatus', ConntrackMatch)
