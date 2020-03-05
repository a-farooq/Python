import sys
import subprocess
from subprocess import call


def delete():
    print("delete branch")
    if len(sys.argv) != 3:
        usage()
        return

    branch_name = sys.argv[2]

    delete_cmd = "git push origin :" + branch_name
    subprocess.run(delete_cmd.split(" "))

    # print(delete_cmd)
    # print(branch_name)


def rename():
    print("rename branch")
    if len(sys.argv) != 4:
        usage()
        return

    old_name = sys.argv[2]
    new_name = sys.argv[3]

    rename_cmd = "git push origin origin/" + old_name + ":refs/heads/" + new_name + " :" + old_name
    subprocess.run(rename_cmd.split(" "))

    # print(rename_cmd)
    # print(old_name)
    # print(new_name)


def list_branches():
    print("list branches")
    if len(sys.argv) != 3:
        usage()
        return

    userid = sys.argv[2]

    list_user = "git for-each-ref refs/remotes/ --format=%(authoremail)%09%(committerdate:short)%09%(refname:short) --sort=authordate"
    list_all = "git for-each-ref refs/remotes/ --format=%(authoremail)%09%(committerdate:short)%09%(refname:short) --sort=authorname"

    if userid == "all":
        result = subprocess.run(list_all.split(" "), stdout=subprocess.PIPE)
    else:
        result = subprocess.run(list_user.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    result.stdout.decode('utf-8')
    result_str = str(result)

    for line in result_str.split("\\n"):
        if userid == "all":
            branch = line.split("\\t")
            print(*branch, sep='\t\t\t')
        elif "@intuit.com" in userid and userid in line:
            branch = line.split("\\t")
            print(*branch, sep='\t')


def usage():
    print("Usage: python <script-name> [--list <user-mail-id>|--delete <branch-name>|--rename <old-branch-name> <new-branch-name>]")


def main():
    print(sys.argv[0])
    if len(sys.argv) < 3:
        usage()
        exit(0)

    try:
        option = sys.argv[1]
        if "--delete" == option:
            delete()
        elif "--rename" == option:
            rename()
        elif "--list" == option:
            list_branches()
        else:
            print("invalid argument")
    except Exception:
        print("exception caught")


if __name__ == '__main__':
    main()
