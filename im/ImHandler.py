#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from im.Im import Im


class ImHandler(object):
    DELIM = '#*&^$!'

    _COL_USER_NAME = 0
    _COL_USER_EMAIL = 1
    _COL_USER_FULLNAME = 2

    _COL_FIELD_NAME = 0
    _COL_FIELD_DISPLAY_NAME = 1
    _COL_FIELD_TYPE = 2

    _COL_BUG_ID = 0
    _COL_BUG_MODIFIED_TIME = 1

    _COL_PROJECT_NAME = 0
    _COL_PROJECT_IS_ACTIVE = 1

    _COL_TYPE_NAME = 0

    CREATE_DEFECT_PATTERN = re.compile(r'[\s\S]*Created Defect\s+(\d+)[\s\S]*')

    @staticmethod
    def execute(im_cmd, on_line, param = None):
        count = 0
        (code, out, err) = Im.execute(im_cmd)
        if code == 0:
            # insert lines
            lines = out.split('\n')
            for line in lines:
                count += 1
                line = line.strip()
                if len(line) <= 0:
                    continue

                # on line callback
                on_line(line, param)
        else:
            print('------------- im command -------------------')
            print(im_cmd)
            print('------------- im error message -------------')
            print(out)
            print(err)
            print('--------------------------------------------')
            return False, count

        return True, count

    @staticmethod
    def create_defect(project, summary, release_version, branch, username, password):
        cmds = ['im createissue --type=defect --user="%s" --password="%s"' % (username, password),
                '--field="In Project=%s"' % project,
                '--field="Summary=%s"' % summary,
                '--field="Frequency=10 - always to reproduce -> always to occurs, or definitive problem"',
                '--field="SW Release=%s"' % release_version,
                '--field="Regression=NO"',
                '--field="Detection=10 - very easy to detected-> >30%,or GCF/regulation problem"',
                '--field="Severity=10 - blocking->Permanent problem/Retrofit necessary/GCF Problem"',
                '--field="Perso ID=ZZ"',
                '--field="Component=TBD"',
                '--field="Function=Apps"',
                '--field="singleBranch=%s"' % branch]
        cmd = ' '.join(cmds)

        (code, out, err) = Im.execute(cmd)
        if code == 0:
            match = ImHandler.CREATE_DEFECT_PATTERN.match(out + err)
            return match.group(1), out, err
        else:
            return None, out, err

