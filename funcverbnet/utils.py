#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2022/03/14
------------------------------------------
@Modify: 2022/03/14
------------------------------------------
@Description:
"""
import os
from pathlib import Path

ROOT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))


def load_pdata(filename):
    return str(ROOT_PATH / "data" / filename)
