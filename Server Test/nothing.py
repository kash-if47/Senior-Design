
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


temp = cur.execute("SELECT * FROM student")
data = cur.fetchall()
for i in range(0, len(data)):
    id = str(data[i][3])
    name = data[i][0] + " " + data[i][1]
    siz = len(name)
    for j in range(0, 20 - siz):
        name = name + " "
    print(name + id)