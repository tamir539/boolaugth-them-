import pygame
import time
import threading
import pygame as pg

class screen:
    def __init__(self, com,msg_q):
        '''
        create the pygame screen
        '''
        pygame.init()
        self.com = com
        self.q = msg_q

        self.white = (255, 255, 255)
        # assigning values to X and Y variable
        self.X = 1540
        self.Y = 800

        self.display_surface = pygame.display.set_mode((self.X, self.Y))
        self.display_surface.fill(self.white)
        self.username = ''
        self.getLogin('dog.jpg')


    def printAnswers(self, quest):


        blue = (0, 0, 128)
        green = (0, 255, 0)

        font = pg.font.Font(None, 50)

        waiting = font.render('waiting for all the players to answer', True, green, blue)
        waitingRect = waiting.get_rect()
        waitingRect.center = (self.X // 2, 500)

        self.display_surface.blit(waiting, waitingRect)

        pygame.display.update()

        while self.q.empty():
            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    # deactivates the pygame library
                    pygame.quit()

                    # quit the program.
                    exit()

        choose = font.render('Choose the answer that funny you the most', True, green, blue)
        chooseRect = choose.get_rect()
        chooseRect.center = (self.X // 2 , 100)

        question = font.render(f'The question was: {quest}', True, green, blue)
        questionRect = question.get_rect()
        questionRect.center = (self.X // 2 , 200)

        txt = self.q.get()
        answers = []

        image = pygame.image.load('dog.jpg')
        txt = txt.split(',')
        hefresh =  400 // len(txt)

        self.display_surface.blit(image, (0, 0))
        self.display_surface.blit(choose, chooseRect)
        self.display_surface.blit(question, questionRect)
        x = self.X // 2
        y = 300
        for t in txt:
            text = font.render(t, True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (x,y)
            answers.append((textRect, t))
            self.display_surface.blit(text, (x, y))
            y += hefresh

        pygame.display.update()
        while self.com.running:

            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    # deactivates the pygame library
                    pygame.quit()

                    # quit the program.
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for rect,t in answers:
                        if rect.collidepoint(event.pos):
                            print('text --->>>>', t)

        exit()


    def displayImg(self, route):
        '''

        :param route: route to picture
        :return: display the picture
        '''
        pygame.display.set_caption('Image')

        # create a surface object, image is drawn on it.
        image = pygame.image.load(route)
        # infinite loop

        t_end = time.time() + 5

        while True:

            # copying the image surface object
            # to the display surface object at
            # (0, 0) coordinate.
            self.display_surface.blit(image, (0 ,0))

            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    # deactivates the pygame library
                    pygame.quit()

                    # quit the program.
                    quit()

                # Draws the surface object to the screen.
            pygame.display.update()

    def write(self, text, x, y):

        blue = (0, 0, 128)
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 32)

        # create a text suface object,
        # on which text is drawn on it.
        text = font.render(text, True,  blue)

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = (x, y)



        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        self.display_surface.blit(text, textRect)
        pygame.display.update()
        time.sleep(2)

    def question(self):
        quest = self.q.get()
        print(quest)

        blue = (0, 0, 128)
        green = (0, 255, 0)

        image = pygame.image.load('dog.jpg')

        font = pg.font.Font(None, 32)

        answer_ord = font.render('you have 5 seconds to Answer the question: ', True, green, blue)
        answer_ordRect = answer_ord.get_rect()
        answer_ordRect.center = (self.X // 2, 100)

        time_left = font.render('0', True, green, blue)
        time_leftRect = time_left.get_rect()
        time_leftRect.center = (self.X // 2, 400)

        question = font.render(quest, True, green, blue)
        questionRect = question.get_rect()
        questionRect.center = (self.X // 2, 250)

        input_box = pg.Rect(700, 320, 200, 32)

        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        color = color_inactive
        active = False

        ans = ''

        self.display_surface.blit(image, (0, 0))
        self.display_surface.blit(answer_ord, answer_ordRect)
        self.display_surface.blit(question, questionRect)

        start_time = time.time()
        sec = str(start_time % 60).split(".")[0]

        pygame.display.update()
        while self.com.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pygame.quit()
                    exit()
                    done = True

                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # If the user clicked on the input_box rect.
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            print(ans)
                            self.com.sendEnc('2'+ans)
                            # self.display_surface.blit(image, (0, 0))
                            # self.display_surface.blit(answer_ord, answer_ordRect)
                            # self.display_surface.blit(question, questionRect)
                            # self.display_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

                            # Blit the input_box rect.
                            # pg.draw.rect(self.display_surface, color, input_box, 2)
                            # pygame.display.update()
                            self.printAnswers(quest)
                            # return text1+","+text2
                        elif event.key == pg.K_BACKSPACE:
                            ans = ans[:-1]
                        else:
                            ans += event.unicode

            # self.display_surface.fill((30, 30, 30))

            # Render the current text.
            txt_surface = font.render(ans, True, color)

            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width


            self.display_surface.blit(image, (0, 0))
            self.display_surface.blit(answer_ord, answer_ordRect)
            self.display_surface.blit(question, questionRect)
            self.display_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            # Blit the input_box rect.
            pg.draw.rect(self.display_surface, color, input_box, 2)

            pg.display.flip()

            if ((time.time() - start_time) % 60) != int(sec):
                sec = str((time.time() - start_time) % 60).split(".")[0]
                time_left = font.render(sec, True, green, blue)
                time_leftRect = time_left.get_rect()
                time_leftRect.center = (self.X // 2, 400)
                self.display_surface.blit(time_left, time_leftRect)

            if time.time() - start_time > 30:
                self.com.sendEnc('2 ')
                self.printAnswers(quest)
                #move to choose answers
                #the time over

            pygame.display.update()

    def lobby(self):
        names = []

        mode = 'laugh'
        is_raedy = False
        blue = (0, 0, 128)
        green = (0, 255, 0)

        x = self.X//2 - 300
        y = 150
        font = pygame.font.Font('freesansbold.ttf', 32)

        waiting = font.render('WAITING FOR AT LEAST 2 PLAYERS... ', True, green, blue)
        waitingRect = waiting.get_rect()
        waitingRect.center = (self.X // 2 - 300, 700)

        loby = font.render('LLOBY', True,  green, blue)
        lobyRect = loby.get_rect()
        lobyRect.center = (self.X // 2, 100)

        gameMode = font.render('CHOOSE GAME MODE:', True,  green, blue)
        gameModeRect = loby.get_rect()
        gameModeRect.center = (self.X // 2 + 300, 150)

        bullshit = font.render('BOOLSHIT!', True,  blue)
        bullshitRect = loby.get_rect()
        bullshitRect.center = (self.X // 2 + 400, 275)

        laugh = font.render('LAUGH!', True, green, blue)
        laughRect = loby.get_rect()
        laughRect.center = (self.X // 2 + 400, 200)

        players = font.render('PLAYERS:', True, green, blue)
        playersRect = loby.get_rect()
        playersRect.center = (self.X // 2 - 400, 150)

        image = pygame.image.load('dog.jpg')
        text = font.render(self.username, True,  blue)

        ready = font.render('READY!', True, blue)

        textRect = text.get_rect()
        readyRect = ready.get_rect()

        readyRect.center = (self.X -200, self.Y - 100)

        # set the center of the rectangular object.
        textRect.center = (x, y)

        # create a text suface object,
        # on which text is drawn on it.

        self.display_surface.blit(image, (0, 0))
        self.display_surface.blit(ready, readyRect)
        self.display_surface.blit(loby, lobyRect)
        self.display_surface.blit(players, playersRect)
        self.display_surface.blit(gameMode, gameModeRect)
        self.display_surface.blit(bullshit, bullshitRect)
        self.display_surface.blit(laugh, laughRect)
        self.display_surface.blit(waiting, waitingRect)
        while self.com.running:
            if not self.q.empty():
                msg = self.q.get()
                print(msg)
                if msg == '':
                    pygame.quit()
                    print('bye')
                    break
                if msg == 'start':
                    print('start!!!!')
                    self.question()
                else:
                    if msg[0] == '!':
                        if msg[1:] in names:
                            names.remove(msg[1:])
                    #print to the screen all the names that joined
                    else:
                        n = msg
                        print(n)
                        y += 50
                        text = font.render(n, True, blue)
                        textRect = text.get_rect()
                        # set the center of the rectangular object.
                        textRect.center = (x, y)
                        self.display_surface.blit(text, textRect)
                        pygame.display.update()
                        names.append(n)
                        print(names)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pygame.quit()
                    print('bye')
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if readyRect.collidepoint(event.pos):
                        if not is_raedy:
                            is_raedy = True
                            print('ready')
                            # Toggle the active variable.
                            self.com.sendEnc(f'1ready,{mode}')
                            ready = font.render('UNREADY', True, blue)
                            readyRect = ready.get_rect()
                            readyRect.center = (self.X - 200, self.Y - 100)
                            self.display_surface.blit(ready, readyRect)
                        else:
                            is_raedy = False
                            print('unready!')
                            self.com.sendEnc('1unready, none')
                            ready = font.render('Ready!', True, blue)
                            readyRect = ready.get_rect()
                            readyRect.center = (self.X - 200, self.Y - 100)
                    elif laughRect.collidepoint(event.pos):
                        if mode == 'bullshit':
                            laugh = font.render('LAUGH!', True, green, blue)
                            laughRect = loby.get_rect()
                            laughRect.center = (self.X // 2 + 400, 200)
                            bullshit = font.render('BOOLSHIT!', True, blue)
                            bullshitRect = loby.get_rect()
                            bullshitRect.center = (self.X // 2 + 400, 275)
                            mode = 'laugh'
                    elif bullshitRect.collidepoint(event.pos):
                        if mode == 'laugh':
                            bullshit = font.render('BOOLSHIT!', True, green, blue)
                            bullshitRect = loby.get_rect()
                            bullshitRect.center = (self.X // 2 + 400, 275)
                            laugh = font.render('LAUGH!', True, blue)
                            laughRect = loby.get_rect()
                            laughRect.center = (self.X // 2 + 400, 200)
                            mode = 'bullshit'


            self.display_surface.blit(image, (0, 0))
            self.display_surface.blit(ready, readyRect)
            self.display_surface.blit(loby, lobyRect)
            self.display_surface.blit(players, playersRect)
            self.display_surface.blit(gameMode, gameModeRect)
            self.display_surface.blit(bullshit, bullshitRect)
            self.display_surface.blit(laugh, laughRect)

            if len(names) < 2:
                self.display_surface.blit(waiting, waitingRect)
            n = names[0]
            text = font.render(n, True, blue)
            textRect = text.get_rect()
            # set the center of the rectangular object.
            textRect.center = (x, y)
            y = 150
            for n in names:
                y += 50
                text = font.render(n, True, blue)
                textRect = text.get_rect()
                # set the center of the rectangular object.
                textRect.center = (x, y)
                self.display_surface.blit(text, textRect)



            pygame.display.update()
        exit()

    def getLogin(self, route):
        green = (0, 255, 0)
        blue = (0, 0, 128)

        font = pg.font.Font(None, 32)

        # create a text suface object,
        # on which text is drawn on it.
        username = font.render('username: ', True, green, blue)
        usernameRect = username.get_rect()
        usernameRect.center = (630, 335)

        passWord = font.render('password: ', True, green, blue)
        passwordRect = passWord.get_rect()
        passwordRect.center = (630, 465)


        image = pygame.image.load(route)
        screen = self.display_surface

        input_box1 = pg.Rect(700, 320, 140, 32)
        input_box2 = pg.Rect(700, 450, 140, 32)

        color_inactive1 = pg.Color('lightskyblue3')
        color_active1 = pg.Color('dodgerblue2')

        color_inactive2 = pg.Color('lightskyblue3')
        color_active2 = pg.Color('dodgerblue2')

        color1 = color_inactive1
        color2 = color_inactive2

        active1 = False
        active2 = False

        text1 = ''
        text2 = ''

        done = False
        self.display_surface.blit(image, (0, 0))

        self.display_surface.blit(username, usernameRect)
        self.display_surface.blit(passWord, passwordRect)

        pygame.display.update()
        while self.com.running:

            if not self.q.empty():
                msg = self.q.get()
                print("in loggin ->>>>>", msg)
                if msg == "ok":
                    self.write('you logged in!',self.X//2, self.Y//2)
                    self.username = text1
                    self.lobby()
                elif msg == 'no':
                    self.write('enter other username',self.X//2, self.Y//2)
                elif msg == 'os':
                    self.write('game has already started :(', self.X//2, self.Y//2)
                    pygame.quit()
                    exit()
                    done = True

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pygame.quit()
                    exit()
                    done = True

                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box1.collidepoint(event.pos):
                        # Toggle the active variable.
                        active1 = not active1
                    else:
                        active1 = False
                    # If the user clicked on the input_box rect.
                    if input_box2.collidepoint(event.pos):
                        # Toggle the active variable.
                        active2 = not active2
                    else:
                        active2 = False
                    # Change the current color of the input box.
                    color1 = color_active1 if active1 else color_inactive1
                    color2 = color_active2 if active2 else color_inactive2
                if event.type == pg.KEYDOWN:
                    if active1:
                        if event.key == pg.K_RETURN:
                            self.com.sendEnc(text1 + "," + text2)
                            #return text1+","+text2
                        elif event.key == pg.K_BACKSPACE:
                            text1 = text1[:-1]
                        else:
                            text1 += event.unicode
                    if active2:
                        if event.key == pg.K_RETURN:
                            self.com.sendEnc(text1+","+text2)
                        elif event.key == pg.K_BACKSPACE:
                            text2 = text2[:-1]
                        else:
                            text2 += event.unicode
            try:

                screen.fill((30, 30, 30))
                # Render the current text.
                txt_surface = font.render(text1, True, color1)
                txt_surface2 = font.render(text2, True, color2)

                # Resize the box if the text is too long.
                width = max(200, txt_surface.get_width() + 10)
                input_box1.w = width

                width = max(200, txt_surface.get_width() + 10)
                input_box2.w = width

                # Blit the text.
                self.display_surface.blit(image, (0, 0))

                self.display_surface.blit(username, usernameRect)
                self.display_surface.blit(passWord, passwordRect)
                screen.blit(txt_surface, (input_box1.x + 5, input_box1.y + 5))
                screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))

                # Blit the input_box rect.
                pg.draw.rect(screen, color1, input_box1, 2)
                pg.draw.rect(screen, color2, input_box2, 2)

                pg.display.flip()

                pygame.display.update()
            except Exception as e:
                pass

        # operate start_game

if __name__ == '__main__':
    scr = screen()
    while True:
        data = scr.getLogin('dog.jpg')
        if data.split(',')[0] == 'hey':
            scr.write('enter a valid login details!')


