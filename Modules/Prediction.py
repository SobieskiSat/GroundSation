from matplotlib import pyplot as plt
class Predictor:
    def __init__(self):
        pass


    def predict(self, data_in, height):
        data=[]
        for i in range(0, len(data_in[0])):
            temp=[]
            temp.append(data_in[0][i])
            temp.append(data_in[1][i])
            temp.append(data_in[2][i])
            data.append(temp)
        x=[]
        y=[]
        h=[]
        #print(data)
        for d in data:
            if float(d[0])>49.025 and float(d[0])<51.035 and float(d[1])>18.880 and float(d[1])<22.890 and float(d[2])>0 and float(d[2])<5000:
                x.append(float(d[0]))
                y.append(float(d[1]))
                h.append(float(d[2])-height)

        count_len = int(len(x)/5)#first and last 1/5 of data
        #print(len(x))
        for t in [x, y, h]: #average of all axis
            counter=0
            for d in t[count_len:]:
                counter+=d
            t[0]=counter/count_len
            counter=0
            for d in t[-count_len:]:
                counter+=d
            t[-1]=counter/count_len

        dh=h[0]-h[-1]#delta h
        dx=x[0]-x[-1]
        dy=y[0]-y[-1]

        dx=dx/dh#x per one meter altitude
        dy=dy/dh

        new_x=dx*h[-1]
        new_y=dy*h[-1]

        return {'x':new_x, 'y':new_y, 'r':h[-1]/7}









class PredictorO:
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

'''
p=Predictor()
p.plot()
p.predict_from_data(2180, 2200, 0)
'''
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
