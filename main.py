class BigNumber:
    def __init__(self, number):
        self.number = number
        if number[0] == '-':
            self.sign = -1
        else:
            self.sign = 1

    def __str__(self):
        return self.number

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self == other:
            return False

        if self.sign == -1 and other.sign == 1:
            return True
        if self.sign == 1 and other.sign == -1:
            return False

        if self.sign == -1 and other.sign == -1:
            return BigNumber(other.number[1:]) < BigNumber(self.number[1:])

        x1 = self.number
        x2 = other.number
        n1 = len(x1)
        n2 = len(x2)
        if n1 < n2:
            return True
        elif n1 > n2:
            return False

        for i in range(n1):
            digit1 = int(x1[i])
            digit2 = int(x2[i])
            if digit1 < digit2:
                return True
            elif digit1 > digit2:
                return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __add__(self, other):
        if (self.sign == other.sign):
            x1 = self.number
            x2 = other.number
            if self.sign == -1:
                x1 = x1[1:]

            if other.sign == -1:
                x2 = x2[1:]
            n1 = len(x1)
            n2 = len(x2)
            x1 = "0" * (n2 - n1) + x1
            x2 = "0" * (n1 - n2) + x2
            carry = 0
            res = ""
            n = len(x1)
            for i in range(n):
                digit1 = int(x1[n - i - 1])
                digit2 = int(x2[n - i - 1])
                sumOfDigits = digit1 + digit2 + carry
                if sumOfDigits > 9:
                    carry = 1
                else:
                    carry = 0
                res = str(sumOfDigits % 10) + res
            if carry == 1:
                res = "1" + res
            if (self.sign == -1):
                res = "-" + res
            return BigNumber(res)
        else:
            if self.number == "0":
                return BigNumber(other.number)
            elif other.number == "0":
                return BigNumber(self.number)
            else:
                if self.sign == 1:
                    return self - BigNumber(other.number[1:])
                else:
                    return other - BigNumber(self.number[1:])

    def __sub__(self, other):
        if (self.sign == -1 and other.sign == -1):
            return BigNumber(other.number[1:]) - BigNumber(self.number[1:])
        if self.sign == -1:
            return self + BigNumber("-" + other.number)
        if other.sign == -1:
            return self + BigNumber(other.number[1:])

        x1 = self.number
        x2 = other.number
        n1 = len(x1)
        n2 = len(x2)
        swapped = False

        if self < other:
            x1, x2 = x2, x1
            n1, n2 = n2, n1
            swapped = True
        x2 = "0" * (n1 - n2) + x2
        res = ""
        carry = 0
        n = len(x1)
        for i in range(n):
            digit1 = int(x1[n - i - 1]) - carry
            digit2 = int(x2[n - i - 1])
            carry = 0
            if digit1 < digit2:
                carry = 1
                digit1 += 10
            diff = digit1 - digit2
            res = str(diff) + res

        while (res[0] == "0" and len(res) > 1):
            res = res[1:]
        if swapped:
            res = "-" + res
        return BigNumber(res)

    def __mul__(self, other):
        if (self.number == "0") or (other.number == "0"):
            return BigNumber("0")
        toAddMinus = self.sign != other.sign
        x1 = self.number
        x2 = other.number
        if (self.sign == -1):
            x1 = x1[1:]
        if (other.sign == -1):
            x2 = x2[1:]
        n1 = len(x1)
        n2 = len(x2)

        res = BigNumber("0")
        for i in range(n1):
            carry = 0
            temp = ""
            for j in range(n2):
                digit1 = int(x1[n1 - i - 1])
                digit2 = int(x2[n2 - j - 1])
                product = digit1 * digit2 + carry
                temp = str(product % 10) + temp
                carry = product // 10
            if carry:
                temp = str(carry) + temp
            temp = temp + "0" * i
            res = res + BigNumber(temp)
        if toAddMinus:
            res = BigNumber("-" + res.number)
        return res

    def divideBy(self, divisor):
        if divisor == 0:
            return None
        otherSign = -1 if divisor < 0 else 1
        toAddMinus = self.sign != otherSign
        x = self.number
        if (self.sign == -1):
            x = x[1:]
        divisor = abs(divisor)
        index = 0
        res = ""
        temp = int(x[index])

        while (temp < divisor and index < len(x) - 1):
            index += 1
            temp = temp * 10 + int(x[index])

        while (index < len(x)):
            res += str(temp // divisor)
            temp = temp % divisor
            index += 1
            if index < len(x):
                temp = temp * 10 + int(x[index])

        if len(res) == 0:
            res = "0"
        return BigNumber(res)

    def moduleOf(self, divisor):
        return self - self.divideBy(divisor) * BigNumber(str(divisor))

    def __power(self, other):
        pass

    def __pow__(self, other):
        if other.number == "0":
            return BigNumber("1")
        else:
            if (other.moduleOf(2).number == "1"):
                return self * (self ** (other - BigNumber("1")))
            else:
                result = self ** (other.divideBy(2))
                return result * result
        return res


def test1():
    n1 = BigNumber("1234567890")
    n2 = BigNumber("234658276879432343")
    print(n1 * n2, int(n1.number) * int(n2.number), sep='\n')


def test2():
    for i in range(-100, 100):
        for j in range(-100, 100):
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = BigNumber(str(j))
            if (num1 + num2).number != str(i + j):
                print(i, j, "   Correct result: ", i + j, "      Got: ", num1 + num2)


def test3():
    for i in range(-100, 100):
        for j in range(-100, 100):
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = BigNumber(str(j))
            if (num1 - num2).number != str(i - j):
                print(i, j, "   Correct result: ", i - j, "      Got: ", num1 - num2)


def test4():
    for i in range(-100, 100):
        for j in range(-100, 100):
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = BigNumber(str(j))
            if (num1 * num2).number != str(i * j):
                print(i, j, "   Correct result: ", i * j, "      Got: ", num1 * num2)


def test5():
    for i in range(1, 100):
        for j in range(1, 100):
            if (j == 0):
                continue
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = j
            if num1.divideBy(num2).number != str(i // j):
                print(i, j, "   Correct result: ", i // j, "      Got: ", num1.divideBy(num2))


def test6():
    for i in range(1, 100):
        for j in range(1, 100):
            if (j == 0):
                continue
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = j
            if num1.moduleOf(num2).number != str(i % j):
                print(i, j, "   Correct result: ", i % j, "      Got: ", num1.moduleOf(num2))


def test7():
    for i in range(1, 10):
        for j in range(0, 10):
            # print(i, j)
            num1 = BigNumber(str(i))
            num2 = BigNumber(str(j))
            # print(num1, num2, num1 ** num2)
            if (num1 ** num2).number != str(i ** j):
                print(i, j, "   Correct result: ", i ** j, "      Got: ", num1 ** num2)


test1()
test2()
test3()
test4()
test5()
test6()
test7()








