import cv2
import random
import math
from PIL import Image


class Script:
    def __init__(self):
        self.arr_classify = []
        self.arr_points = []

        self.classes_file = cv2.imread(r"venv/pictures/classes.png")
        self.rgb_file = cv2.imread(r"venv/pictures/rgb.png")

        self.width_rgb, self.height_rgb, _ = self.rgb_file.shape

        self.thresh = cv2.threshold(self.classes_file, 127, 255, cv2.THRESH_BINARY)[1] #zapewnia obraz czarno-biały

        N = 100
        M = 701

        self.classify()
        self.cut(N, M)

    def cut(self, n, m):
        im = Image.open(r"venv/pictures/rgb.png")

        if n > self.width_rgb*self.height_rgb:
            raise ValueError("Liczba N przekracza rozmiar obrazu")                  # zapobiega utworzeniu ilości wycięć większej niż ilość pixeli w obrazie

        self.random_fun(n)

        s = 0

        for z in range(n):
            box_new = (self.arr_points[z][0] - math.floor(m / 2), self.arr_points[z][1] - math.floor(m / 2),
                       self.arr_points[z][0] + math.floor(m / 2), self.arr_points[z][1] + math.floor(m / 2))    #uciety obraz jest pixel mniejszy, niz zaklada zadanie, przy wartosci nieparzystej M
                                                                                                                #nie bedzie srodka kwadratu MxM
            crop_img = im.crop(box_new)

            if self.arr_classify[self.arr_points[z][0]][self.arr_points[z][1]] == 1:
                s += 1

            crop_img.save(r"venv/pictures/" + str(z) + "new.png")

        print("S", s / n)           #liczba nigdy nie będzie większa od 1

    def random_fun(self, n):        #Tworzy "macierz" dwuwymiarową posiadającą unikatowe wartości dla koordynatów pixeli
        i = 0

        while i < n:
            x = random.randint(0, self.width_rgb - 1)
            y = random.randint(0, self.height_rgb - 1)

            if not self.arr_points:
                self.arr_points.append([x, y])
                i += 1
            else:
                if [x, y] not in self.arr_points:
                    self.arr_points.append([x, y])
                    i += 1

    def classify(self):                                 #klasyfikuje pixele, bialy - 1, czarny - 0
        height, width, _ = self.classes_file.shape

        for x in range(height):
            self.arr_classify.append([])
            for y in range(width):
                k = self.thresh[x, y]
                if all(k == [255, 255, 255]):            #sprawdza czy kolor pixela jest biały
                    self.arr_classify[x].append(1)
                else:
                    self.arr_classify[x].append(0)


if __name__ == '__main__':
    start = Script()

