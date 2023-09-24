import argparse


def add_parm():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-n", dest="sum", help="生成数量")
    argument_parser.add_argument("-r", dest="range", help="生成范围")
    argument_parser.add_argument("-e", dest="exercise_file", help="题目文件")
    argument_parser.add_argument("-a", dest="answer_file", help="答案文件")
    args = argument_parser.parse_args()
    return args


def main():
    args = add_parm()
    # 支持操作：-n-r输入 或 -e-a输入 两种情况。
    if args.range and args.sum:
        print("-n-r")
    elif args.exercise_file and args.answer_file:
        print("-e-a")
    else:
        print("请正确输入参数!")


if __name__ == '__main__':
    main()
