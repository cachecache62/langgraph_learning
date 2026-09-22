# 04_nodes/05_str_demo.py

# 通过 f-string 动态生成（运行时才确定值）
str1 = "hello world"
name = "world"
str2 = f"hello {name}"

print("\n--- 比较 str1 和 str2 (f-string 动态生成) ---")
print(f"str1: {id(str1)}")
print(f"str2: {id(str2)}")
print(f"内容相同 (==): {str1 == str2}")  # True  字面量
print(f"地址相同 (is): {str1 is str2}")  # False