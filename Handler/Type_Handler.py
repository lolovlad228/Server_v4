import Handler.MainHadler as Hand
import numpy as np
import data_besa.data_mssql as db
import Builder_Command.BuilderCommand as Command #создание команд Command.create_commamd(Type, [])
import DataLog as Data
import json as js
import keras.models
from sklearn.tree import DecisionTreeClassifier
import pickle
from Manager.NetModelManager import Pred


class NewGoods(Hand.AbstractHandler):

    def gen_sort(self, flag):
        if flag == 1:
            list_qr = Command.create_command("SortTask", [[0, 2]])
            return list_qr, 2
        else:
            list_qr = Command.create_command("Loading", "Loading")
            return list_qr, flag

    def update_count(self, id_counte, goods_name):
        data_base = db.db_sql()
        select = db.db_sql.select_db(data_base, "SELECT TOP(1) d.* FROM MapsDay d INNER JOIN Goods g "
                                                "ON d.id_goods = g.id "
                                                "WHERE g.Name = ? and d.fullstr = 0", (goods_name,))
        select_info_neural = db.db_sql.select_db(data_base, "SELECT n.dot_order, "
                                                            "n.isseasons, n.seasons, "
                                                            "n.cell_col, n.orhov, "
                                                            "n.relehes "
                                                            "FROM neural_goods_info n "
                                                            "INNER JOIN Goods g "
                                                            "ON n.id_goods = g.id "
                                                            "Where g.Name = ?", (goods_name,))
        ser = Pred().pre(np.array([[select_info_neural[5], select_info_neural[2], select_info_neural[1],
                                                    select_info_neural[6]]]))
        with open('small_tree.sav', 'rb') as file:
            tree = pickle.load(file)
        trt = tree.predict([[select_info_neural[0], select_info_neural[3], select_info_neural[4], ser[0]]])
        print('12')
        print(ser, trt)
        if trt > 3:
            i = 4
        elif trt == 3:
            i = 5
        else:
            i = 6
        print(select[0], i)
        db.db_sql.update_db(data_base, "UPDATE MapsDay SET idgraf = ? WHERE idgoods = ?", (i, select[0]))

    def handle(self, request):
        robo_list = Data.DataBase()
        if request["Type_command"] == "New_goods":
            state_sort = next(i for i in robo_list.robot if i[0].type_robot == "Sorter")
            print(state_sort[0].state_robot)
            if state_sort[0].state_robot == 1:
                data_base = db.db_sql()
                select_info = db.db_sql.select_db(data_base, "SELECT m.idgraf, m.side, m.district, m.id FROM MapsDay "
                                                             "m INNER JOIN Goods g ON m.idgoods = g.id "
                                                             "WHERE g.Name = ? and m.fullstr = 0", (request["Goods"]))
                db.db_sql.update_db(data_base, "UPDATE MapsDay SET fullstr = ? WHERE id = ?", (1, select_info[3]))
                select_info = list(select_info)
                select_info.insert(0, "Map")
                com = Command.create_command("StandCommand", [
                    [select_info[0], 2, "Input", "None", select_info[3].replace(' ', '')],
                    [select_info[0], select_info[1], "Input_line", select_info[2].replace(' ', ''),
                     select_info[3].replace(' ', '')]
                ])
                Data.DataBase.task_list_robot.append(com)
                command_1, state = self.gen_sort(state_sort)
                robo_list.robot[robo_list.robot.index(state_sort)][0].state_robot = state
                robo_list.task_list_sort.append(command_1)
                robo_list.listupdate()
                return "New_goods"
            else:
                return "None Command"
        else:
            return super(NewGoods, self).handle(request)


class NewTaskSort(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "New_sort_list":
            try:
                info = js.dumps(Data.DataBase.task_list_sort.pop(0)).encode()
                request["sock"].send(info)
            except IndexError:
                request["sock"].send(js.dumps(Command.create_command("CommandNone", [["None", "None"]])).encode())
            return "new_sort_list"
        else:
            return super(NewTaskSort, self).handle(request)


class RefreshState(Hand.AbstractHandler):
    def handle(self, request):
        robo_list = Data.DataBase
        robot = next(i for i in robo_list.robot if i[0].zone == request["District"])
        if request["Type_command"] == "Refresh_state":
            robo_list.robot[robo_list.robot.index(robot)] = request["Task"]
            return "refresh_state"
        else:
            return super(RefreshState, self).handle(request)


class InfoTime(Hand.AbstractHandler):
    def generate_time(self, info, task_now):
        if task_now == info:
            return 1
        else:
            return 0

    def handle(self, request):
        if request["Type_command"] == "Time":
            if request["District"] == "A":
                g = "B"
            else:
                g = "A"
            ts = str(self.generate_time(l.Lists().robot_state[g], request["Task"])).encode()
            request["sock"].send(ts)
            return "time"
        else:
            return super(InfoTime, self).handle(request)


class RefreshFlag(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "Refresh_flag":
            robo_list = Data.DataBase()
            state_sort = next(i for i in robo_list.robot if i[0].type_robot == "Sorter")
            robo_list.robot[robo_list.robot.index(state_sort)] = 1
            command = Command.create_command("SortTask", [[0, 1]])
            robo_list.task_list_sort.append(command)
            robo_list.listupdate()
            return "refresh_flag"
        else:
            return super(RefreshFlag, self).handle(request)


class User(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "Out_goods":
            data_base = db.db_sql()
            select_id = db.db_sql.select_db(data_base, "SELECT id FROM Goods WHERE Name = ? SET ROWCOUNT 1",
                                            (request["Goods"]))
            select = db.db_sql.select_db(data_base, "SELECT idgraf, side, district "
                                                    "FROM MapsDay WHERE idgoods = ? and fullstr=1",
                                         select_id[0])
            db.db_sql.update_db(data_base, "UPDATE TOP(1) MapsDay SET fullstr=0 WHERE idgoods = ? and fullstr=1",
                                (select_id[0]))
            com = Command.create_command("StandCommand", [
                ["Map", select[0], "Output_line", select[1].replace(' ', ''), select[2].replace(' ', '')],
                ["Map", 8, "Output", "None", select[2].replace(' ', '')]
            ])
            Data.DataBase().task_list_robot.append(com)
            Data.DataBase().listupdate()
            return "our_cube"
        else:
            return super(User, self).handle(request)
