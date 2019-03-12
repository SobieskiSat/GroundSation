from matplotlib import pyplot as plt

class Predictor:
    def __init__(self):
        self.reader()
    def reader(self):
        print('xa')
        with open('GPS.TXT') as f:
            data = f.readlines()
        self.x=[]
        self.y=[]
        self.h=[]
        for d in data:
            #print(d)
            l=d.split(' ')
            if float(l[0])>50.025 and float(l[0])<50.035 and float(l[1])>19.880 and float(l[1])<19.890 and float(l[2])>200 and float(l[2])<500:
                self.x.append(float(l[0]))
                self.y.append(float(l[1]))
                self.h.append(float(l[2])-202)

    def predict(self, posbx, posby, hb, posex, posey, he):

        hd=he-hb
        factor
        mx=(posex-posbx)/hd
        my=(posey-posby)/hd
        print(posey+my*he)
        print(posex+mx*he)

    def predict_from_data(self, numb, nump, gh):
        bx=self.x[numb]
        by=self.y[numb]
        bh=self.h[numb]-gh
        px=self.x[nump]
        py=self.y[nump]
        ph=self.h[nump]-gh
        self.predict(bx,by, bh, px, py, ph)



    def plot(self):
        plt.plot(self.h)
        plt.show()


p=Predictor()
p.plot()
p.predict_from_data(2180, 2200, 0)

'''
filename = 'data1.txt'
with open(filename) as f:
    data = f.readlines()
x=[]
y=[]
z=[]
for d in data:
    try:
        b=d.split(' ')
        x.append(float(l[3]))
        y.append(float(l[4]))
        z.append(float(l[5]))
    except Exception:
        pass
plt.plot(z)
plt.show()
'''
