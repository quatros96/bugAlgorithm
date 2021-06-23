import typing as type
import numpy as np


class BugZero:

    def __init__(self, direction='left') -> None:
        pass
        self.__direction: str = direction
        self.__robotPosition: type.Dict[str, int] = {
            'x': -1,
            'y': -1
        }
        self.__targetPosition: type.Dict[str, int] = {
            'x': -1,
            'y': -1
        }
        self.__map: type.List[type.List[int]] = []
        self.__validFields: type.List[int] = [0, 1, 2, 3]

    def loadMapFromFile(self, path):
        try:
            with open(path) as file:
                try:
                    rowLength: int = 0
                    targetFound: bool = False
                    robotFound: bool = False
                    lines: type.List[str] = file.readlines()
                    for index, line in enumerate(lines):
                        fields: type.List[str] = line.split(' ')
                        if index == 0:
                            rowLength = len(fields)
                        elif len(fields) != rowLength:
                            raise Exception('Map is not rectangular')
                        row: type.List[int] = []
                        for field in fields:
                            fieldInt: int = int(field)
                            if(fieldInt not in self.__validFields):
                                raise Exception('Incorrect value')
                            if fieldInt == 2:
                                if robotFound:
                                    raise Exception('Too many roboooots!')
                                robotFound = True
                                self.__robotPosition['x'] = len(row)
                                self.__robotPosition['y'] = index
                            if fieldInt == 3:
                                if targetFound:
                                    raise Exception('Too many targets!')
                                targetFound = True
                                self.__targetPosition['x'] = len(row)
                                self.__targetPosition['y'] = index
                            row.append(fieldInt)
                        self.__map.append(row)
                    if not targetFound or not robotFound:
                        raise Exception('Robot or target not found!')
                except Exception as e:
                    print(e)
                    return
        except EnvironmentError:
            print('File error!')
            return
        print(np.array(self.__map))
        print('Robot pos', self.__robotPosition)
        print('Target pos', self.__targetPosition)

    def findRoute(self):
        pass

    def getNextRobotMove(self) -> type.Dict[str, int]:
        angle: float = 0
        worldVector = [1, 0]
        directionVector = [self.__targetPosition['x'] - self.__robotPosition['x'],
                           self.__targetPosition['y'] - self.__robotPosition['y']]
        unit_vector_1 = worldVector / np.linalg.norm(worldVector)
        unit_vector_2 = directionVector / np.linalg.norm(directionVector)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angleRad = np.arccos(dot_product)
        if directionVector[1] < 0:
            angle = angleRad * (180 / np.pi)
        else:
            angle = 360 - angleRad * (180 / np.pi)
        print(angle)
        if angle <= 22.5 and angle > 360 - 22.5:
            return {
                'x': 1,
                'y': 0
            }
        elif angle <= 22.5 + 45 and angle > 22.5:
            return {
                'x': 1,
                'y': 1
            }
        elif angle <= 22.5 + 90 and angle > 22.5 + 45:
            return {
                'x': 0,
                'y': 1
            }
        elif angle <= 22.5 + 135 and angle > 22.5 + 90:
            return {
                'x': -1,
                'y': 1
            }
        elif angle <= 22.5 + 180 and angle > 22.5 + 135:
            return {
                'x': -1,
                'y': 0
            }
        elif angle <= 22.5 + 225 and angle > 22.5 + 180:
            return {
                'x': -1,
                'y': -1
            }
        elif angle <= 22.5 + 270 and angle > 22.5 + 225:
            return {
                'x': 0,
                'y': -1
            }
        else:
            return {
                'x': 1,
                'y': -1
            }


test = BugZero()
test.loadMapFromFile('map.txt')
print(test.getNextRobotMove())
