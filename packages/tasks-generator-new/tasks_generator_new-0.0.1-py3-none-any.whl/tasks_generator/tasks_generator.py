import random
import fractions
import math







# Задача № 10991
def random_logarythm():

    base_of_loogarythm = random.randint(2, 15)
    answer = random.randint(0, 4)
    degree_of_logarythm = base_of_loogarythm**answer
    a = math.log(degree_of_logarythm, base_of_loogarythm)
    task = f'Вычислите: \(log_'"{" + str(base_of_loogarythm)+'}{'+str(degree_of_logarythm)+'}\)'
    return answer, task





#Задача 14526
def random_logarythm_stepen():

    base_of_loogarythm = random.randint(2, 15)
    answer = random.randint(0, 4)
    degree_of_logarythm = base_of_loogarythm**answer
    n = random.randint(1, 5)
    if n < 2:
        a = int(n**math.log(degree_of_logarythm, base_of_loogarythm))
        task = f'Вычислите: \(log_'"{" + str(base_of_loogarythm)+'}{'+str(degree_of_logarythm)+'}\)'
    else:
        a = int(n ** math.log(degree_of_logarythm, base_of_loogarythm))
        task = f'Вычислите: \({n}^'"{"'log_'"{" + str(base_of_loogarythm) + '}{' + str(degree_of_logarythm) + '}}\)'
    return a, task



#Задачи 14526, 14567, 10991
def random_logarythm_stepen_umnojenie():
    base_of_loogarythm = random.randint(2, 6)
    answer = random.randint(0, 4)
    degree_of_logarythm = base_of_loogarythm ** answer
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    if n < 2 and m < 2:
        a = int(n ** (m * math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите: \(log_'"{" + str(base_of_loogarythm) + '}{' + str(degree_of_logarythm) + '}\)'
    elif n >= 2 and m >= 2:
        a = int(n ** (m * math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'{m}*log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n < 2 and m >= 2:
        a = int(n ** (m * math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'{m}*log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n >= 2 and m < 2:
        a = int(n ** (m * math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'

    return a, task





# Задание № 14591
def random_logarythm_stepen_slojenie():
    base_of_loogarythm = random.randint(2, 6)
    answer = random.randint(0, 4)
    degree_of_logarythm = base_of_loogarythm ** answer
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    if n < 2 and m < 2:
        a = int(n ** (m + math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите: \(log_'"{" + str(base_of_loogarythm) + '}{' + str(degree_of_logarythm) + '}\)'
    elif n >= 2 and m >= 2:
        a = int(n ** (m + math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'{m}+log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n < 2 and m >= 2:
        a = int(n ** (m + math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'{m}+log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n >= 2 and m < 2:
        a = int(n ** (m + math.log(degree_of_logarythm, base_of_loogarythm)))
        task = f'Вычислите:' f'\({n}^'"{"f'log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'

    return a, task




# Задание № 14592
def random_logarythm_stepen_minus():
    base_of_loogarythm = random.randint(2, 6)
    answer = random.randint(0, 4)
    degree_of_logarythm = base_of_loogarythm ** answer
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    if n < 2 and m < 2:
        a = format(n ** (m - math.log(degree_of_logarythm, base_of_loogarythm)), '.4')
        task = f'Вычислите: \(log_'"{" + str(base_of_loogarythm) + '}{' + str(degree_of_logarythm) + '}\)'
    elif n >= 2 and m >= 2:
        a = format(n ** (m - math.log(degree_of_logarythm, base_of_loogarythm)), '.4')
        task = f'Вычислите:' f'\({n}^'"{"f'{m}-log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n < 2 and m >= 2:
        a = format(n ** (m - math.log(degree_of_logarythm, base_of_loogarythm)), '.4')
        task = f'Вычислите:' f'\({n}^'"{"f'{m}-log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'
    elif n >= 2 and m < 2:
        a = format(n ** (m - math.log(degree_of_logarythm, base_of_loogarythm)), '.4')
        task = f'Вычислите:' f'\({n}^'"{"f'log_'"{" + str(base_of_loogarythm) + '}{' \
               + str(degree_of_logarythm) + '}}\)'

    return a, task





#Задача № 12242

def random_logarythm_with_fractions():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    if even_or_odd % 2 == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        a = int(math.log(fraction, 2))
        task = f'Вычислите: \(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) + '}\)'
    else:
        fraction = fractions.Fraction(1, even_or_odd)
        a = int(math.log(fraction, 3))
        task = f'Вычислите: \(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + '}\)'
    return a, task




def random_logarythm_with_fractions_with_stepen():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    if even_or_odd % 2 == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b*(-1)
        a = format(pow(n, 1 / x), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) + '}\)'
    else:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b*(-1)
            a = format(pow(n, 1 / x), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + '}\)'

    return a, task





def random_logarythm_with_fractions_with_stepen_decrement_figure():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    p = random.randint(0, 4)
    if even_or_odd % 2 == 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x)-p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) +"})}{-" f"{p}"'}'
    elif even_or_odd % 2 != 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b*(-1)
            a = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + "})}{-" f"{p}"'}'
    elif even_or_odd % 2 == 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x)-p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            2) + '}\)'
    elif even_or_odd % 2 != 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            3) + '}\)'
    return a, task





def random_logarythm_with_fractions_with_stepen_increment_figure():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    p = random.randint(0, 4)
    if even_or_odd % 2 == 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) +"})}{+" f"{p}"'}'
    elif even_or_odd % 2 != 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + "})}{+" f"{p}"'}'
    elif even_or_odd % 2 == 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            2) + '}\)'
    elif even_or_odd % 2 != 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            a = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \{n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            3) + '}\)'
    return a, task








# № Задача 14069

def sum_logarytms():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(k*math.log(degree_of_logarythm2, base_of_loogarythm2) + m*math.log(degree_of_logarythm1, base_of_loogarythm1))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'

    return a, task







def sum_logarytms_stepen():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(n**(k*math.log(degree_of_logarythm2, base_of_loogarythm2) + m*math.log(degree_of_logarythm1, base_of_loogarythm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) +\
           '}\)' "+" f'{m}*\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'{m}*\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "+" f'\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'


    return a, task


# 14540, 14599
def sum_logarytms_sum_stepen():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    l = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(n**(k*math.log(degree_of_logarythm2, base_of_loogarythm2)) + l**((m*math.log(degree_of_logarythm1, base_of_loogarythm1))))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) +\
           '}\)}' "+" f'{l}^'"{"f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "+" f'{l}^'"{"f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "+" f'{l}^'"{"f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "+" f'{l}^'"{"f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'


    return a, task







# Задачи 14510, 14515
def decrement_logarytms():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    n = random.randint(1, 3)

    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(math.log(degree_of_logarythm2, base_of_loogarythm2) - n*math.log(degree_of_logarythm1, base_of_loogarythm1))
    if n > 1:
        task = f'Вычислите разницу логарифмов:\(log_'"{" + str(base_of_loogarythm2) +\
                         '}{' + str(degree_of_logarythm2) + '}\)' "-" f'{n}*\(log_'"{" + str(base_of_loogarythm1) + \
                         '}{' + str(degree_of_logarythm1) + '}\)'
    else:
        task = f'Вычислите разницу логарифмов:\(log_'"{" + str(base_of_loogarythm2) + '}{' + str(
            degree_of_logarythm2) + '}\)' "-" f'\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(
            degree_of_logarythm1) + '}\)'

    return a, task


# 14510

def decrement_logarytms_new():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(k*math.log(degree_of_logarythm2, base_of_loogarythm2) - m*math.log(degree_of_logarythm1, base_of_loogarythm1))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})'

    return a, task



