import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pymysql

def connectDB():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='rfid1234', db='rfid')
    # cur = conn.cursor()
    return conn

conn = connectDB()
cur = conn.cursor()
cur.execute("SELECT * FROM LOG" )
dataMain = cur.fetchall()
# username = "kashif.iqbal@mavs.uta.edu"
# inpassword = "1234"
#
# username2 = "austin.hastings@mavs.uta.edu"
# # temp = cur.execute("SELECT Password FROM ADMIN WHERE Email = %s", username)
#
# def loginCheck(username, inpassword):
#     temp = cur.execute("Select * FROM staff WHERE Email = %s", username)
#     if temp == 0:
#         print("Invalid Username")
#     else:
#         check = cur.fetchone()
#         password = check[3]
#         isAdmin = check[5]
#         if(password == inpassword):
#             if (isAdmin == 1):
#                 print("Show Admin Page")
#             elif (isAdmin == 0):
#                 print("Show Staff Page")
#         else:
#             print("Show Incorrect Password message!")
#
#
# loginCheck(username, inpassword)
# loginCheck(username2, inpassword)
# loginCheck(username2, "hey")
# loginCheck("hey hey", "hey")


# temp = cur.execute("SELECT * FROM staff")
# data2 = cur.fetchall()
# print(data2)
#
# for i in range(0, len(data2)):
#     fName = data2[i][0]
#     lName = data2[i][1]
#     email = data2[i][2]
#     password = data2[i][3]
#     staffId = data2[i][4]
#     isAdmin = data2[i][5]
#
# self.StudentText_GName.show()
# self.StudentText_Grade.show()
# self.StudentText_ID.show()
# self.StudentText_Name.show()
# self.StudentText_Picture.show()
# self.StudentText_RFID.show()

# result = []
# result.append("hello")
# print(result)



data = {'Student ID': [], 'Staff ID': [], 'Date': [], 'Time': []}
for i in range(0, len(dataMain)):
    data['Student ID'].append(str(dataMain[i][0]))
    data['Staff ID'].append(str(dataMain[i][1]))
    data['Date'].append(str(dataMain[i][2]))
    data['Time'].append(str(dataMain[i][3]))



def main(args):

    app = QApplication(args)
    table = QTableWidget(len(dataMain),4)
    horHeaders = []
    for n, key in enumerate(sorted(data.keys())):
        horHeaders.append(key)
        for m, item in enumerate(data[key]):
            newitem = QTableWidgetItem(item)
            table.setItem(m, n, newitem)
    table.setHorizontalHeaderLabels(horHeaders)
    table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)