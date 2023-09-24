import argparse


class Operation:

    def __init__(self):
        self.number = 10
        self.value = 10

    def operation(self):
        f_exercise = open('./Exercise.txt', 'a+', encoding='utf-8')
        f_answer = open('./Answer.txt', 'a+', encoding='utf-8')
        f_exercise.seek(0)
        f_answer.seek(0)
        f_exercise.truncate()
        f_answer.truncate()
        count = 0
        # TODO
        f_exercise.close()
        f_answer.close()


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
        opera = Operation()
        opera.number = int(args.sum)
        opera.value = int(args.range)
        opera.operation()
    elif args.exercise_file and args.answer_file:
        print("-e-a")
    else:
        print("请正确输入参数!")


if __name__ == '__main__':
    main()
