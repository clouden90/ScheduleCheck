#!/usr/bin/env python3
"""
driver for the schedule-conflict library
"""


from datetime import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
import filecmp
import schedulecheck


class meeting(object):

    def __init__(self, fname=[], method=[], output=[]):
        self.fname = fname
        self.method = method
        self.output = output
        self.conflicts = []

    def readFile(self):
        try:
            fileObj = open(self.fname, "r")
            self.data = fileObj.read().splitlines()
            fileObj.close()
            # remove '-'
            self.data_ = [(interval.split(' - ')) for interval in self.data]
            # Unify time format
            for i, d in enumerate(self.data_):
                self.data_[i][:] = [datetime.strptime(t, '%H:%M')
                                    .strftime('%H:%M')
                                    for t in d]
        except IOError:
            print("File not accessible!!! Please check!!!")
            exit()

    def writefile(self):
        head_tail = os.path.split(self.output)
        isExist = os.path.exists(head_tail[0])
        if not isExist:
            os.makedirs(head_tail[0])
        fileObj = open(self.output, "w")
        for str1, str2 in self.conflicts:
            str1_ = ("-".join([str1[0], str1[1]]))
            str2_ = ("-".join([str2[0], str2[1]]))
            print(f"{str1_} and {str2_} conflict")
            print(f"{str1_} and {str2_} conflict", file=fileObj)
        fileObj.close()

    def test(self):
        f1 = self.output
        if self.method <= 1:
            fref = './reference/method1_ref.txt'
        else:
            fref = './reference/method2_ref.txt'
        result = filecmp.cmp(f1, fref)
        assert result is True


def main():
    desc = "A schedule-conflict checking script."
    parser = ArgumentParser(
           description=desc,
           formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-f', '--filename', help='Name of input schedule file',
        type=str, default='example/schedule.txt', required=False)
    parser.add_argument(
        '-m', '--method', help='choose simple method (1) or Interval Tree (2)',
        type=int, default=1, required=False)
    parser.add_argument(
        '-o', '--output', help='Output file name of schedule-conflict',
        type=str, default='./schedule_check.txt', required=False)
    parser.add_argument(
        '-t', '--test', help='compare results to reference answers',
        type=int, default=0, required=False)
    parser.add_argument(
        '-v', '--version', action='version', version='1.0.0')

    #
    args = parser.parse_args()

    # Initialize meeting class
    schedule = meeting(fname=args.filename, method=args.method,
                       output=args.output)

    # read schedule from file
    schedule.readFile()

    # check conflict
    if schedule.method == 1:
        schedule.conflicts = schedulecheck.meetinglib.conflicts_check1(
         schedule.data_)
    elif schedule.method == 2:
        schedule.conflicts = schedulecheck.meetinglib.conflicts_check2(
         schedule.data_)
    else:
        print("--method can only be 1 or 2 now!!! STOP!!!")
        exit()

    # output
    schedule.writefile()

    # test
    if args.test == 1:
        schedule.test()


if __name__ == '__main__':
    main()
