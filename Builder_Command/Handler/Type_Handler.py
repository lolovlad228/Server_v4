import Handler.MainHadler as Hand
import Builder_Command.Builder as BuildCom


class Command_None(Hand.AbstractHandler):

    def __init__(self, gen_list):
        self.gen_list = gen_list

    def handle(self, request):
        if request == "CommandNone":
            command = []
            director = BuildCom.Director()
            for i in range(len(self.gen_list)):
                builder = BuildCom.ConcreteBuilder(self.gen_list[i])
                director.builder = builder
                director.none_command()
                command.append({})
                for data in builder.product.list_parts():
                    command[i][data[0]] = data[1]
            return command
        else:
            return super(Command_None, self).handle(request)


class Standarte_Command(Hand.AbstractHandler):
    def __init__(self, gen_list):
        self.gen_list = gen_list

    def handle(self, request):
        if request == "StandCommand":
            command = []
            director = BuildCom.Director()
            for i in range(len(self.gen_list)):
                builder = BuildCom.ConcreteBuilder(self.gen_list[i])
                director.builder = builder
                director.standert_command()
                command.append({})
                for data in builder.product.list_parts():
                    command[i][data[0]] = data[1]
            return command
        else:
            return super(Standarte_Command, self).handle(request)


class SortTask(Hand.AbstractHandler):

    def __init__(self, gen_list):
        self.gen_list = gen_list

    def handle(self, request):
        if request == "SortTask":
            command = []
            director = BuildCom.Director()
            for i in range(len(self.gen_list)):
                builder = BuildCom.ConcreteBuilder(self.gen_list[i])
                director.builder = builder
                director.sort_task()
                command.append({})
                for data in builder.product.list_parts():
                    command[i][data[0]] = data[1]
            return command
        else:
            return super(SortTask, self).handle(request)
