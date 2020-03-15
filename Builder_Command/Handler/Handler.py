import Builder_Command.Handler.Type_Handler as Type


def code(command, list_main):
    command_none = Type.Command_None(list_main)
    standarta_command = Type.Standarte_Command(list_main)
    sort_task = Type.SortTask(list_main)

    command_none.set_next(standarta_command).set_next(sort_task)
    result = command_none.handle(command)
    return result if result else "None createCommand"
