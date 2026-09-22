# 04_nodes/04_intern_demo.py

import sys

# 使用 intern 优化
str1 = sys.intern("hello" + " world")
str2 = sys.intern("hello" + " world")

print(str1 == str2)       # True  - 内容相同
print(str1 is str2)       # True  - 是同一个对象（内存地址相同）
print(id(str1))           # 2584161877936
print(id(str2))           # 2584161877936 （相同的ID）


# 直接赋值常量字符串，Python 编译器会自动优化（常量折叠）
str3 = "hello world"
str4 = "hello world"
print(str3 == str4)       # True  - 内容相同
print(str3 is str4)       # True  - 是同一个对象
print(id(str3))           # 例如: 2584161877936
print(id(str4))           # 例如: 2584161877936 (与上面相同)