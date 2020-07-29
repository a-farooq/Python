##################################################
#
# author: Aamil Farooq - afarooq1
# date: 12 Sep 2019
#
##################################################

import os
import subprocess
import shlex

master_list = []


class Build:
    def __init__(self, cwd):
        # print("**********************inside init************************")
        self.__stack = [cwd]
        # print(self.__stack)
        self.__err1 = "cannot open file"
        self.__err2 = "cannot open input file"

    def run_command(self, command):
        # process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        process = subprocess.Popen(['echo', '"Hello stdout"'], stdout=subprocess.PIPE)
        # stdout = process.communicate()[0]
        output = process.stdout.readline()
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc

    def __build(self):
        # print("**********************inside build************************")
        cmd = "m"
        output = "yes"
        # return self.run_command(cmd)

        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        # process = subprocess.Popen([cmd], stdout=subprocess.PIPE)

        # output = process.stdout.readline()

        # result = subprocess.run(cmd, stdout=subprocess.PIPE)
        # result = subprocess.run(cmd, stdout=subprocess.PIPE, input=input())
        # result.stdout.decode('utf-8')

        # p = subprocess.Popen(['dir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out, err = p.communicate()
        # print(out)
        return output

    def do(self):
        # print("**********************inside do************************")
        while len(self.__stack) > 0:

            sol_dir = self.__get_dir()  # get solution dir from stack to build
            # print("sol dir: "+sol_dir)

            if not self.__change_dir(sol_dir):
                break

            output = self.__build()  # build solution n get output
            print(output)
            # find error string
            if self.__is_failing(output):
                print("FAILED " + sol_dir)
                sol_dir = self.__get_failed_sol(output)
                self.__add_dir(sol_dir)
                # if true, get failing dir and insert into stack
            else:
                print("PASSED " + sol_dir)
                self.__pop_dir() # remove the solution which passed

    def __is_failing(self, log):
        # print("**********************inside is_failing************************")
        if self.__err1 in log or self.__err2 in log:
            # print("FAILED")
            return True
        # print("PASSED")
        return False

    def __get_failed_sol(self, log):
        # print("**********************inside get_failed_sol************************")
        failed_sol = ""
        if self.__err1 in log:
            # print("err1")
            failed_sol = log.split(self.__err1)[1].split()[0]
        elif self.__err2 in log:
            # print("err2")
            failed_sol = log.split(self.__err2)[1].split()[0]

        if failed_sol.startswith('\'') and failed_sol.endswith('\''):
            failed_sol = failed_sol[1:-1]

        if failed_sol.lower().endswith('.lib'):
            failed_sol = os.path.dirname(failed_sol)  # get lib dir
            failed_sol = os.path.dirname(failed_sol)  # get solution dir

        # print("failed solution: "+failed_sol)
        return failed_sol

    def __change_dir(self, new_dir):
        # print("**********************inside change_dir************************")
        if os.path.exists(new_dir):
            os.chdir(new_dir)
            # print("cwd: "+os.getcwd())
            return True
        return False

    def __add_dir(self, dir):
        # print("**********************inside add_dir************************")
        self.__stack.append(dir)
        master_list.append(dir)
        # print("after add: {0}".format(self.stack))

    def __get_dir(self):
        # print("**********************inside get_dir************************")
        cur_dir = self.__stack[-1]
        # print("after get: {0}".format(self.stack))
        return cur_dir

    def __pop_dir(self):
        # print("**********************inside pop_dir************************")
        self.__stack.pop()
        # print("after pop: {0}".format(self.stack))


def main():
    cwd = os.getcwd()
    master_list.append(cwd)
    print(cwd)
    obj = Build(cwd)
    obj.do()
    print("master list: {0}".format(master_list))


if __name__ == '__main__':
    main()
