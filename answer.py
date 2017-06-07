# -*- coding:utf-8 -*-
import termcolor
from conf import session, headers, clear
import re

offset = 0
temp_offset = 0
limit = 5
temp_page = 1
total_page = 0
replies = 0
current_answer_list = []


class Answer:

    def __init__(self):
        pass

    def error(self):
        print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看","red")

    def ignore(self, answer):
        pass

    def thanks(self, answer):
        pass

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               u"**\n" \
               u"**  next:       下一页\n" \
               u"**  prev:       上一页\n" \
               u"**  clear:      清屏\n" \
               u"**  back:       返回上级操作目录\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def show_answers(self, answer_list, cur_page=1):
        global offset, limit, temp_offset, total_page, temp_page
        global current_answer_list
        # 当前 answer，用于分页显示答案
        current_answer_list = answer_list[offset:offset+limit]
        index = 0
        temp_offset = offset
        temp_page = cur_page
        total_page = len(answer_list)/limit if len(answer_list) % limit == 0 else len(answer_list)/limit+1
        total_page = 1 if total_page == 0 else total_page
        print termcolor.colored(u"答案共有 ", "yellow")+ \
            termcolor.colored(u"{total_page}".format(total_page=str(total_page)), "red") + \
            termcolor.colored(u" 页.当前第 ", "yellow") + \
            termcolor.colored("{cur_page}".format(cur_page=str(cur_page)), "red") + \
            termcolor.colored(u" 页.共有 ", 'yellow') + \
            termcolor.colored("{replies}".format(replies=replies), "red") + \
            termcolor.colored(u" 条回答.", "yellow")
        if len(current_answer_list) > 0:
            for answer in current_answer_list:
                id = termcolor.colored(str(index), 'red')
                time = termcolor.colored(answer.time, 'white')
                thanks = termcolor.colored(str(answer.thanks)+u" 人感谢.", 'cyan')
                content = termcolor.colored(answer.content, 'blue') + \
                    termcolor.colored("(" + answer.author + ")", 'green')
                info = '\n'.join([id + '\t\t' + time + '\t\t' + thanks, content]) + '\n'
                index += 1
                print info
        else:
            print termcolor.colored(u"还没有回答.", 'red')

    def next_page(self, answer_list):
        global offset, limit, temp_offset, temp_page, total_page
        if temp_page + 1 <= total_page:
            cur_page = temp_page + 1
            offset = temp_offset + limit
            self.show_answers(answer_list, cur_page)
        else:
            print termcolor.colored(u"已是最后一页.", "red")

    def prev_page(self, answer_list):
        global offset, limit, temp_offset, temp_page, total_page
        if temp_page - 1 >= 1:
            cur_page = temp_page - 1
            offset = temp_offset - limit
            self.show_answers(answer_list, cur_page)
        else:
            print termcolor.colored(u"已是第一页.", "red")

    def operate(self, answer_list, reply):
        global replies
        replies = reply
        self.show_answers(answer_list)
        mode = re.compile(r"^\d+$")
        while True:
            op = raw_input("Answer List$ ")
            if re.match(mode, op.strip()):
                pass
            else:
                if op == "next":
                    self.next_page(answer_list)
                elif op == "prev":
                    self.prev_page(answer_list)
                elif op == "help":
                    self.help()
                elif op == "back":
                    break
                elif op == "clear":
                    clear()
                else:
                    self.error()

