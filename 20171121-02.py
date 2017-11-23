import os

cwd = os.getcwd()

for file in os.listdir(cwd):
    if file.endswith(".xlsx"):
        print(os.path.join(cwd, file))

print("\n\n")

for file in os.listdir(cwd):
    if file.startswith("STOCK_"):
        print(os.path.join(cwd, file))

print("\n\n")

for file in os.listdir(cwd):
    if file.startswith("STOCK_") and file.endswith(".xlsx"):
        print(os.path.join(cwd, file))