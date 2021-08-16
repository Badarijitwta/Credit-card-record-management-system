import time
class credit:
    def __init__(self, pli=[], sli=[]):
        con = ''
        self.plist = pli
        self.slist = sli
        pi = open("Pindex.csv", "r")
        si = open("Sindex.csv", "r")
        '''line = pi.readline()
        while line:
            con = ''
            a = line.split(",")
            con = con + str(a[0]) + "," + str(a[1])
            if (a[0][0] != "*"):
                self.plist.append(con)
            line = pi.readline()

        self.plist.sort()
        pi.close()

        line = si.readline()
        while line:
            con = ''
            a = line.split(",")
            con = con + str(a[0]) + "," + str(a[1])
            #print(con)
            self.slist.append(con)
            line = si.readline()

        self.slist.sort()
        si.close()
        #print(self.plist)
        #print(self.slist)'''

    def getstu(self):
        self.issuing = input("Issuing Bank: ")
        self.cnumber = input("Card Number: ")
        self.name = input("Card Holders Name: ")
        self.cvv = input("CVV/CVV2: ")
        self.issue = input("Issue Date: ")
        self.expiry = input("Expiry Date: ")
        self.billing = input("Billing Date: ")
        self.pin = input("Card Pin: ")

    def pack(self):
        self.getstu()
        st = ""
        st = st + self.issuing + "," + self.cnumber + "," + self.name + ","+ self.cvv + "," + self.issue + "," + self.expiry + "," + self.billing + "," + self.pin + "," + '\n'
        fi = open("record.csv", "a")

        pos = fi.tell()
        pfile = open("Pindex.csv", "a")
        con = self.cnumber + "," + str(pos) + "," + '\n'
        pfile.write(con)
        pfile.close()

        char = ''
        char = char + self.cnumber + "," + str(pos)
        self.plist.append(char)
        self.plist.sort()
        print("------Primary Index----------")
        print(self.plist)

        sfile = open("Sindex.csv", "a")
        con = self.name + "," + self.cnumber + "," + '\n'
        sfile.write(con)
        sfile.close()

        char = ''
        char = char + self.name + "," + self.cnumber
        self.slist.append(char)
        self.slist.sort()
        print("------Secondary Index----------")
        print(self.slist)

        fi.write(st)
        fi.close()

    def indexing(self):
        fi = open("record.csv", "r")
        line = fi.readline()
        a = line.split(",")
        while line:
            if (a[0][0] != "*"):
                pos=fi.tell()
                x=(pos,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7])         
                line = fi.readline()
                a = line.split(",")

                pfile = open("Pindex.csv", "a")
                con = x[2] + "," + str(x[0]) + "," + '\n'
                pfile.write(con)
                pfile.close()
                

                char = ''
                char = char + x[2] + "," + str(x[0])
                self.plist.append(char)
                self.plist.sort()

                sfile = open("Sindex.csv", "a")
                vvv = x[3] + "," + x[2] + "," + '\n'
                sfile.write(vvv)
                sfile.close()

                char = ''
                char = char + x[3] + "," + x[2]
                self.slist.append(char)
                self.slist.sort()
        fi.close()

    def dispstudata(self, pk, flagsk):
        flagpk = self.binarysearchpk(pk)

        if (flagpk == -1):
            print("Not There In The Primary Index")
        else:
            lin = self.plist[flagpk]
            a = lin.split(",")
            pos = a[1]
            fi = open("record.csv", "r+")
            fi.seek(int(pos))
            line = fi.readline()
            b = line.split(",")
            print("Issuing Bank:", b[0])
            print("Card Number: ", b[1])
            print("Card Holders Name:", b[2])
            print("CVV/CVV2:", b[3])
            print("Issue Date: ", b[4])
            print("Expiry Date: ", b[5])
            print("Billing Date: ", b[6])
            print("Card Pin: ", b[7])
            fi.close()
            self.deletesk(b[1], flagsk)

    def deletesk(self, usntd, flagsk):
        print("Do You Want to Delete This Credit Card Record?(yes/no): ")
        n = input()
        if (n != "no"):
            self.deletepk(usntd)
            print("Pimary Index Maintainance Done!")
            self.updateSListandSFile(flagsk)

    def updateSListandSFile(self, flagsk):
        del self.slist[flagsk]
        self.slist.sort()
        print("")

        fi = open("Sindex.csv", "w")
        for rec in self.slist:
            fi.write(rec + "\n")
        fi.close()
        print("Secondary Index is Updated Successfully!")

    def searchsk(self, namets):
        flag = self.binarysearchsk(namets)
        if (flag == -1):
            print("Not There In The Secondary Index")
        else:
            lin = self.slist[flag]
            a = lin.split(",")
            pk = a[1]
            self.dispstudata(pk, flag)
            self.checkduplicates(flag, namets)

    def checkduplicates(self, flag, namets):
        lis = []
        r = len(self.slist)
        for i in range(0, r):
            a = self.slist[i].split(",")
            lis.append(a[0])
        if (flag != 0):
            for i in range(flag - 1, -1, -1):
                if (lis[i] == namets):
                    lin = self.slist[i]
                    a = lin.split(",")
                    pk = a[1]
                    self.dispstudata(pk, i)
                else:
                    break

        if (flag != len(self.slist) - 1):
            for i in range(flag + 1, r):
                if (lis[i] == namets):
                    lin = self.slist[i]
                    a = lin.split(",")
                    pk = a[1]
                    self.dispstudata(pk, i)
                else:
                    break

    def searchpk(self, usnts):
        flag = self.binarysearchpk(str(usnts))
        if (flag == -1):
            print("Not There In The Record File")
        else:
            lin = self.plist[flag]
            a = lin.split(",")
            pos = a[1]
            fi = open("record.csv", "r+")
            fi.seek(int(pos))
            line = fi.readline()
            b = line.split(",")
            print("Issuing Bank:", b[0])
            print("Card Number: ", b[1])
            print("Card Holders Name: ", b[2])
            print("CVV/CVV2: ", b[3])
            print("Issue Date: ", b[4])
            print("Expiry Date ", b[5])
            print("Billing Date:", b[6])
            print("Card Pin: ", b[7])
            fi.close()


    def binarysearchsk(self, namets):
        lis = []
        l = 0
        r = len(self.slist)
        try:
            for i in range(0, r):
                a = self.slist[i].split(",")
                lis.append(a[0])

            while (l <= r):
                m = (l + r) // 2
                if (namets == lis[m]):
                    return m
                if (lis[m] < namets):
                    l = m + 1
                else:
                    r = m - 1
            return -1
        except:
            return -1

    def binarysearchpk(self, usnts):
        lis = []
        l = 0
        r = len(self.plist)
        print(r)
        try:
            for i in range(0, r):
                a = self.plist[i].split(",")
                lis.append(a[0])

            while (l <= r):
                m = (l + r) // 2
                if (usnts == lis[m]):
                    return m
                if (lis[m] < usnts):
                    l = m + 1
                else:
                    r = m - 1
            return -1
        except:
            return -1

    def deletepk(self, usntd):
        flag = self.binarysearchpk(usntd)
        if (flag == -1):
            print("Not There In The Record File")
        else:
            line = self.plist[flag]
            a = line.split(",")
            pos = int(a[1])

            file = open("record.csv", "r+")
            file.seek(int(pos))
            file.write("*")
            file.close()

            self.maintainPIndex(usntd)

            del self.plist[flag]
            self.plist.sort()
            print("Both the Index Lists Updated Successfully!\n")

    def maintainPIndex(self, usntd):
        fi = open('Pindex.csv', "r+")
        pos = fi.tell()
        line = fi.readline()

        a = line.split(",")
        while line:
            usn = a[0]
            if usn == usntd:
                fi.seek(pos)
                fi.write('*')
                print("Primay Index File Updated Successfully!\n")
                fi.close()
                break
            else:
                pos = fi.tell()
                line = fi.readline()
                a = line.split(",")
        fi.close()

    def maintainSIndex(self, usntd):
        lis = []
        r = len(self.slist)
        for i in range(0, r):
            a = self.slist[i].split(",")
            lis.append(a[1])
        for i in range(0, r):
            if (lis[i] == usntd):
                self.updateSListandSFile(i)


