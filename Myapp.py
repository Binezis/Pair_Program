import argparse
import re
from fractions import Fraction
from random import randint


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
        while True:
            try:
                exercise_list, answer = self.combine()
            except ZeroDivisionError:  # 当0位除数 和 负数情况
                continue
            # True表示检查后无重复
            if check(exercise_list, answer, exerciseFile='./Exercise.txt', answerFile='./Answer.txt'):
                f_exercise.write("题目" + str(count + 1) + ": " + ' '.join(exercise_list) + ' =\n')
                if re.search('/', answer):
                    d, n = answer.split('/')
                    if int(d) > int(n):
                        answer = to_fraction(answer)
                f_answer.write("答案" + str(count + 1) + ": " + answer + '\n')
                count += 1
                if count == self.number:
                    break
        f_exercise.close()
        f_answer.close()

    def combine(self):
        # 不超过3个运算符
        nums_operation = randint(1, 3)
        bracket = 0
        n1 = self.is_proper()
        op1 = four_operator()
        n2 = self.is_proper()
        exercise_list = [n1, op1, n2]
        # 两步运算以上
        if nums_operation >= 2:
            op2 = four_operator()
            n3 = self.is_proper()
            exercise_list.append(op2)
            exercise_list.append(n3)
            bracket = randint(0, 2)
            # 三步运算
            if nums_operation == 3:
                op3 = four_operator()
                n4 = self.is_proper()
                exercise_list.append(op3)
                exercise_list.append(n4)
                bracket = randint(0, 4)
        # 插入括号
        if bracket != 0:
            exercise_list = bracket_insert(exercise_list, bracket)
        answer = get_answer(exercise_list, bracket)
        if re.search('-', answer):  # 有负号就报错
            raise ZeroDivisionError("负号")
        return exercise_list, answer

    def is_proper(self):
        # 是否用真分数
        flag_is_rf = randint(0, 1)
        if flag_is_rf == 1:
            n = self.get_proper_fraction()
        else:
            n = str(randint(0, self.value - 1))
        # 返回的是str类型
        return n

    def get_proper_fraction(self):
        denominator = randint(2, self.value)
        numerator = randint(1, denominator - 1)
        random_attach = randint(0, 1)
        real_fraction = str(Fraction(numerator, denominator))
        # 调用fraction方法生成真分数
        if random_attach != 0:
            real_fraction = str(random_attach) + "'" + real_fraction
        return real_fraction


def is_same(orig_list, same_list):
    nums = ''.join(orig_list).split('+|-|*|/|(|)')
    # 运算符个数
    ''.join(orig_list).split('+|-')
    for string in same_list:
        if nums == string:
            return True
        else:
            # 判断数字是否一样
            nums_copy = string.split('+|-|*|/|(|)')
            if len(nums) != len(nums_copy):
                return False
            else:
                for i in nums:
                    if i in nums_copy:
                        continue
                    else:
                        return False
                # 判断运算符个数是否一样
                if (len(orig_list) - len(nums)) != (len(string) - len(nums_copy)):
                    return False
                else:

                    if len(orig_list) == 6 and len(same_list) == 6:
                        if orig_list[0] == string[4] and string[2] == orig_list[2]:
                            if orig_list[0] == same_list[4] and orig_list[2] == same_list[2]:
                                return True
                            else:
                                return False
                        else:
                            return False

                    if len(orig_list) == 6 and len(same_list) == 8:
                        if same_list[0] == '(':
                            if orig_list[1] == same_list[1] or orig_list[1] == same_list[3]:
                                return True

                            else:
                                return False
                    if len(orig_list) == 8 and len(same_list) == 6:
                        if orig_list[0] == '(':
                            if same_list[1] == orig_list[1] or same_list[1] == orig_list[3]:
                                return True

                            else:
                                return False

                    if len(orig_list) == 8 and len(same_list) == 8:
                        return True


def check(orig_list, answer, exerciseFile, answerFile):
    # 读取文件
    exercise_file = open(exerciseFile, "r", encoding='utf-8')
    answer_file = open(answerFile, "r", encoding='utf-8')
    # 定义一个list用来存储具有相同结果的式子
    same_list = []
    # 先判断库中是否有相同的结果
    i = 0
    j = 0
    for aline in answer_file.readlines():
        answer = answer.strip()
        real_answer = aline.split(':')[1]
        real_answer = real_answer.strip()
        if answer == real_answer:
            i += 1
            for eline in exercise_file.readlines():
                j += 1
                if j == i:
                    # 提取出式子
                    eline = eline.split(':')[1]
                    eline = eline.split('=')[0]
                    same_list.append(eline.strip())
                    break
    return not is_same(orig_list, same_list)


def to_fraction(fraction):
    try:
        # 将字符串分割为分子和分母
        numerator, denominator = map(int, fraction.split('/'))
        if denominator == 0:
            return "分母不能为零"
        # 计算整数部分
        whole_part = numerator // denominator
        # 计算真分数部分的分子
        remainder = numerator % denominator
        # 返回带分数的字符串形式
        if remainder == 0:
            return str(whole_part)
        else:
            return f"{whole_part}'{remainder}/{denominator}"
    except ValueError:
        return ValueError


def four_operator():
    operators = ['+', '-', 'x', '÷']
    return operators[randint(0, len(operators) - 1)]


def bracket_insert(exercise_list, bracket):
    if bracket == 1:
        exercise_list.insert(0, '(')
        exercise_list.insert(4, ')')
    if bracket == 2:
        exercise_list.insert(2, '(')
        exercise_list.insert(6, ')')
    if bracket == 3:
        exercise_list.insert(4, '(')
        exercise_list.insert(8, ')')
    if bracket == 4:
        exercise_list.insert(0, '(')
        exercise_list.insert(4, ')')
        exercise_list.insert(6, '(')
        exercise_list.insert(10, ')')
    return exercise_list


