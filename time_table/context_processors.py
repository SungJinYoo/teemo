# -*- coding: utf-8 -*-
from core.constants import *


def time_table_constants(request):
    context = dict(
        WEEK_DAYS=WEEK_DAYS,
        WEEK_DAYS_KOR=WEEK_DAYS_KOR,
        WEEK_DAY_KEYS=WEEK_DAY_KEYS,
        TIME_TABLE_PERIODS=TIME_TABLE_PERIODS_VERBOSE,
        GRADE_VERBOSE=GRADES_VERBOSE,
        GRADE_VERBOSE_KOR=GRADES_VERBOSE_KOR,
        SEMESTER=SEMESTERS,
        SEMESTER_VERBOSE=SEMESTERS_VERBOSE,
    )

    return context
