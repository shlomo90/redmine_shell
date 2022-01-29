""" All Constants variables. """


import os


# TODO: Unify name.
UPDATE_RECOMMAND_FORMAT = "--> The version {} is released! Please upgrade program!"
UPDATE_WARNING_MESSAGE = "--> WARNING!: This version is an invalid version."

TEMPLATE_COMMON = """# Write down the Title and Time, Presenter, Audience.
# The "내용" part will be shown after saving this file.

h3. #{issue} {subject}

* 일시 : {year}. {month}. {day} ({weekday}) 00:00 ~ 00:00
* 진행자 :
* 참석자 :

# PLEASE DON'T REMOVE BELOW COMMENT BEFORE YOU SAVE THE FILE.
#
# Write down a review page with Redmine Syntax
# This contents directly upload to Redmine.
#
# Example
#
# h3. 일감번호 제목
#
# * 일시 : 2020. 10. 12 (금요일) 14:00 ~ 15:00
# * 진행자 :
# * 참석자 :
"""

TEMPLATE_CONTENT = """# Write down "내용" part with redmine textile syntax.
* 내용

# PLEASE DON'T REMOVE BELOW COMMENT BEFORE YOU SAVE THE FILE.
#
# Example
#
# * 내용
# ** 내용 1
# *** 내용1 부연설명
# ** 내용 2
# *** 내용2 부연설명
#
"""

BANNER_WELCOME = """Hello! It's redmine_shell. Thanks."""
HOME_PATH = os.getenv('HOME')
DATA_PATH = HOME_PATH + '/.redmine_shell'