def get_answer(exercise_list, bracket):
    num_list = []
    operation_list = []
    no_list = []
    for i in exercise_list:

        if re.match(r"[+\-x÷]", i):
            if i == '÷':
                i = '/'  # 除号转换
            if i == 'x':
                i = '*'  # 乘号转换
            operation_list.append(i)
        elif re.match(r'\d+', i):
            num_list.append(i)
        else:
            pass
    for j in num_list:
        if re.search(r"'", j):
            f1, f2 = j.split("'")
            fraction = Fraction(f1) + Fraction(f2)
            no_list.append(fraction)
        else:
            no_list.append(Fraction(j))
    # 根据括号情况计算出答案
    answer = bracket_answer(bracket, operation_list, no_list)
    return str(answer)


def bracket_answer(bracket, operation_list, no_list):
    if no_list is None:
        return
    format_cal_answer = []
    if bracket == 0:
        if len(operation_list) == 1:
            format_cal_answer = eval("no_list[0] %s no_list[1]" % (operation_list[0]))
        if len(operation_list) == 2:
            format_cal_answer = eval(
                "no_list[0] %s no_list[1] %s no_list[2]" % (operation_list[0], operation_list[1]))
        if len(operation_list) == 3:
            format_cal_answer = eval('no_list[0] %s no_list[1] %s no_list[2] %s no_list[3]' % (
                operation_list[0], operation_list[1], operation_list[2]))
    if bracket == 1:
        if len(operation_list) == 2:
            format_cal_answer = eval(
                "(no_list[0] %s no_list[1]) %s no_list[2]" % (operation_list[0], operation_list[1]))
        if len(operation_list) == 3:
            format_cal_answer = eval('(no_list[0] %s no_list[1]) %s no_list[2] %s no_list[3]' % (
                operation_list[0], operation_list[1], operation_list[2]))
    if bracket == 2:
        if len(operation_list) == 2:
            format_cal_answer = eval(
                "no_list[0] %s (no_list[1] %s no_list[2])" % (operation_list[0], operation_list[1]))
        if len(operation_list) == 3:
            format_cal_answer = eval('no_list[0] %s (no_list[1] %s no_list[2]) %s no_list[3]' % (
                operation_list[0], operation_list[1], operation_list[2]))
    if bracket == 3:
        format_cal_answer = eval('no_list[0] %s no_list[1] %s (no_list[2] %s no_list[3])' % (
            operation_list[0], operation_list[1], operation_list[2]))
    if bracket == 4:
        format_cal_answer = eval('(no_list[0] %s no_list[1]) %s (no_list[2] %s no_list[3])' % (
            operation_list[0], operation_list[1], operation_list[2]))
    return format_cal_answer


def out_grade(exerciseFile, answerFile):
    exercise_file = open(exerciseFile, "r", encoding='utf-8')
    answer_file = open(answerFile, "r", encoding='utf-8')
    # 定义一个flag记录同行的练习和答案
    wrong = []
    correct = []
    line_flag = 0
    # 依次对两个文件里的练习和答案校对
    for e, a in zip(exercise_file.readlines(), answer_file.readlines()):

        line_flag += 1
        a = a.split(':')[1]
        a = a.strip()
        if re.search(r"'", a):
            a_r, a_f = a.split("'")
            real_answer = str(Fraction(a_r) + Fraction(a_f))
        else:
            real_answer = str(Fraction(a))

        e = e.split(': ')[1]
        e = e.split('=')[0]
        operation_list = []
        no_list = []
        bracket = 0
        pattern = re.compile(r"\d+'\d+/\d+|\d+/\d+|\d+")
        num_list = re.findall(pattern, e)

        for i in e:
            if re.match(r'[+\-x÷]', i):
                if i == '÷':
                    i = '/'  # 除号转换
                if i == 'x':
                    i = '*'  # 乘号转换
                operation_list.append(i)
            elif re.match(r'\(', i):
                bracket_before = e.index(i)
                bracket_after = e.find(")", -2, -1)
                if bracket_before == 0 and bracket_after == -1:
                    bracket = 1
                if bracket_before != 0:
                    bracket = 2
                if bracket_before != 0 and bracket_after == (len(e) - 2) and len(num_list) == 4:
                    bracket = 3
                if bracket_before == 0 and bracket_after == (len(e) - 2) and len(num_list) == 4:
                    bracket = 4
            else:
                pass
        for j in num_list:
            if re.search(r"'", j):
                f1, f2 = j.split("'")
                fraction = Fraction(f1) + Fraction(f2)
                no_list.append(fraction)
            else:
                no_list.append(Fraction(j))
        # 分析得出四种情况后，计算答案与answer.txt里的答案校对
        cal_answer = bracket_answer(bracket, operation_list, no_list)
        if Fraction(real_answer) - Fraction(cal_answer) == 0:
            correct.append(str(line_flag))
        else:
            wrong.append(str(line_flag))
    # 处理结果，返回输出
    correct_result = "Correct:" + str(len(correct)) + " " + "(" + ",".join(correct) + ")\n"
    wrong_result = "Wrong:" + str(len(wrong)) + " " + "(" + ",".join(wrong) + ")"
    return correct_result + wrong_result


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
        result = out_grade(args.exercise_file, args.answer_file)
        with open('Grade.txt', 'w+') as f:
            f.write(result)
    else:
        print("请正确输入参数!")


if __name__ == '__main__':
    main()
