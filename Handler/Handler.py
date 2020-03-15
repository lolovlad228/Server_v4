import Handler.Type_Handler as Type

New_goods = Type.NewGoods()
New_Task_Sort = Type.NewTaskSort()
Refresh_state = Type.RefreshState()
Info_Time = Type.InfoTime()
Refresh_Flag = Type.RefreshFlag()
User = Type.User()

New_goods.set_next(New_Task_Sort).set_next(Refresh_state).set_next(Info_Time).set_next(Refresh_Flag).set_next(User)


def task(command):
    result = New_goods.handle(command)
    return result if result else "None command"
