#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Excel操作
"""
import os
import random
import string
import datetime
import xlwt
import xlrd
from xlrd import XL_CELL_NUMBER


class Excel(object):
    """
    Excel文件操作
    """
    def __init__(self, callback=None, date_format="%Y-%m-%d"):
        """
        初始化, 临时文件夹
        """
        self.home = "/tmp"
        self.callback = callback
        self.date_format = date_format
        self.depth = 0

    def load_by_cont(self, file_cont, sheet_index=0):
        """
        根据文件内容进行解析
        :param str file_cont: 文件内容
        :param int sheet_index: Sheet索引号
        :return data:[{
            "titile": "值"
        }, ... ]
        """
        title, data = [], []
        work_book = xlrd.open_workbook(file_contents=file_cont)
        sheet = work_book.sheet_by_index(sheet_index)
        for i in xrange(sheet.ncols):
            title.append(sheet.cell(0, i).value)
        for i in xrange(1, sheet.nrows):
            unit = {}
            for j in xrange(sheet.ncols):
                if sheet.cell(i, j).ctype == XL_CELL_NUMBER:
                    unit[title[j]] = "%f" % sheet.cell(i, j).value
                else:
                    unit[title[j]] = sheet.cell(i, j).value
            data.append(unit)
        return data

    def generate(self, title_list, data_list):
        """
        生成Excel
        :param list title_list: [
            {
                "name": 标题,
                "field": 数据中的字段值,
                "sub_list": [
                    {
                        "title": 标题,
                        "field": 数据中的字段值,
                        "sub_list": ...
                    },
                ],
            }
        ]
        :param list data_list: [
            {
                field1: value1,
                field2: {
                    field1: value1,
                    ...
                },
                ...
            }
        ]
        """
        work_book = xlwt.Workbook("UTF-8")
        sheet = work_book.add_sheet("sheet", True)

        # 获取总深度
        self.depth = self.get_title_depth(title_list)

        # 填充每个title的层级
        self.fill_title_level(title_list)

        # 生成标题
        title_style = self.get_title_style()
        col_ptr = 0
        for idx, title in enumerate(title_list):
            col_ptr += self.write_title(sheet, title, 0, col_ptr, title_style)

        # 写入数据
        text_style = self.get_text_style()
        for idx, data in enumerate(data_list):
            self.write_data(sheet, title_list, data, self.depth + idx, 0,
                            text_style)

        filename = self.tmp_filename()
        work_book.save(filename)
        content = ""
        with open(filename, "rb") as fpr:
            content = fpr.read()
        os.remove(filename)
        return content

    def get_title_depth(self, title_list):
        """
        获取title的深度
        """
        def inner_func(title):
            sub_list = title.get("sub_list", [])
            if sub_list:
                tmp = 0
                for i in sub_list:
                    tmp = max(inner_func(i), tmp)
                return 1 + tmp
            else:
                return 1
        self.depth = 0
        for i in title_list:
            self.depth = max(inner_func(i), self.depth)
        return self.depth

    def fill_title_level(self, title_list):
        """
        填充每个title的层级
        """
        def inner_func(title, level):
            title["level"] = level
            for i in title.get("sub_list", []):
                inner_func(i, level + 1)

        for i in title_list:
            inner_func(i, 0)

    def get_title_row_num(self, title):
        """
        获取title的行跨度
        """
        if title.get("sub_list", []):
            return 1
        else:
            return self.depth - title["level"]

    def get_title_column_num(self, title):
        """
        获取title的行跨度
        """
        sub_list = title.get("sub_list", [])
        if not sub_list:
            return 1
        row_num = 0
        for i in sub_list:
            row_num += self.get_title_column_num(i)
        return row_num

    def write_title(self, sheet, title, row_idx, colum_idx, style):
        """
        写title
        """
        # 当前title应该占用几行
        row_num = self.get_title_row_num(title)

        # 当前title应该占用几列
        col_num = self.get_title_column_num(title)

        # 写入单元格
        for i in range(row_num):
            for j in range(col_num):
                sheet.col(colum_idx + j).width = int(3333 * 1)
                sheet.write(row_idx + i, colum_idx + j, "", style)
        sheet.write(row_idx, colum_idx, title["name"], style)

        # 合并
        for i in range(row_num):
            span = col_num - 1
            if span <= 0:
                continue
            sheet.merge(row_idx, row_idx, colum_idx, colum_idx + span)

        for i in range(col_num):
            span = row_num - 1
            if span <= 0:
                continue
            sheet.merge(row_idx, row_idx + span, colum_idx, colum_idx)

        # 递归写入子Title
        sub_list = title.get("sub_list", [])
        if not sub_list:
            all_row_num = 1
        else:
            all_row_num = 0
            for i in title.get("sub_list", []):
                all_row_num += self.write_title(sheet, i, row_idx + 1,
                                                colum_idx + all_row_num, style)
        return all_row_num

    def write_data(self, sheet, title_list, data, row_idx, col_idx, style):
        """
        写title
        :return: 当前的列号
        """
        col_num = 0
        for title in title_list:
            value = data[title["field"]]
            sub_list = title.get("sub_list", [])
            if sub_list and not isinstance(value, dict):
                raise ValueError("title:%s value error" % title["name"])
            if not sub_list:
                val = self.callback(value) if self.callback else value
                if isinstance(val, datetime.datetime):
                    val = val.strftime(self.date_format)
                sheet.write(row_idx, col_idx + col_num, val, style)
                col_num += 1
            else:
                col_num += self.write_data(sheet, sub_list, value,
                                           row_idx, col_idx + col_num, style)
        return col_num

    def tmp_filename(self):
        """
        临时文件名
        :return: 返回临时文件名
        """
        fname = "".join(random.sample(string.lowercase, 10))
        return os.path.join(self.home, fname)

    def get_title_style(self):
        """
        获取title的Style
        """
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment
        return style

    def get_text_style(self):
        """
        获取text的Style
        """
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment
        return style

if __name__ == "__main__":
    exel = Excel()
    TILE_LIST = [
        {
            "name": "班组名称", "field": "team_name",
        },
        {
            "name": "负责人", "field": "principal",
        },
        {
            "name": "总收入", "field": "income_info",
            "sub_list": [
                {"name": "饭票", "field": "fanpiao"},
                {
                    "name": "现金", "field": "cash_info",
                    "sub_list": [
                        {"name": "美元", "field": "dollar"},
                        {"name": "人民币", "field": "rmb"},
                    ]},
            ]
        },
        {
            "name": "总费用", "field": "fee_info",
            "sub_list": [
                {"name": "水费", "field": "water"},
                {"name": "电费", "field": "elec"},
            ]
        }
    ]
    # title的总深度
    assert exel.get_title_depth(TILE_LIST) == 3

    # 填充层级
    exel.fill_title_level(TILE_LIST)

    # 指定title的行跨度
    assert exel.get_title_row_num(TILE_LIST[0]) == 3
    assert exel.get_title_row_num(TILE_LIST[2]) == 1
    assert exel.get_title_column_num(TILE_LIST[0]) == 1
    assert exel.get_title_column_num(TILE_LIST[2]) == 3

    DATA_LIST = [
        {
            "team_name": "西北小吃",
            "principal": "张三",
            "income_info": {
                "fanpiao": 1000,
                "cash_info": {"rmb": 1000, "dollar": 1000},
            },
            "fee_info": {"water": 1000, "elec": 1000}
        },
        {
            "team_name": "麻辣烫",
            "principal": "李四",
            "income_info": {
                "fanpiao": 2000,
                "cash_info": {"rmb": 2000, "dollar": 2000},
            },
            "fee_info": {"water": 2000, "elec": 2000}
        },
        {
            "team_name": "老家肉饼",
            "principal": "王五",
            "income_info": {
                "fanpiao": 3000,
                "cash_info": {"rmb": 3000, "dollar": 3000},
            },
            "fee_info": {"water": 3000, "elec": 3000}
        }
    ]

    FP = open("test.xls", "wb")
    FP.write(exel.generate(TILE_LIST, DATA_LIST))
    FP.close()

