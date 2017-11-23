import os

print("目前工作目錄:")
cwd = os.getcwd()
print(cwd)

mv_file = "STOCK_CHIP_ANA_20171120.xlsx"
tar_file = cwd + "\\" + mv_file
des_file = cwd + "\\des_dir\\" + mv_file
print("移動檔案:" + tar_file + "-->" + des_file)

try:
	os.rename(tar_file, des_file)
	print("移動檔案完畢.")
except Exception as e:
	print("移動檔案失敗.")
	print(e.args)

print("End of prog.")