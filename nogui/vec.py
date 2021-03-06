from typing import Union, overload

class Vec2:
    __object__ = [0, 0]

    @overload
    def __init__(self, obj: Union[list, tuple, int, float] = ...) -> None: ...
    def __init__(self, number1: Union[int, float] = ..., number2: Union[int, float] = ...) -> None: self._init([number1, number2])

    def _init(self, obj: object = ...) -> None:

        if obj == [..., ...]:
            obj = (0, 0)
        if obj[1] == ...:
            obj = obj[0]
            if obj.__class__ == int or obj.__class__ == float:
                obj = (obj, obj)
        if obj.__class__ == tuple:
            obj = list(obj)


        self.__object__ = obj

    def __repr__(self) -> str:
        return f"Vec2{tuple(self.__object__)}"
    
    def __math_func__(self, obj1: object, sign: str):
        out = []
        if obj1.__class__ == int or obj1.__class__ == float:
            for i in range(len(self.__object__)):
                if sign == "+": out.append((self.__object__[i] + obj1))
                elif sign == "-": out.append((self.__object__[i] - obj1))
                elif sign == "/": out.append((self.__object__[i] / obj1))
                elif sign == "*": out.append((self.__object__[i] * obj1))
                elif sign == "**": out.append((self.__object__[i] ** obj1))
                elif sign == "//": out.append((self.__object__[i] // obj1))
                elif sign == "%": out.append((self.__object__[i] % obj1))
            return self.__class__(out)

        elif obj1.__class__ == list or obj1.__class__ == tuple or obj1.__class__ == self.__class__:
            for i in range(len(self.__object__)):
                if sign == "+": out.append(self.__object__[i] + obj1[i])
                elif sign == "-": out.append(self.__object__[i] - obj1[i])
                elif sign == "/": out.append(self.__object__[i] / obj1[i])
                elif sign == "*": out.append(self.__object__[i] * obj1[i])
                elif sign == "**": out.append(self.__object__[i] ** obj1[i])
                elif sign == "//": out.append(self.__object__[i] // obj1[i])
                elif sign == "%": out.append(self.__object__[i] % obj1[i])
            return self.__class__(out)
        
        else: raise TypeError

    def __add__(self, obj: object): return self.__math_func__(obj, "+")
    def __sub__(self, obj: object): return self.__math_func__(obj, "-")
    def __mul__(self, obj: object): return self.__math_func__(obj, "*")
    def __rmul__(self, obj: object): return self.__math_func__(obj, "*")
    def __truediv__(self, obj: object): return self.__math_func__(obj, "/")
    def __pow__(self, obj: object): return self.__math_func__(obj, "**")
    def __floordiv__(self, obj: object): return self.__math_func__(obj, "//")
    def __mod__(self, obj: object): return self.__math_func__(obj, "%")
    def __neg__(self):
        for i in range(len(self.__object__)): self.__object__[i] *= -1
        return self.__class__(self.__object__)

    def __contains__(self, obj: Union[int, float]): return obj in self.__object__
    def __getitem__(self, index: int): return self.__object__[index]
    def __setitem__(self, index: int, obj: Union[int, float]): self.__object__[index] = obj

    def __comparison__(self, obj1: object, sign: str):
        out = []
        if obj1.__class__ == int or obj1.__class__ == float:
            for i in range(len(self.__object__)):
                if sign == ">": out.append((self.__object__[i] < obj1))
                elif sign == "<": out.append((self.__object__[i] > obj1))
                elif sign == "<=": out.append((self.__object__[i] >= obj1))
                elif sign == ">=": out.append((self.__object__[i] <= obj1))
                elif sign == "==": out.append((self.__object__[i] == obj1))
                elif sign == "!=": out.append((self.__object__[i] != obj1))
            return self.__class__(out)

        elif obj1.__class__ == list or obj1.__class__ == tuple or obj1.__class__ == self.__class__:
            for i in range(len(self.__object__)):
                if sign == ">": out.append(self.__object__[i] < obj1[i])
                elif sign == "<": out.append(self.__object__[i] > obj1[i])
                elif sign == "<=": out.append(self.__object__[i] >= obj1[i])
                elif sign == ">=": out.append(self.__object__[i] <= obj1[i])
                elif sign == "==": out.append(self.__object__[i] == obj1[i])
                elif sign == "!=": out.append(self.__object__[i] != obj1[i])
            return self.__class__(out)
        
        else: return False

    def __eq__(self, obj: object): return self.__comparison__(obj, "==")
    def __ne__(self, obj: object): return self.__comparison__(obj, "!=")
    def __lt__(self, obj: object): return self.__comparison__(obj, ">")
    def __gt__(self, obj: object): return self.__comparison__(obj, "<")
    def __le__(self, obj: object): return self.__comparison__(obj, ">=")
    def __ge__(self, obj: object): return self.__comparison__(obj, "<=")

    def index(self, number: Union[int, float]): return self.__object__.index(number)
    def __len__(self): return len(self.__object__)
    def __round__(self):
        for i in range(len(self.__object__)):
            self.__object__[i] = round(self.__object__[i])
        return self.__object__

    def __hash__(self) -> int: return id(self)

# print(min(Vec2(5, 10) >= 0) > 0)