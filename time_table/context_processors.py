# -*- coding: utf-8 -*-
from core.constants import *


def time_table_constants(request):
    context = dict(
        WEEK_DAYS=WEEK_DAYS,
        WEEK_DAYS_KOR=WEEK_DAYS_KOR,
        TIME_TABLE_PERIODS=TIME_TABLE_PERIODS,
        GRADE_VERBOSE=GRADE_VERBOSE,
        GRADE_VERBOSE_KOR=GRADE_VERBOSE_KOR,
        SEMESTER=SEMESTER,
        SEMESTER_VERBOSE=SEMESTER_VERBOSE,
    )

    return context
