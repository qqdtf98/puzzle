from bangtal import *
from bangtal.singleton import *
from bangtal.game import *
import random

scene1 = Scene("메인","images/main.png")
selectedTheme = ''

# 복수 이미지에 대해 게임 제공
bears = Object("images/b_s.png")
bears.setScale(0.5)
bears.locate(scene1,300,300)
bears.show()

pingu = Object("images/p_s.png")
pingu.setScale(0.5)
pingu.locate(scene1,700,300)
pingu.show()


recordList = []

puzzles = [[1,4,7],[2,5,8],[3,6,9]]
answers = [[1,4,7],[2,5,8],[3,6,9]]

scene2 = Scene("게임","images/main.png")

scene3 = Scene("타임아웃","images/timeout.png")
returnToMain = Object("images/return.png")
returnToMain.locate(scene3,550,200)
returnToMain.show()

returnToMain2 = Object("images/return.png")
returnToMain2.setScale(0.7)
def returnToMain_onMouseAction(x,y,action):
  # 게임 종료 시 타이머 리셋. scene1으로 이동.
  global puzzleTimer
  hideTimer()
  puzzleTimer= Timer(100)
  puzzleTimer.stop()
  scene1.enter()
returnToMain.onMouseAction = returnToMain_onMouseAction
returnToMain2.onMouseAction = returnToMain_onMouseAction

def puzzleTimer_onTimeOut():
  scene3.enter()

puzzleTimer = Timer(100)
puzzleTimer.onTimeout = puzzleTimer_onTimeOut

def setGame():
  shufflePuzzles()
  returnToMain2.locate(scene2,900,400)
  returnToMain2.show()
  showTimer(puzzleTimer)
  scene2.enter()
  # 게임 시작 시 타이머 작동
  puzzleTimer.start()
  for i in range(0,3):
    for j in range(0,3):
      puzzles[i][j] = Puzzle(puzzles[i][j],f"images/{selectedTheme}/{puzzles[i][j]}.png")
      puzzles[i][j].setScale(0.5)
      puzzles[i][j].locate(scene2,700-150*i,500-150*j)
      puzzles[i][j].show()

def shufflePuzzles():
  global puzzles
  puzzles = [[1,4,7],[2,5,8],[3,6,9]]
  for k in range(0,random.randint(40,50)):
    for i in range(0,3):
      for j in range(0,3):
        if(puzzles[i][j] == 9):
          if(random.randint(0,3)== 0 and i+1<3):
            puzzles[i][j] = puzzles[i+1][j]
            puzzles[i+1][j] = 9
          elif(random.randint(0,3)== 1 and j-1>=0):
            puzzles[i][j] = puzzles[i][j-1]
            puzzles[i][j-1] = 9
          elif(random.randint(0,3)== 2 and i-1>=0):
            puzzles[i][j] = puzzles[i-1][j]
            puzzles[i-1][j] = 9
          elif(random.randint(0,3)== 3 and j+1<3):
            puzzles[i][j] = puzzles[i][j+1]
            puzzles[i][j+1] = 9


def bears_onMouseAction(x,y,action):
  global scene2
  global selectedTheme
  selectedTheme = 'bears'
  scene2 = Scene("게임", "images/bears/background.png")
  setGame()
bears.onMouseAction = bears_onMouseAction

def pingu_onMouseAction(x,y,action):
  global scene2
  global selectedTheme
  selectedTheme = 'pingu'
  scene2 = Scene("게임", "images/pingu/background.png")
  setGame()
pingu.onMouseAction = pingu_onMouseAction

# Object 클래스를 상속받는 Puzzle 클래스 정의
class Puzzle(Object):
  def onMouseClick(self,x,y,action):
    blackPos = findBlank(self.num)
    if(blackPos is not None):
      puzzles[blackPos[2]][blackPos[3]].num = self.num
      puzzles[blackPos[0]][blackPos[1]].num = 9
      setImage()

  def __init__(self,num,file):
    id = GameServer.instance().createObject(file)
    ObjectManager.instance().register(id, self)

    self._file = file
    self.ID = id
    self.num = num
    self.onMouseAction = self.onMouseClick

def findBlank(num):
  for i in range(0,3):
    for j in range(0,3):
       if(puzzles[i][j].num is num):
         if(j-1>=0 and puzzles[i][j-1].num is 9):
           return [i,j,i,j-1]
         elif(j+1<3 and puzzles[i][j+1].num is 9):
           return [i,j,i,j+1]
         elif(i-1>=0 and puzzles[i-1][j].num is 9):
           return [i,j,i-1,j]
         elif(i+1<3 and puzzles[i+1][j].num is 9):
           return [i,j,i+1,j]
         else:
           return None

def checkAnswer():
  for i in range(0,3):
    for j in range(0,3):
      if(puzzles[i][j].num != answers[i][j]):
        return None
  return 1

def setImage():
  for i in range(0,3):
    for j in range(0,3):
      puzzles[i][j] = Puzzle(puzzles[i][j].num,f"images/{selectedTheme}/{puzzles[i][j].num}.png")
      puzzles[i][j].setScale(0.5)
      puzzles[i][j].locate(scene2,700-150*i,500-150*j)
      puzzles[i][j].show()
  if(checkAnswer() == 1):
    # 종료 시 걸린 시간 출력
    gameTime = int(puzzleTimer.get())
    showMessage(str(100-gameTime)+'초가 걸렸습니다!!')
    puzzleTimer.stop()
    hideTimer()
    recordList.append(100-gameTime)
    bestRecord = ''
    if(min(recordList) == 100-gameTime):
      # 최고 기록 갱신 시 출력
      bestRecord = '최고 기록입니다!!'
    showMessage(str(100-gameTime)+'초가 걸렸습니다!!\n'+bestRecord)

startGame(scene1)