s = credit()
print('--------------------------------------------------------------------------------------------------------------')
print('|                                          CREDIT CARD MANAGEMENT SYSTEM                                      | ')
print('--------------------------------------------------------------------------------------------------------------')
j=int(input("1.Admin\n2.User\n"))
if j==2:
        usnts = input("Enter the  CardNumber to search: ")
        s.searchpk(usnts)
        j=int(input("1.Admin\n2.User\n"))
elif j==1:
    name=input("Enter the name: \n")
    pwd =input("Enter the password: \n")
    if(name=="admin" and pwd=="1234"):
        n = int(input(
        "1.Enter the Credit Card Details \n2.To Index \n3.To Search a CreditCard  by CardNumber \n4.To Search & Delete a CreditCard by Name  \n5.To Delete a CreditCard by CardNumber \n6.To Exit\n"))
        while (n <= 6):
            if (n == 1):
                start=time.time()
                s.pack()
                stop=time.time()
                print("Time taken to execute is: "+str(stop-start)+"ms")
            if (n == 2):
                start=time.time()
                s.indexing()
                stop=time.time()
                print("Time taken to execute is: "+str(stop-start)+"ms")
            if (n == 3):
                usnts = input("Enter the  CardNumber to search: ")
                start=time.time()
                s.searchpk(usnts)
                stop=time.time()
                print("Time taken to execute is: "+str(stop-start)+"ms")
            if (n == 4):
                namets = input("Enter Name of The CardHolder to Search or Delete: ")
                start=time.time()
                s.searchsk(namets)
                stop=time.time()
                print("Time taken to execute is: "+str(stop-start)+"ms")
                
            if (n == 5):
                usntd = input("Enter CardNumber of The CardHolder: ")
                start=time.time()
                stop=time.time()
                s.deletepk(usntd)
                s.maintainSIndex(usntd)
                print("Time taken to execute is: "+str(stop-start)+"ms")
                
            if (n==6):
                j=int(input("1.Admin\n2.User\n"))
                if j>2:
                    print("Please enter the valid choice\n")
            n = int(input(
                "1.Enter the Credit Card Details \n2.To Unpack \n3.To Search a CreditCard  by CardNumber \n4.To Search & Delete a CreditCard by Name  \n5.To Delete a CreditCard by CardNumber \n6.To Exit\n"))
        print('----------------------------------------------------------------------------------------------------------------')

    else:
        print("Please enter the valid name and password")