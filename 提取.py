# -*- coding: utf-8 -*-
"""
# —*— ProjectName：提取指定站点数据
# —*— Author：李国龙
# —*— CreateTime：2023年2月23日21:23:36
# —*— Vision：1.0.0
# —*— Information:
"""
import csv
import os
import shutil
from tqdm import tqdm

def Extra(input_path, output_path, point_names):
    filelist = os.listdir(input_path)
    date_list = [s[-12:-4] for s in filelist]
    tem_csv = output_path + '/tem.csv'

    # 打开CSV文件并读取列标题
    with open(tem_csv, 'r') as f:
        reader = csv.reader(f)
        # 获取第1行中第2到第16个元素，即2-16列的标题
        headers = next(reader)[1:16]
        f.close()
    # print(filelist)
    print('站点数据：', date_list)
    print('属性变量：', headers)

    # 生成每个站点的输出文件
    for i in range(len(point_names)):
        path = output_path + f'/{point_names[i]}.csv'
        shutil.copy(tem_csv, path)

    # 提取数据
    for o, file in tqdm(enumerate(filelist)):
        file = input_path + '/' + file
        for i, point in enumerate(point_names):
            # 读取新csv文件中已经存在的站点数据
            path = output_path + f'/{point}.csv'
            with open(path, 'r') as f:
                # print(path)
                # 创建CSV读取器
                reader = csv.reader(f)
                # 创建一个空列表
                oldrows = []
                # 迭代CSV文件的每一行，将其作为一个元素添加到列表中
                for row in reader:
                    oldrows.append(row)

            for title in headers:
                # 定义要查找的type列中值为“AOI”的数据行的行号列表
                rows = []
                newdates = []

                # 读取原csv文件
                with open(file, 'r') as f:
                    reader = csv.DictReader(f)
                    # 遍历原csv文件中的所有行
                    for index, row in enumerate(reader):
                        # 如果当前行的type列值为“AOI”，则将该行的行号添加到aoi_rows列表中
                        if row['type'] == title:
                            rows.append(reader.line_num)

                            newdate = str(date_list[o]) + '.' + str(row['hour'])
                            newdates.append(newdate)
                # 定义一个用于保存数据的列表
                data_list = []

                # 读取原csv文件
                with open(file, 'r') as f:
                    reader = csv.DictReader(f)
                    # 遍历原csv文件中的所有行
                    for row in reader:
                        # 如果当前行的行号在aoi_rows列表中，则将该行的“站点”列数据添加到data_list列表中
                        if reader.line_num in rows:
                            try:
                                data_list.append(row[point])
                            except:
                                data_list.append('None')
                # print(file, '***', point, '***', title, ':', data_list)


                for name in headers:
                    if title == name:
                        name = name.replace('.', '_')
                        # 构造要执行的代码
                        code = 'globals()["' + name + '"] = data_list'
                        # 执行代码
                        exec(code)


            # 创建新行
            for j in range(len(newdates)):
                new_row = []
                new_row.append(newdates[j])
                for name in headers:
                    name = name.replace('.', '_')
                    # print(globals()[name][j])
                    new_row.append(globals()[name][j])
                oldrows.append(new_row)


            # 打开CSV文件并写入更新后的数据
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                # print('output newrows', oldrows)
                for row in oldrows:
                    # print('写入新行：', row)
                    writer.writerow(row)
                f.close()

if __name__ == '__main__':
    input_path = 'E:/test/input'
    output_path = 'E:/test/output'
    point_names = ['1462A', '1463A', '1464A', '1465A', '1466A', '1467A', '1468A', '1469A', '1471A', '1472A', '1473A',
                   '1474A', '3524A', '3605A']   # 站点列表
    Extra(input_path, output_path, point_names)
    print("Extra Success")