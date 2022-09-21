import json
import math
import urllib.request as httplib  # 3.x

def get_json_from_url(url):  # 抓網頁資料 轉json使用
    contents = ""
    req = httplib.Request(url, data=None,
                          headers={
                              'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})
    reponse = httplib.urlopen(req)
    if reponse.code == 200:  # 當連線正常時
        contents = reponse.read().decode("utf-8")  # 轉換編碼為 utf-8
    # 字串 換成  JSON 的 Dict
    return json.loads(contents)

def distence(x1,y1,x2,y2):
    ans = math.sqrt(((x1-x2)*101.75) ** 2 + ((y1-y2)*110.75) ** 2)
    return ans

def parkingLoading():

    # 抓網路資料
    url = "https://motoretag.taichung.gov.tw/DataAPI/api/ParkingSpotListAPI"
    data = get_json_from_url(url)

    # 分類
    parkingData = data
    parkingName = []
    parkingX =[]
    parkingY = []
    parkingTotal = []
    parkingAva = []
    parkingNote = []
    parkingUpadateTime = []
    for a in parkingData:
        for b in a["ParkingLots"]:
            if b["Position"] == None:
                pass
            else:
                parkingName.append(b["Position"])
                # print(b["Position"])

                parkingX.append(b["X"])
                # print("經度:",b["X"])

                parkingY.append(b["Y"])
                # print("緯度:",b["Y"])

                parkingTotal.append(b["TotalCar"])
                # print("總停車數:", b["TotalCar"])

                parkingAva.append(b["AvailableCar"])
                # print("剩餘車位:", b["AvailableCar"])

                parkingNote.append(b["Notes"])
                # print("價格:", b["Notes"])

                parkingUpadateTime.append(b["Updatetime"])


    return parkingName,parkingX,parkingY,parkingTotal,parkingAva,parkingNote,parkingUpadateTime
# parkingName,parkingX,parkingY,parkingTotal,parkingAva,parkingNote,parkingUpadateTime
def parkingSearch(allpark, x=0, y=0 ):
    N = allpark[0].copy()
    X = allpark[1].copy()
    Y = allpark[2].copy()
    T = allpark[3].copy()
    A = allpark[4].copy()
    P = allpark[5].copy()
    U = allpark[6].copy()
    distence_list = []
    for i in range(len(N)):
        distence_list.append(distence(x, y, X[i], Y[i]))
    # 沒有停車位的移除
    t=0
    for i in allpark[4]:
        if int(i) < 0:
            t += 1
            detele_park = A.index(i)
            N.pop(detele_park)
            X.pop(detele_park)
            Y.pop(detele_park)
            T.pop(detele_park)
            A.pop(detele_park)
            P.pop(detele_park)
            U.pop(detele_park)
            distence_list.pop(detele_park)

    if __name__ == '__main__':
        print("長度比對:", len(N), len(X), len(Y), len(T), len(A), len(P), len(U), len(distence_list))
        print("沒有停車位的停車場數量:", t)
        print("原資料　　　:",allpark[4])
        print("測試剩餘車位:",A)
    nearDis = min(distence_list)
    nearNum = distence_list.index(min(distence_list))

    return N[nearNum],X[nearNum],Y[nearNum],T[nearNum],A[nearNum],P[nearNum],U[nearNum],nearDis

if __name__=="__main__":
    while True:
        print("----台中市停車場空位查詢系統----")
        while True:
            print("(輸入e退出系統)")
            t = input("1.請輸入欲查詢的台中市區名(ex:西屯區):")

            if t == "e":
                exit()
            data = parkingLoading()
            parkingName = ""
            Nm = 1
            pt = []
            for i in data[0]:
                if t in i:
                    parkingName += f"({Nm})" + i + ","
                    pt.append(i)
                    Nm += 1
                    if Nm % 5 == 0:
                        parkingName += "\n"
                else:
                    pass
            if pt == []:
                print("輸入名稱錯誤或該區無監管之停車場!")
                parkingName =""
                continue
            else:
                break
        print("本區可查詢之停車場如下:")
        print(parkingName)
        while True:
                t = input("2.請輸入該停車場代號(ex:1):")
                if t =="e":
                    exit()
                    break
                else:
                    pass
                try:
                    int(t)
                except:
                    print("請輸入數字!")
                    continue
                else:
                    if int(t) <= len(pt):
                        break
                    else:
                        print("請輸入有效數字!")
                        continue
        p = data[0].index(pt[int(t) - 1])
        print("-------------")
        print("該停車場資訊如下:")
        # parkingName,parkingX,parkingY,parkingTotal,parkingAva,parkingNote,parkingUpadateTime
        print(f"停車場名稱: {data[0][p]}")
        print(f"停車場座標(經,緯度): ({data[1][p]},{data[2][p]})")
        if int(data[4][p]) <=0:
            data[4][p] ="0"
        print(f"停車場車位情況: 剩餘{data[4][p]}位 (全部有{data[3][p]}位)")
        print(f"停車場收費情形: {data[5][p]}")
        print(f"資料最後更新時間: {data[6][p]}\n\n")


