class Model:
    def __init__(self):
        self.username = None
        self.password = None
    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

class QtbaleView:
    def __init__(self):
        self.model = Model()

    def setModel(self, model):
        self.model = model
    def getModel(self):
        return self.model

    def printModel(self):
        print('当前',self.model)
        print(self.model.username, self.model.password)


model = Model()
model.setUsername('admin')
model.setPassword('123456')

view = QtbaleView()
view.setModel(model)
view.printModel()

print(vars(model).items())

