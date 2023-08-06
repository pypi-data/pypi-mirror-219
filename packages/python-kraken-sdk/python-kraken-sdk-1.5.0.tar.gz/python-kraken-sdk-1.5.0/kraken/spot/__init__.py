#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that provides the Spot REST clients and utility functions."""

# pylint: disable=unused-import
from kraken.spot.funding import Funding
from kraken.spot.market import Market
from kraken.spot.orderbook import OrderbookClient
from kraken.spot.staking import Staking
from kraken.spot.trade import Trade
from kraken.spot.user import User
from kraken.spot.ws_client import KrakenSpotWSClient
