
import pymysql

def connectDB():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='rfid1234', db='rfid')
    # cur = conn.cursor()
    return conn

conn = connectDB()
cur = conn.cursor()

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

result = []
result.append("hello")
print(result)