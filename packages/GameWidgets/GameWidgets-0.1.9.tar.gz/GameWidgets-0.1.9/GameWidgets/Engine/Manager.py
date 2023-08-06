import pygame

class Manager:
    def __init__(self, screen, *args):
        self.screen = screen
        self.drawlist = []
        for key in args:
            self.drawlist.append(key)

    def ReturnLayer(self, layer:int):
        return self.drawlist[layer-1]

    def Return(self):
        return self.drawlist

    def DeleteLayer(self, layer:int):
        self.drawlist.pop(layer-1)

    def Drawlayer(self,layer:int):
        try:
            for i in self.drawlist[layer-1]:
                if i[1] != "False":
                    self.screen.blit(i[2],i[3])
        except:
            for i in self.drawlist[layer-1]:
                if i[1] != "False":
                    i[2].Draw()

    def AddLayer(self,item,index:int):
        self.drawlist.insert(index,item)

    def DrawAll(self):
        for i in self.drawlist:
            for thing in i:
                if thing[1]:
                    try:
                        self.screen.blit(thing[2],thing[3])
                    except:
                        thing[2].Draw()