# 14601, № 14604
def decrement_logarytms_stepen():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    n = random.randint(1, 4)
    m = random.randint(1, 4)
    k = random.randint(1, 4)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(n**(k*math.log(degree_of_logarythm2, base_of_loogarythm2) - m*math.log(degree_of_logarythm1, base_of_loogarythm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) +\
           '}\)' "-" f'{m}*\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'{m}*\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)' "-" f'\(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'


    return a, task


# № 14537

def decrement_logarytms_in_stepen():
    base_of_loogarythm1 = random.randint(2, 10)
    answer_of_loogarythm1 = random.randint(0, 4)
    degree_of_logarythm1 = base_of_loogarythm1**answer_of_loogarythm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    o = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    a = int(n**(k*math.log(degree_of_logarythm2, base_of_loogarythm2)) - o**(m*math.log(degree_of_logarythm1, base_of_loogarythm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) +\
           '}\)}' "-" f'{o}^'"{"f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'

    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "-" f'{o}^'"{"f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'

    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "-" f'{o}^'"{"f'{m}*(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\{n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}\)}' "-" f'{o}^'"{"f'(log_'"{" + str(base_of_loogarythm1) + '}{' + str(degree_of_logarythm1) + '})}'


    return a, task





stack_of_functions = [random_logarythm_with_fractions_with_stepen_increment_figure(),
                      random_logarythm_with_fractions_with_stepen_decrement_figure(),
                      random_logarythm(), random_logarythm_with_fractions(), random_logarythm_with_fractions_with_stepen(),
                      random_logarythm_stepen_slojenie(), random_logarythm_stepen(), random_logarythm_stepen_umnojenie(),
                      random_logarythm_stepen_minus(), sum_logarytms_stepen(), sum_logarytms(), decrement_logarytms_stepen(),
                      decrement_logarytms(), decrement_logarytms_new(), sum_logarytms_sum_stepen()]





def tasks_generator():
    a = random.choice(stack_of_functions)
    return a




if __name__ == "__main__":
    ...