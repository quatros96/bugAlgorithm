from os import stat
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

    def getNextRobotMoveToTarget(self) -> type.Dict[str, int]:
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
        if (angle <= 45.0) or (angle > 360.0 - 45.0):
            return {
                'x': 1,
                'y': 0
            }
        elif (angle < 135.0) and (angle > 45.0):
            return {
                'x': 0,
                'y': -1
            }
        elif (angle <= 225.0) and (angle >= 135.0):
            return {
                'x': -1,
                'y': 0
            }
        elif (angle <= 315) and (angle > 225):
            print('cos tu nie gra')
            return {
                'x': 0,
                'y': 1
            }
        else:
            return {
                'x': 0,
                'y': 0
            }

    def canRobotMakeMove(self, sensors: type.List[type.Dict[str, int]]) -> bool:
        # print('pierwsza wsp na tab',
        # self.__robotPosition['y'] + sensors[1]['y'])
        # print('druga wsp na tablicy',
        # self.__robotPosition['x'] + sensors[1]['x'])
        if self.__map[self.__robotPosition['y'] + sensors[1]['y']][self.__robotPosition['x'] + sensors[1]['x']] != 1:
            return True
        else:
            return False

    def obstacleOnRightSensor(self, sensors: type.List[type.Dict[str, int]]) -> bool:
        if self.__map[self.__robotPosition['y'] + sensors[2]['y']][self.__robotPosition['x'] + sensors[2]['x']] == 1:
            return True
        else:
            return False

    def obstacleOnSensor(self, sensors: type.List[type.Dict[str, int]], sensor: str) -> bool:
        index = 0
        if sensor == 'left':
            index = 2
        elif sensor == 'right':
            index = 0
        if self.__map[self.__robotPosition['y'] + sensors[index]['y']][self.    __robotPosition['x'] + sensors[index]['x']] == 1:
            return True
        else:
            return False

    def rotateRobot(self, robotOrientation: type.Dict[str, int], direction: str) -> type.Dict[str, int]:
        if robotOrientation['x'] == 1 and robotOrientation['y'] == 0:
            if direction == 'left':
                return {
                    'x': 0,
                    'y': -1
                }
            else:
                return {
                    'x': 0,
                    'y': 1
                }
        elif robotOrientation['x'] == 0 and robotOrientation['y'] == 1:
            if direction == 'left':
                return {
                    'x': 1,
                    'y': 0
                }
            else:
                return {
                    'x': -1,
                    'y': 0
                }
        elif robotOrientation['x'] == -1 and robotOrientation['y'] == 0:
            if direction == 'left':
                return {
                    'x': 0,
                    'y': 1
                }
            else:
                return {
                    'x': 0,
                    'y': -1
                }
        else:
            if direction == 'left':
                return {
                    'x': -1,
                    'y': 0
                }
            else:
                return {
                    'x': 1,
                    'y': 0
                }

    def getCurrentRobotSensors(self, robotOrientation: type.Dict[str, int]) -> type.List[type.Dict[str, int]]:
        sensorsToCheck: type.List[type.Dict[str, int]] = []
        # left sensor always first
        if robotOrientation['x'] == 0 and robotOrientation['y'] < 0:
            sensorsToCheck.append({'x': -1, 'y': 0})
            sensorsToCheck.append(robotOrientation)
            sensorsToCheck.append({'x': 1, 'y': 0})
        elif robotOrientation['x'] == 0 and robotOrientation['y'] > 0:
            sensorsToCheck.append({'x': 1, 'y': 0})
            sensorsToCheck.append(robotOrientation)
            sensorsToCheck.append({'x': -1, 'y': 0})
        elif robotOrientation['x'] > 0 and robotOrientation['y'] == 0:
            sensorsToCheck.append({'x': 0, 'y': -1})
            sensorsToCheck.append(robotOrientation)
            sensorsToCheck.append({'x': 0, 'y': 1})
        else:
            sensorsToCheck.append({'x': 0, 'y': 1})
            sensorsToCheck.append(robotOrientation)
            sensorsToCheck.append({'x': 0, 'y': -1})
        return sensorsToCheck

    def findRoute(self):
        state: int = 0
        allRobotPositions: type.List[type.Dict[str, int]] = [
            self.__robotPosition]
        robotOrientation: type.Dict[str, int] = self.getNextRobotMoveToTarget()
        sensorsToCheck: type.List[type.Dict[str, int]
                                  ] = self.getCurrentRobotSensors(robotOrientation)
        test: int = 0
        #self.__robotPosition != self.__targetPosition
        while self.__robotPosition != self.__targetPosition:
            test += 1
            if state == 0:
                if self.canRobotMakeMove(sensorsToCheck):
                    print('robot idzie do przodu')
                    self.__robotPosition['x'] += robotOrientation['x']
                    self.__robotPosition['y'] += robotOrientation['y']
                    allRobotPositions.append(self.__robotPosition)
                    robotOrientation = self.getNextRobotMoveToTarget()
                    sensorsToCheck = self.getCurrentRobotSensors(
                        robotOrientation)
                else:
                    print('robot nie moze do przodu')
                    #robotOrientation = self.getNextRobotMoveToTarget()
                    sensorsToCheck = self.getCurrentRobotSensors(
                        robotOrientation)
                    state = 1
            if state == 1:
                print('robot obraca sie w lewo')
                robotOrientation = self.rotateRobot(
                    robotOrientation, self.__direction)
                sensorsToCheck = self.getCurrentRobotSensors(
                    robotOrientation)
                state = 2
            if state == 2:
                if self.canRobotMakeMove(sensorsToCheck) and self.obstacleOnSensor(sensorsToCheck, self.__direction):
                    print('robot moze do przodu i ma przeszkode po prawej')
                    self.__robotPosition['x'] += robotOrientation['x']
                    self.__robotPosition['y'] += robotOrientation['y']
                    allRobotPositions.append(self.__robotPosition)
                elif not self.obstacleOnSensor(sensorsToCheck, self.__direction):
                    print('robot chcial do przodu ale nie ma po prawej przeszkody')
                    state = 3
                elif not self.canRobotMakeMove(sensorsToCheck):
                    state = 1
            if state == 3:
                print('robot skreca w prawo i rusza do przodu')
                if self.__direction == 'left':
                    robotOrientation = self.rotateRobot(
                        robotOrientation, 'right')
                if self.__direction == 'right':
                    print('rotacja w lewo')
                    robotOrientation = self.rotateRobot(
                        robotOrientation, 'left')
                sensorsToCheck = self.getCurrentRobotSensors(
                    robotOrientation)
                self.__robotPosition['x'] += robotOrientation['x']
                self.__robotPosition['y'] += robotOrientation['y']
                allRobotPositions.append(self.__robotPosition)
                state = 0
            print('position', self.__robotPosition)
            print('orientation', robotOrientation)
            print('-------------------')


test = BugZero('right')
test.loadMapFromFile('map3.txt')
print(test.getNextRobotMoveToTarget())
test.findRoute()
