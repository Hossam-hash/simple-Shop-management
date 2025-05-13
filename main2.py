from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from os import path
import sys
import datetime
import sqlite3
from  xlsxwriter import Workbook
from datetime import datetime
import numpy as np
import xlrd
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),'main_shop1.ui'))
l=None
ll=None
class App_Window(QMainWindow , FORM_CLASS):

    def __init__(self):
        QMainWindow. __init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.Handle_UI()
        self.DB_Connection()
        self.Show_All_products()
        self.autocomplete()
        self.Show_All_sold()
        self.Show_all_Presold()
        self.Show_lost()
        #self.Search()
        #global l
    def Handle_UI(self):
        self.setWindowTitle(' صلــــى علـــــى الـــنبـــي ')
        self.groupBox_4.setVisible(False)
        self.groupBox_5.setVisible(False)
        self.groupBox_6.setVisible(False)
        self.tableWidget_4.setVisible(False)
        self.tableWidget_5.setVisible(False)
    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Product_search)
        #self.pushButton_2.clicked.connect(self.enter_product)
        self.pushButton_3.clicked.connect(self.sell_and_save)
        self.pushButton_2.clicked.connect(self.Search)
        #self.pushButton_4.clicked.connect(self.Retrive_product)
        self.pushButton_4.clicked.connect(self.Product_search2)
        self.pushButton_5.clicked.connect(self.Add_new_product)
        self.pushButton_6.clicked.connect(self.delete_sell)
        self.pushButton_7.clicked.connect(self.retrive_selled)
        self.pushButton_8.clicked.connect(self.Edit_Product)
        self.pushButton_9.clicked.connect(self.delet_product)
        self.pushButton_10.clicked.connect(self.sell_Report)
        self.comboBox.currentTextChanged.connect(self.do_something)
        self.comboBox_2.currentTextChanged.connect(self.combo2)
        self.comboBox_4.currentTextChanged.connect(self.combo4)

        self.pushButton_14.clicked.connect(self.Done_all)
        self.pushButton_13.clicked.connect(self.button)
        self.pushButton_15.clicked.connect(self.detlete_presell)
        self.pushButton_12.clicked.connect(self.changestylesheeet1)
        self.pushButton_16.clicked.connect(self.style2)
        self.pushButton_17.clicked.connect(self.style3)
        self.pushButton_11.clicked.connect(self.style4)
        self.pushButton_20.clicked.connect(self.style5)
        self.pushButton_19.clicked.connect(self.style6)
        self.pushButton_18.clicked.connect(self.style7)
        self.pushButton_21.clicked.connect(self.style8)
        self.pushButton_22.clicked.connect(self.style9)
        self.pushButton_23.clicked.connect(self.style10)
        self.pushButton_24.clicked.connect(self.sty11)

    def DB_Connection(self):
        #connection between app and database
        self.db = sqlite3.connect('mydatabasee.db')
        self.cur = self.db.cursor()
        # self.db=pymysql.connect(host='localhost',user='hossam', password='Hossam110$', db='shop')
    def Show_All_products(self):
        #عرف انتا في اللفه الكام
        QApplication.processEvents()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''select prodctname,cost,quantitiy,buy_price_all,sell_price_all,price_each,barcode from products  ''')
        data=self.cur.fetchall()
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                col += 1
            row_position=self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
    def Product_search(self):
        product_name=self.lineEdit.text()
        try:
            if self.comboBox_2.currentIndex() == 0:

                QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
            if self.comboBox_2.currentIndex() == 1:
                global l
                completer = QCompleter(l)
                self.lineEdit.setCompleter(completer)
                if product_name=='':
                    QMessageBox.information(self, 'خطأ', '  من فضلك ادخل كل البيانات ياعمااااى ابوس ايدك')
                else:
                    sql=('''select * from products where prodctname =? ''')
                    self.cur.execute(sql,[(product_name)])
                    data=self.cur.fetchone()
                    data=list(data)
                    #طلعلي كل المعلومات
                    self.lineEdit_2.setText(str(data[3]))
                    self.lineEdit_3.setText(str(data[2]))
                    self.lineEdit_4.setText(str(data[7]))
                    self.lineEdit_8.setText(str(data[4]))
                    self.lineEdit_9.setText(str(data[5]))
                    self.lineEdit_10.setText(str(data[6]))
                    self.statusBar().showMessage('----------------عملية بحث ناجحة---------------')
            if self.comboBox_2.currentIndex() == 2:

                if product_name == '':
                    QMessageBox.information(self, 'خطأ يابيه', '  من فضلك ادخل كل البيانات يابنى بقاااااا')
                else:
                    sql = ('''select * from products where barcode =? ''')
                    self.cur.execute(sql, [(product_name)])
                    data = self.cur.fetchone()
                    self.lineEdit_2.setText(str(data[3]))
                    self.lineEdit_3.setText(str(data[2]))
                    self.lineEdit_4.setText(str(data[1]))
                    self.lineEdit_8.setText(str(data[4]))
                    self.lineEdit_9.setText(str(data[5]))
                    self.lineEdit_10.setText(str(data[6]))
                    self.statusBar().showMessage('----------------عملية بحث ناجحة---------------')

        except Exception:
            QMessageBox.information(self, 'خطأ', '    اعد البحث مره اخري هذا المنج غيرموجود')
            self.lineEdit.setText('')
    def autocomplete(self):
        global l,ll
        list_date=[]
        list_barcod=[]
        self.cur.execute('''select prodctname from products  ''')
        data = self.cur.fetchall()
        for i in data:
            list_date.append(i[0])
        #completer = QCompleter(list_date)
        l=list_date
        self.cur.execute('''select barcode from products  ''')
        data2 = self.cur.fetchall()
        for i in data2:
            list_barcod.append(str(i[0]))
        ll=list_barcod
        completer2 = QCompleter(list_barcod)
        # create line edit and add auto complete
        #if self.comboBox.currentIndex() == 0:
        #self.lineEdit_5.setCompleter(completer)
        #self.lineEdit.setCompleter(completer)
        #self.lineEdit_13.setCompleter(completer)
        #self.lineEdit_15.setCompleter(completer)
        #self.lineEdit_7.setEnabled(True)
        self.Show_All_products()
        #self.db.commit()
    def enter_product(self):
        self.lineEdit_7.setEnabled(True)
        product_name = self.lineEdit_5.text()
        try:
            if product_name=='':
                QMessageBox.information(self, 'خطأ يابيه', '  من فضلك ادخل كل البيانات يابنى بقاااااا')
            else:
                sql = ('''select * from products where prodctname =? ''')
                self.cur.execute(sql, [(product_name)])
                alldate = self.cur.fetchone()
                self.lineEdit_6.setText(str(alldate[3]))
                self.lineEdit_21.setText(str(alldate[2]))
        except Exception:
            QMessageBox.information(self, 'خطأ', 'مدخلش حروف او تسبهالى فاضيه او الأسم مش موجود')
            self.lineEdit_7.setText('')
    def sell_and_save(self):
        delete_message = QMessageBox.warning(self, 'البيع', ' هل تريد اتمام العملية والحفظ',
                                             QMessageBox.Yes | QMessageBox.No)
        if delete_message == QMessageBox.Yes:
            need_to_sell = self.lineEdit_7.text()
            try:
                if need_to_sell == '':
                    QMessageBox.information(self, 'خطأ', ' من فضلك ادخل كل البيانات متتعبش قلبي يابنى انا عجوز')
                else:
                    need_to_sell=float(need_to_sell)
                    product_name = self.lineEdit_5.text()
                    if self.comboBox.currentIndex() ==0:
                        QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
                    if self.comboBox.currentIndex() == 1:
                        if product_name == '':
                            QMessageBox.information(self, 'خطأ', '  من فضلك ادخل كل البيانات متتعبش قلبي يابنى انا عجوز')
                        else:
                            sql = ('''select * from products where prodctname =? ''')
                            self.cur.execute(sql, [(product_name)])
                            alldate = self.cur.fetchone()
                            quantityall = float(alldate[3])
                            if quantityall<=0:
                                QMessageBox.information(self, 'خطأ', 'مفيش منتج ياحج المنتج صفر او تحت الصفر ناااااااقص')
                                self.lineEdit_5.setText('')
                            else:
                                resdual = quantityall - need_to_sell
                                cost = float(alldate[2])
                                price_each=float(alldate[5])
                                sell_price_all_new=resdual*cost
                                buy_price_product=resdual*price_each
                                sel_price=need_to_sell*cost
                                gain=need_to_sell*cost-need_to_sell*price_each
                                self.cur.execute('''update products set quantitiy=?,buy_price_all=?,sell_price_all=? where prodctname =?  
                                                                        ''', (resdual,buy_price_product,sell_price_all_new, product_name))

                                date = datetime.now()
                                self.cur.execute(
                                    '''insert into selled_products (productname,costt,quantitys,buy_price,daten,gain) values (?,?,?,?,?,?) ''',
                                    (product_name, sel_price, need_to_sell,price_each,date,gain))
                                self.db.commit()
                                self.statusBar().showMessage('عملية البيع تمت بنجاح شكرا ابقى تعاله تانى بحبك')
                                self.lineEdit_7.setText('')
                                self.lineEdit_5.setText('')
                                self.Show_All_sold()
                    if self.comboBox.currentIndex() == 2:
                        if product_name == '':
                            QMessageBox.information(self, 'خطأ','  من فضلك ادخل كل البيانات متتعبش قلبي يابنى انا عجوز')
                        else:
                            sql = ('''select * from products where barcode =? ''')
                            self.cur.execute(sql, [(product_name)])
                            alldate = self.cur.fetchone()
                            quantityall = float(alldate[3])
                            barcode=str(alldate[7])
                            if quantityall <= 0:
                                QMessageBox.information(self, 'خطأ',
                                                        'مفيش منتج ياحج المنتج صفر او تحت الصفر ناااااااقص')
                                self.lineEdit_5.setText('')
                            else:
                                resdual = quantityall - need_to_sell
                                cost = float(alldate[2])
                                price_each=float(alldate[5])
                                sell_price_all_new=resdual*cost
                                buy_price_product=resdual*price_each
                                sel_price=need_to_sell*cost
                                gain=need_to_sell*cost-need_to_sell*price_each
                                self.cur.execute('''update products set quantitiy=?,buy_price_all=?,sell_price_all=? where barcode =?  
                                                                        ''', (resdual,buy_price_product,sell_price_all_new, barcode))

                                date = datetime.now()
                                product_name = str(alldate[1])
                                self.cur.execute(
                                    '''insert into selled_products (productname,costt,quantitys,buy_price,daten,gain) values (?,?,?,?,?,?) ''',
                                    (product_name, sel_price, need_to_sell,price_each,date,gain))
                                self.db.commit()
                                self.statusBar().showMessage('عملية البيع تمت بنجاح شكرا ابقى تعاله تانى بحبك')
                                self.lineEdit_7.setText('')
                                self.lineEdit_5.setText('')
                                self.Show_All_sold()
            except Exception:
                QMessageBox.information(self, 'خطأ', 'متدخلش حروف او تسبهالى فاضيه يابا')
                self.lineEdit_7.setText('')
                self.lineEdit_5.setText('')
                self.lineEdit_6.setText('')
                self.lineEdit_21.setText('')
    def Show_All_sold(self):    #عرف انتا في اللفه الكام

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.cur.execute('''select productname,costt,quantitys,daten from selled_products  ''')
        data=self.cur.fetchall()
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget.setItem(row,col,QTableWidgetItem(str(item)))
                col += 1
            row_position=self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
    def Add_new_product(self):
        Product_name = self.lineEdit_15.text()
        Product_cost = self.lineEdit_16.text()
        Product_quantity = self.lineEdit_17.text()
        Product_buy_price_all = self.lineEdit_19.text()
        productbarcode=self.lineEdit_27.text()
        try:
            if Product_name == '' or Product_cost=='' or Product_quantity=='' or Product_buy_price_all==''   :
                QMessageBox.information(self, 'خطأ', ' دخل كل المعلومات ياحج ابوس ايدك')
            else:
                Product_buy_each_price = float(Product_buy_price_all) / float(Product_quantity)
                Product_sell_price = float(Product_cost) * float(Product_quantity)
                self.cur.execute('''insert into products (prodctname,cost,quantitiy,buy_price_all,sell_price_all,price_each,barcode)
                        values (?,?,?,?,?,?,?)''', (Product_name, float(Product_cost),float( Product_quantity),float( Product_buy_price_all), Product_sell_price,Product_buy_each_price,int(productbarcode)))
                self.db.commit()
                self.lineEdit_15.setText('')
                self.lineEdit_16.setText('')
                self.lineEdit_17.setText('')
                self.lineEdit_19.setText('')
                self.lineEdit_27.setText('')
                self.Show_All_products()
                self.statusBar().showMessage('مبرك المنتج اضاف بنجاح ')
            self.Show_All_products()
            self.Show_All_sold()
        except Exception:
            QMessageBox.information(self, 'خطأ', 'مدخلش حروف او تسبهالى فاضيه يابا')
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_17.setText('')
            # self.lineEdit_18.setText('')
            self.lineEdit_19.setText('')
            # self.lineEdit_20.setText('')
    def retrive_selled(self):
        datee=self.lineEdit_22.text()
        if datee == ''  :
            QMessageBox.information(self, 'خطأ', ' دخل كل المعلومات ياحج ابوس ايدك')
        else:
            try:
                self.pushButton_6.setEnabled(True)
                date = datetime.strptime(datee, '%Y-%m-%d %H:%M:%S.%f')
                sql = ('''select * from selled_products where daten =? ''')
                self.cur.execute(sql, [(date)])
                alldate = self.cur.fetchone()
                self.lineEdit_23.setText(str(alldate[1]))
                self.lineEdit_25.setText(str(alldate[2]))
                self.lineEdit_24.setText(str(alldate[3]))
            except ValueError:
                QMessageBox.information(self, 'خطأ', ' دخل تاريخ كامل زى اللى مكتوب في العمليات اليوميه')
    def delete_sell(self):
        delete_message = QMessageBox.warning(self, 'مسح عملية بيع', 'هل تريد مسح العمليه ', QMessageBox.Yes | QMessageBox.No)
        if delete_message == QMessageBox.Yes:
            datee = self.lineEdit_22.text()
            date = datetime.strptime(datee, '%Y-%m-%d %H:%M:%S.%f')
            sql = ('''select * from selled_products where daten =? ''')
            self.cur.execute(sql, [(date)])
            alldate = self.cur.fetchone()
            name = alldate[1]
            sql = ('''delete from selled_products where daten =?''')
            self.cur.execute(sql, [(date)])
            quantity_sold=alldate[3]
            sql = ('''select * from products where prodctname =? ''')
            self.cur.execute(sql, [(name)])
            alldate = self.cur.fetchone()
            quantityall = int(alldate[3])
            resdual = quantityall + quantity_sold
            cost = int(alldate[2])
            price_each = int(alldate[5])
            sell_price_all_new = resdual * cost
            buy_price_product = resdual * price_each
            self.cur.execute('''update products set quantitiy=?,buy_price_all=?,sell_price_all=? where prodctname =? ''',(resdual, buy_price_product, sell_price_all_new, name))
            self.db.commit()
        self.statusBar().showMessage('عملية الاعاده تمت بنجاح عشان محترمين بحبك برضو')
        self.Show_All_products()
        self.Show_All_sold()
        self.lineEdit_22.setText('')
        self.lineEdit_23.setText('')
        self.lineEdit_24.setText('')
        self.lineEdit_25.setText('')
    def Product_search2(self):
        product_name=self.lineEdit_13.text()
        try:
            if self.comboBox_4.currentIndex() == 0:
                self.lineEdit_13.setText('')
                QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
            if self.comboBox_4.currentIndex() == 1:
                if product_name=='':
                    QMessageBox.information(self, 'خطأ', '  من فضلك ادخل كل البيانات ياعمااااى ابوس ايدك')
                else:
                    sql=('''select * from products where prodctname =? ''')
                    self.cur.execute(sql,[(product_name)])
                    data=self.cur.fetchone()
                    data=list(data)
                    #طلعلي كل المعلومات
                    self.lineEdit_18.setText(str(data[3]))
                    self.lineEdit_26.setText(str(data[2]))
                    self.lineEdit_11.setText(str(data[0]))
                    self.lineEdit_14.setText(str(data[4]))
                    self.lineEdit_20.setText(str(data[5]))
                    self.lineEdit_12.setText(str(data[6]))
                    self.lineEdit_28.setText(str(data[7]))
                    self.statusBar().showMessage('----------------عملية بحث ناجحة---------------')
                    self.pushButton_8.setEnabled(True)
                    self.pushButton_9.setEnabled(True)
            if self.comboBox_4.currentIndex() == 2:
                sql = ('''select * from products where barcode =? ''')
                self.cur.execute(sql, [(product_name)])
                data = self.cur.fetchone()
                self.lineEdit_18.setText(str(data[3]))
                self.lineEdit_26.setText(str(data[2]))
                self.lineEdit_11.setText(str(data[0]))
                self.lineEdit_14.setText(str(data[4]))
                self.lineEdit_20.setText(str(data[5]))
                self.lineEdit_12.setText(str(data[6]))
                self.lineEdit_28.setText(str(data[1]))
                self.statusBar().showMessage('----------------عملية بحث ناجحة---------------')
                self.pushButton_8.setEnabled(True)
                self.pushButton_9.setEnabled(True)
        except Exception:
            QMessageBox.information(self, 'خطأ', '    اعد البحث مره اخري هذا المنج غيرموجود')
            self.lineEdit_13.setText('')
    def Edit_Product(self):
        delete_message = QMessageBox.warning(self, 'التعديل', ' هل تريد اتمام العملية والحفظ',QMessageBox.Yes | QMessageBox.No)
        if delete_message == QMessageBox.Yes:
            if self.comboBox_4.currentIndex() == 1:
                product_name = self.lineEdit_13.text()
                cost = float(self.lineEdit_26.text())
                quantitiy = float(self.lineEdit_18.text())
                buy_price_all = float(self.lineEdit_14.text())
                price_each = buy_price_all / quantitiy
                sell_price_all_new = cost * quantitiy
                try:
                    bar = self.lineEdit_28.text()
                    if product_name == '' and cost == 0 and quantitiy == 0 and buy_price_all == 0:
                        QMessageBox.information(self, 'خطأ', '  من فضلك ادخل كل البيانات ')
                    else:
                        self.cur.execute('''update products set barcode =?,  cost=? , quantitiy=?,buy_price_all=?,price_each=?,sell_price_all=? where prodctname =?  ''',(int(bar), cost, quantitiy, buy_price_all, price_each, sell_price_all_new, product_name))
                        self.db.commit()
                        self.Show_All_products()
                        self.lineEdit_13.setText('')
                        self.lineEdit_18.setText('')
                        self.lineEdit_26.setText('')
                        self.lineEdit_11.setText('')
                        self.lineEdit_14.setText('')
                        self.lineEdit_20.setText('')
                        self.lineEdit_12.setText('')
                        self.lineEdit_28.setText('')
                except ValueError:
                    #bar = float(self.lineEdit_11.text())
                    bar = None
                    self.cur.execute('''update products set barcode =?,  cost=? , quantitiy=?,buy_price_all=?,price_each=?,sell_price_all=? where prodctname =? ''',(bar, cost, quantitiy, buy_price_all, price_each, sell_price_all_new, product_name))
                    self.db.commit()
                    QMessageBox.information(self, 'message', '  barcode=None ')
                    self.Show_All_products()
                    self.lineEdit_13.setText('')
                    self.lineEdit_18.setText('')
                    self.lineEdit_26.setText('')
                    self.lineEdit_11.setText('')
                    self.lineEdit_14.setText('')
                    self.lineEdit_20.setText('')
                    self.lineEdit_12.setText('')
                    self.lineEdit_28.setText('')
            if self.comboBox_4.currentIndex() == 2:
                barcod =int( self.lineEdit_13.text())
                name=self.lineEdit_28.text()
                cost = float(self.lineEdit_26.text())
                quantitiy = float(self.lineEdit_18.text())
                buy_price_all =float( self.lineEdit_14.text())
                if barcod=='' and cost==0 and quantitiy==0 and buy_price_all==0 :
                    QMessageBox.information(self, 'خطأ', '  من فضلك ادخل كل البيانات ياعمااااى ابوس ايدك')
                else:
                    price_each =buy_price_all/quantitiy
                    sell_price_all_new = cost*quantitiy
                    self.cur.execute('''update products set prodctname =?,  cost=? , quantitiy=?,buy_price_all=?,price_each=?,sell_price_all=? where barcode =?  ''',(name,cost, quantitiy,buy_price_all, price_each,sell_price_all_new,barcod ))
                    self.db.commit()
                self.Show_All_products()
                self.lineEdit_13.setText('')
                self.lineEdit_28.setText('')
                self.lineEdit_18.setText('')
                self.lineEdit_26.setText('')
                self.lineEdit_11.setText('')
                self.lineEdit_14.setText('')
                self.lineEdit_20.setText('')
                self.lineEdit_12.setText('')
    def delet_product(self):
        try:
            product_name = self.lineEdit_13.text()
            if product_name == '' :
                QMessageBox.information(self, 'خطأ', ' من فضلك ادخل كل البيانات ياعمااااى ابوس ايدك')
            else:
                delete_message = QMessageBox.warning(self, 'Deleting', 'do you want to delete',QMessageBox.Yes | QMessageBox.No)
                if delete_message == QMessageBox.Yes:
                    sql = ('''delete from products where prodctname =? ''')
                    self.cur.execute(sql, [(product_name)])
                    self.db.commit()
                    self.statusBar().showMessage('Product  is Deleted successfuly----->')
                    QMessageBox.information(self, 'Deleting', 'Product is Deleted successfuly----->')
                    self.Show_All_products()
                    self.lineEdit_13.setText('')
                    self.lineEdit_18.setText('')
                    self.lineEdit_26.setText('')
                    self.lineEdit_11.setText('')
                    self.lineEdit_14.setText('')
                    self.lineEdit_20.setText('')
                    self.lineEdit_12.setText('')
                    self.lineEdit_28.setText('')
        except Exception:
            QMessageBox.information(self, 'خطأ', '    اعد البحث مره اخري هذا المنج غيرموجود')
            self.lineEdit_13.setText('')
    def sell_Report(self):
        save_place = QFileDialog.getSaveFileName(self, caption='save as', filter='All Files(*.xlsx)')
        text = str(save_place)
        name = (text[2:].split(',')[0].replace("'", ''))
        self.cur.execute('''select productname,costt,quantitys,buy_price,daten,gain from selled_products  ''')
        data = self.cur.fetchall()
        excel_file = Workbook(name)
        #excel_file = Workbook('sell_report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, 'إسم المنتج')
        sheet1.write(0, 1, 'ثمن البيع')
        sheet1.write(0, 2, 'الكمية')
        sheet1.write(0, 3, 'ثمن الشراء')
        sheet1.write(0, 4, 'تاريخ العمليه')
        sheet1.write(0, 5, 'الربح')
        row_num = 1
        for row in data:
            colm_num = 0  ###العمود
            for item in row:
                sheet1.write(row_num, colm_num, item)
                colm_num += 1
            row_num += 1
        excel_file.close()
        self.statusBar().showMessage('excel file report is exported successfuly----->')
        QMessageBox.information(self, 'التقرير', '    تم اصدار التقرير بنجاح ')
    def Search(self):
        enter_data=self.lineEdit_5.text()
        if self.comboBox.currentIndex() == 0:
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_5.setText('')
            QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
        if self.comboBox.currentIndex() == 1:
            product_name = self.lineEdit_5.text()
            try:
                if product_name == '':
                    QMessageBox.information(self, 'خطأ يابيه', '  من فضلك ادخل كل البيانات يابنى بقاااااا')
                else:
                    sql = ('''select * from products where prodctname =? ''')
                    self.cur.execute(sql, [(product_name)])
                    alldate = self.cur.fetchone()
                    self.lineEdit_6.setText(str(alldate[3]))
                    self.lineEdit_21.setText(str(alldate[2]))
                    self.lineEdit_7.setEnabled(True)
            except Exception:
                QMessageBox.information(self, 'خطأ', 'مدخلش حروف او تسبهالى فاضيه او الأسم مش موجود')
                self.lineEdit_7.setText('')
        if self.comboBox.currentIndex() == 2:
            product_name = self.lineEdit_5.text()
            try:
                if product_name == '':
                    QMessageBox.information(self, 'خطأ يابيه', '  من فضلك ادخل كل البيانات يابنى بقاااااا')
                else:
                    sql = ('''select * from products where barcode =? ''')
                    self.cur.execute(sql, [(product_name)])
                    alldate = self.cur.fetchone()
                    self.lineEdit_6.setText(str(alldate[3]))
                    self.lineEdit_21.setText(str(alldate[2]))
                    self.lineEdit_7.setEnabled(True)
            except Exception:
                QMessageBox.information(self, 'خطأ', 'مدخلش حروف او تسبهالى فاضيه او الأسم مش موجود')
                self.lineEdit_7.setText('')
    def combo2(self):
        if self.comboBox_2.currentIndex() == 0:
            QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
        if self.comboBox_2.currentIndex() == 1:
            global l
            completer = QCompleter(l)
            self.lineEdit.setCompleter(completer)
        if self.comboBox_2.currentIndex() == 2:
            global ll
            completer = QCompleter(ll)
            self.lineEdit.setCompleter(completer)
    def do_something(self):
        if self.comboBox.currentIndex() == 0:
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_5.setText('')
            QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
        if self.comboBox.currentIndex() == 1:
            self.lineEdit_5.setEnabled(True)
            global l
            completer = QCompleter(l)
            self.lineEdit_5.setCompleter(completer)
        if self.comboBox.currentIndex() == 2:
            self.lineEdit_5.setEnabled(True)
            global ll
            completer = QCompleter(ll)
            self.lineEdit_5.setCompleter(completer)
        if self.comboBox.currentIndex() == 3:
            try:
                save_place = QFileDialog.getOpenFileName(self, caption='open', directory='.', filter='All Files(*.xls)')
                excelpath = save_place[0]
                #path=u'C:/Users/sat/Desktop/بببببب.xls.xlsx'
                #path=u'C:\\Users\\hossam\\Desktop\\1.xls'
                bar=self.barcode_reader(excelpath)
                for i in bar:
                    self.cur.execute('''insert into barcodes (barcode) values (?)''', (int(i),))
                    self.db.commit()
                self.groupBox_2.setVisible(False)
                self.tableWidget.setVisible(False)
                self.groupBox_4.setVisible(True)
                self.groupBox_6.setVisible(True)
                self.groupBox_5.setVisible(True)
                self.tableWidget_4.setVisible(True)
                self.tableWidget_5.setVisible(True)
                sql = ('''select * from barcodes  ''')
                self.cur.execute(sql)
                data = self.cur.fetchall()
                quantity = 1
                date = datetime.now()
                u = 0
                for i in data:
                    sql = ('''select * from products where barcode =? ''')
                    self.cur.execute(sql, [(int(i[0]))])
                    data2 = self.cur.fetchone()
                    try:
                        quantityall = float(data2[3])
                        if quantityall <= 0:
                            QMessageBox.information(self, 'خطأ', 'الكميه المتاحه لهذا المنتج %s = صفر' % int(i[0]))
                            self.lineEdit_31.setText('')
                            pass
                        else:
                            # resdual = quantityall - quantity
                            cost = float(data2[2])
                            price_each = float(data2[5])
                            # sell_price_all_new = resdual * cost
                            # buy_price_product = resdual * price_each
                            sel_price = quantity * cost
                            gain = quantity * cost - quantity * price_each
                            self.cur.execute( '''insert into preselled (name,barcode,sellcost,qantity,datee,gainp,buyprice,price_each) values (?,?,?,?,?,?,?,?)''',(data2[1], int(data2[7]), float(data2[2]), quantity, date, gain, sel_price,price_each))
                            self.db.commit()
                    except TypeError:
                        u = u + 1
                        completer = QCompleter(l)
                        self.lineEdit_31.setCompleter(completer)
                        self.cur.execute('''insert into lost (barcode) values (?)''', (int(i[0]),))
                        self.db.commit()
                        self.Show_all_Presold()
                        self.Show_lost()
                QMessageBox.information(self, 'خطأ', "تم إضافة عدد %s الى جدول المفقود" % u)
            except Exception:
                QMessageBox.information(self, 'خطأ', "هذا الملف غير صالح" )
                self.comboBox.setCurrentIndex(0)
    def barcode_reader(self,path):
        barcodes = []
        try:
            book = xlrd.open_workbook(path, encoding_override="cp1251")
        except:
            book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
        for rx in range(sh.nrows):
            if rx == 0:
                pass

            else:
                s = sh.row(rx)
                codes = str(s[1]).split(':')[1].strip().replace("'", '')
                if  '.0' in codes:
                    b = int(codes.replace('.0', ''))
                else:
                    b=int(codes.replace('.',''))
                barcodes.append(b)
                #barcodes.append(int(codes[1].split('.')[0].replace("'", '')))
        return barcodes
    def Show_all_Presold(self):
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        self.cur.execute('''select id,name,sellcost,qantity,barcode,datee,buyprice from preselled  ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)
        self.cur.execute('''select sellcost from preselled  ''')
        data = self.cur.fetchall()
        sumtion_list = []
        for i in data:
            sumtion_list.append(float(i[0]))
        sumtion = sum(sumtion_list)
        self.lineEdit_35.setText(str(sumtion))
    def Show_lost(self):
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        self.cur.execute('''select barcode from lost  ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
    def button(self):
        quantity=1
        date=datetime.now()
        product_name = self.lineEdit_31.text()
        if product_name == '':
            QMessageBox.information(self, 'خطأ ', '  من فضلك ادخل كل البيانات ')
        else:
            sql = ('''select * from products where prodctname =? ''')
            self.cur.execute(sql, [(product_name)])
            data2 = self.cur.fetchone()
            quantityall = float(data2[3])
            if quantityall <= 0:
                QMessageBox.information(self, 'خطأ', 'الكميه المتاحه لهذا المنتج  = صفر')
                self.lineEdit_31.setText('')
            else:
                cost = float(data2[2])
                price_each = float(data2[5])
                # sell_price_all_new = resdual * cost
                # buy_price_product = resdual * price_each
                sel_price = quantity * cost
                gain = quantity * cost - quantity * price_each
                if data2[7] == None:
                    self.cur.execute('''insert into preselled (name,barcode,sellcost,qantity,datee,gainp,buyprice,price_each) values (?,?,?,?,?,?,?,?)''',(data2[1], 1, float(data2[2]), quantity, date, gain, sel_price,price_each))
                    self.db.commit()
                else:
                    self.cur.execute('''insert into preselled (name,barcode,sellcost,qantity,datee,gainp,buyprice,price_each) values (?,?,?,?,?,?,?,?)''',(data2[1], float(data2[7]), float(data2[2]), quantity, date, gain, sel_price,price_each))
                    self.db.commit()
                self.Show_all_Presold()
                QMessageBox.information(self, 'معلومة', 'تم الإضافه بنجاح')
        self.cur.execute('''select sellcost from preselled  ''')
        data = self.cur.fetchall()
        sumtion_list=[]
        for i in  data:
            sumtion_list.append(float(i[0]))
        sumtion=sum(sumtion_list)
        self.lineEdit_35.setText(str(sumtion))
    def detlete_presell(self):
        self.cur.execute('''select * from preselled  ''')
        data = self.cur.fetchall()
        id_deleted = self.lineEdit_34.text()
        if id_deleted == '':
            QMessageBox.information(self, 'خطأ ', '  من فضلك ادخل كل البيانات ')
        else:
            sql = ('''delete from preselled where id =? ''')
            self.cur.execute(sql, [(int(id_deleted))])
            self.db.commit()
        self.Show_all_Presold()
    def Done_all(self):
        self.cur.execute('''select * from preselled  ''')
        data = self.cur.fetchall()
        for i in  data:
            name1=i[1]
            barcode1=int(i[2])
            #sellcost1=float(i[3])#gain1=float(i[6])#buyprice1=float(i[7])#price_each=float(i[8])#id1=int(i[0])
            quantity1=float(i[4])
            date1=i[5]
            sql = ('''select * from products where prodctname =? ''')
            self.cur.execute(sql, [(name1)])
            alldate = self.cur.fetchone()
            quantityall = float(alldate[3])
            if quantityall <= 0:
                QMessageBox.information(self, 'خطأ', 'مفيش منتج ياحج المنتج صفر او تحت الصفر ناااااااقص')
                self.lineEdit_5.setText('')
            else:
                resdual = quantityall - quantity1
                cost = float(alldate[2])
                price_each = float(alldate[5])
                sell_price_all_new = resdual * cost
                buy_price_product = resdual * price_each
                sel_price = quantity1 * cost
                gain = quantity1 * cost - quantity1 * price_each
                self.cur.execute('''update products set quantitiy=?,buy_price_all=?,sell_price_all=? where prodctname =?  ''', (resdual, buy_price_product, sell_price_all_new, name1))
                self.cur.execute('''insert into selled_products (productname,costt,quantitys,buy_price,daten,gain,barcodee) values (?,?,?,?,?,?,?) ''',(name1, sel_price, quantity1, price_each, date1, gain,barcode1))
                self.db.commit()
                self.Show_All_sold()
        sql = ('''delete from preselled  ''')
        self.cur.execute(sql, )
        sql = ('''delete from barcodes  ''')
        self.cur.execute(sql, )
        sql = ('''delete from lost  ''')
        self.cur.execute(sql, )
        self.Show_all_Presold()
        self.groupBox_2.setVisible(True)
        self.tableWidget.setVisible(True)
        self.groupBox_4.setVisible(False)
        self.groupBox_6.setVisible(False)
        self.groupBox_5.setVisible(False)
        self.tableWidget_4.setVisible(False)
        self.tableWidget_5.setVisible(False)
        self.db.commit()
        QMessageBox.information(self, 'Done', 'Done Thanks')
        self.comboBox.setCurrentIndex(1)
        self.lineEdit_31.setText('')
        self.lineEdit_34.setText('')
    def combo4(self):
        if self.comboBox_4.currentIndex() == 0:
            QMessageBox.information(self, 'خطأ', 'من فضلك اختار البحث بالاسم او الباركود')
        if self.comboBox_4.currentIndex() == 1:
            global l
            completer = QCompleter(l)
            self.lineEdit_13.setCompleter(completer)
        if self.comboBox_4.currentIndex() == 2:
            global ll
            completer = QCompleter(ll)
            self.lineEdit_13.setCompleter(completer)
    def changestylesheeet1(self):
        stylesheet='''/*  ---------------------------- ALL OTHERS WIDGETS ---------------------------- */
            *{
            selection-background-color: rgb(67, 128, 179);
            selection-color: rgb(255, 255, 255);
            }
            /*  ---------------------------- MAIN WINDOW, WIDGET ---------------------------- */
            QMainWindow,QWidget
            {
            color:rgb(0,0,0);
            background:rgb(255,255,255);
            }
            /*  ---------------------------- MENU BAR ---------------------------- */
            QMenuBar
            {
            color:rgb(120,120,120);
            background:rgb(230,230,230);
            }
            QMenuBar::item:selected
            {
            color:rgb(100,100,100);
            background:rgb(200,200,200);
            }
            /*  ---------------------------- CONTEXT MENU ---------------------------- */
            QMenu
            {
            color:rgb(90,90,90);
            background:rgb(230,230,230);
            padding: 3;
            }
            QMenu::item:selected
            {
            color:rgb(90,90,90);
            background:rgb(200,200,200);
            }
            QMenu::separator {
            background:rgb(200,200,200);
            height:1px;
            }
            /*  ---------------------------- Q TAB BAR ---------------------------- */
            QTabBar::tab {
            color:rgb(150,150,150);
            background:rgb(240,240,240);
            height:30;
            width:80;
            border: rgb(240,240,240);
            border-width: 0 0 2px 0;
            padding-left:10;
            }
            QTabBar::tab:selected {
            background:white;
            color:rgb(100,100,100);
            border: solid rgb(0,150,255);
            border-width: 0 0 5px 0;
            }
            QTableWidget QTableCornerButton::section {
            background-color: rgb(255, 255, 255);
            }
            /*-----------------------------------------------------------------
            ------------------------------ LINE_EDIT --------------------------
            ------------------------------ TEXT BROWSER -----------------------
            ------------------------------ TEXT_EDIT---------------------------
            ------------------------------ PLAIN_TEXT -------------------------
            ------------------------------------------------------------------- */
            QLineEdit,QTextBrowser,QTextEdit,QPlainTextEdit
            {
            color:rgb(20,20,20);
            background-color:white;
            border: solid lightgrey;
            border-width: 0 0 2px 0;
            border-bottom-left-radius: 5;
            border-bottom-right-radius: 5;
            }
            QLineEdit:disabled
            {
            color:rgb(160, 150, 150);
            background-color:rgb(255, 240, 240);
            border: solid rgb(253, 14, 14);
            border-width: 0 0 2px 0;
            border-bottom-left-radius: 5;
            border-bottom-right-radius: 5;
            }
            /*  ---------------------------- COMBO BOX ----------------------------*/
            QComboBox
            {
            color:rgb(0,115,170);
            background-color:rgb(255, 255, 255);
            min-width: 5px;
            padding: 1px 0px 1px 3px;
            border: 1px solid rgb(0,115,170);
            }      
            QComboBox:hover
            {
            color:rgb(0,115,170);
            background-color: white;
            }        
            QComboBox:selected
            {
            color:rgb(0,115,170);
            selection-background-color: rgb(255, 255, 255);
            }        
            QComboBox::drop-down
            {
            width: 30px;
            background-color:rgb(0,115,170);
            }        
            QComboBox::down-arrow
            {
            image: url(assets/UI/Icons/interface_icons/arrow_down.png);
            width: 14px;
            height: 14px;
            }       
            /* -------------------------------- CHECK BOX ----------------------------------------- */
            QCheckBox
            {
            background: rgb(255, 255, 255);
            color:rgb(25, 29, 32);
            padding: 6;
            }
            /* ----------------------------  TOOL BOX  ----------------------------  */
            QToolBox::tab
            {
            color:darkgrey;
            background:lightgrey;
            }
            QToolBox::tab::selected
            {
            color:grey;
            background:rgb(250, 250,250);
            }
            QToolBox::tab::hover
            {
            color:white;
            background:rgb(0,115,170);
            }
            /*  ---------------------------- PROGRESS BAR ---------------------------- */
            QProgressBar {
            color:grey;
            text-align: center;
            font-size:13px;
            }
            QProgressBar::chunk {
            background:rgb(0, 193, 50);
            }
            /*  ---------------------------- PUSHBUTTON ---------------------------- */
            QPushButton
            {
            border: 1px solid lightgrey;
            color:white;
            background:rgb(0,115,170);
            min-height:30;
            min-width: 50;
            }
            QPushButton:hover
            {
            border: 1px solid lightgrey;
            color:white;
            background:rgb(0, 120, 210);
            }      
            QPushButton:pressed
            {
            border: 1px solid lightgrey;
            color:white;
            background:rgb(0, 53, 100);
            }
            /*  ----------------------------  LCD NUMBER ---------------------------- */
            QLCDNumber
            {
            color:rgb(0,115,170);
            border:2 solid rgb(100,100,100);
            }
            /*  ---------------------------- TABLE_LIST_TABLE ---------------------------- */
            QTableView,
            QTableWidget
            {
            alternate-background-color: rgb(240, 250, 255);
            }
            QTreeView
            {
            background: rgb(250,250,250);
            color: rgb(180,180,180);
            }
            QTableView::item:selected, 
            QListView::item:selected,
            QTableView::item:hover, 
            QListView::item:hover, 
            QTreeView::item:hover
            {
            background:rgb(0,115,170);
            color:rgb(250,250,250);
            }
            QTableView::item, 
            QListView::item, 
            QTreeView::item
            {
            color:rgb(100,100,100);
            }
            QTreeView::item:selected,QListView::item:selected,QTableView::item:selected
            {
            color:rgb(37, 62, 71);
            background:rgb(209, 241, 252);
            }
            /* QTreeView::item:has-children
            {
            background-color: rgb(0, 78, 134);
            color: white;
            border-bottom: 2px solid qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(255, 255, 255, 0), stop:0.5 rgba(0, 150, 255, 255), stop:1 rgba(255, 255, 255, 0));
            }
            */
            /*  ---------------------------- HEADER VIEW ---------------------------- */
            QHeaderView::section
            {
            color:rgb(133, 133, 133);
            background:white;
            border:transparent;
            text-align:center;
            padding:1;
            }
            /* ------------------------------- CALENDAR -------------------------------------------------- */
            QCalendarView
            {
            color: rgb(20,20,20);
            background-color: rgb(240,240,240);
            alternate-background-color: rgb(0,115,170);
            selection-background-color: white;
            selection-color: black;
            }
            QAbstractItemView
            {
            color:rgb(200,200,200);
            }      
            /* ---------------------------------------- SLIDER HORIZONTAL ----------------------------------------------- */      
            QSlider::groove:horizontal,QSlider::add-page:horizontal
            {
            background: rgb(255, 255, 255);
            height: 27px;
            }
            QSlider::sub-page:horizontal {
            height: 10px;
            background: rgb(0,115,170);
            }
            QSlider::handle:horizontal {
            margin-right: -10px;
            margin-left: -10px;
            background: rgb(0,115,170);
            }
            QSlider::handle:horizontal:hover {
            background:rgb(0,115,170);
            }      
            /* --------------------------------  VERTICAL SLIDER --------------------------------------------------------------  */       
            QSlider::handle
            {
            border-radius: 3px;
            }       
            QSlider::groove:vertical,QSlider::add-page:vertical,QSlider::sub-page:vertical
            {
            width: 20px;
            background: rgb(255, 255, 255);
            }       
            QSlider::handle:vertical {
            margin-top: -10px;
            margin-bottom: -10px;
            background: rgb(0,115,170);
            }
            QSlider::handle:vertical:hover {
            background: rgb(0,115,170);
            }      
            /* --------------------------------- SCROLLBAR HORIZONTAL --------------------------------------  */     
            QScrollBar::groove:horizontal{
            background: white;
            height: 17px;
            }
            QScrollBar::sub-page:horizontal,QScrollBar::add-page:horizontal  {
            height: 10px;
            background: rgb(255, 255, 255);
            }
            QScrollBar::handle:horizontal {
            margin-right: -5px;
            background: rgb(0,115,170);
            }
            QScrollBar::handle:horizontal:hover {
            background: rgb(0,115,170);
            }
            /* --------------------------------------- SCROLLBAR VERTICAL ----------------------------------------------  */
            /* SCROLLBAR */
            QScrollBar:vertical {
            background: white;
            width: 15px;
            margin: 22px 0 22px 0;
            }
            /* HANDLE*/
            QScrollBar::handle:vertical {
            background: rgb(0,115,170);
            min-height: 20px;
            }  
            /* UP ARROW */
            QScrollBar::up-arrow:vertical {
            image: url(assets/UI/Icons/interface_icons/arrow_up.png);
            width: 10px;
            height: 10px;
            }
            /* DOWN ARROW */
            QScrollBar::down-arrow:vertical {
            image: url(assets/UI/Icons/interface_icons/arrow_down.png);
            width: 10px;
            height: 10px;
            }
            /* UP BUTTON */
            QScrollBar::sub-line:vertical {
            background: rgb(0,115,170);
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
            }
            /* DOWN BUTTON */
            QScrollBar::add-line:vertical {
            background: rgb(0,115,170);
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            }
            /* SUBPAGES - ADDPAGE */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
            }
            /* ---------------------------------- Q TOOL BAR -------------------------------------------------------- */
            /* TOOLBAR REGION */
            QToolBar {
            background: rgb(35,40,45);
            spacing: 20;       
            }
            /* SEPARATOR */
            QToolBar:separator
            {
            background: rgb(80, 80, 80);
            height: 2;
            }
            /* QToolBar QToolButton { 
                width: 100px;
            } */
            /* -----------------------------------------------Q TOOL BUTTON------------------------------------------- */
            /* BUTTON */
            QToolButton
            {
            color: rgb(255, 255, 255);
            background:rgb(35,40,45);
            }        
            QToolButton:hover,QToolButton:pressed
            {
            background-color: rgb(64, 73, 82);
            }       
            QMessageBox QLabel
            {
            color: red;
            }'''
        self.tabWidget.setStyleSheet(stylesheet)
    def style2(self):
        style2='''/*
 *  BreezeDark stylesheet.
 *
 *  :author: Colin Duquesnoy
 *  :editor: Alex Huszagh
 *  :license: MIT, see LICENSE.md
 *
 *  This is originally a fork of QDarkStyleSheet, and is based on Breeze/
 *  BreezeDark color scheme, but is in no way affiliated with KDE.
 *
 * ---------------------------------------------------------------------
 *  The MIT License (MIT)
 *
 * Copyright (c) <2013-2014> <Colin Duquesnoy>
 * Copyright (c) <2015-2016> <Alex Huszagh>
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 * ---------------------------------------------------------------------
 */

QToolTip
{
    border: 0.1ex solid #eff0f1;
    background-color: #31363b;
    alternate-background-color: #3b4045;
    color: #eff0f1;
    padding: 0.5ex;
    opacity: 200;
}

QWidget
{
    color: #eff0f1;
    background-color: #31363b;
    selection-background-color:#3daee9;
    selection-color: #eff0f1;
    background-clip: border;
    border-image: none;
    border: 0px transparent black;
    outline: 0;
}

QWidget:item:hover
{
    background-color: #3daee9;
    color: #eff0f1;
}

QWidget:item:selected
{
    background-color: #3daee9;
}


QCheckBox
{
    spacing: 0.5ex;
    outline: none;
    color: #eff0f1;
    margin-bottom: 0.2ex;
    opacity: 200;
}

QCheckBox:disabled
{
    color: #76797c;
}

QGroupBox::indicator
{
    margin-left: 0.2ex;
}

QCheckBox::indicator:unchecked,
QCheckBox::indicator:unchecked:focus
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QCheckBox::indicator:unchecked:hover,
QCheckBox::indicator:unchecked:pressed,
QGroupBox::indicator:unchecked:hover,
QGroupBox::indicator:unchecked:focus,
QGroupBox::indicator:unchecked:pressed
{
    border: none;
    border-image: url(:/dark/checkbox_unchecked.svg);
}

QCheckBox::indicator:checked
{
    border-image: url(:/dark/checkbox_checked.svg);
}

QCheckBox::indicator:checked:hover,
QCheckBox::indicator:checked:focus,
QCheckBox::indicator:checked:pressed,
QGroupBox::indicator:checked:hover,
QGroupBox::indicator:checked:focus,
QGroupBox::indicator:checked:pressed
{
    border: none;
    border-image: url(:/dark/checkbox_checked.svg);
}

QCheckBox::indicator:indeterminate
{
    border-image: url(:/dark/checkbox_indeterminate.svg);
}

QCheckBox::indicator:indeterminate:focus,
QCheckBox::indicator:indeterminate:hover,
QCheckBox::indicator:indeterminate:pressed
{
    border-image: url(:/dark/checkbox_indeterminate.svg);
}

QCheckBox::indicator:indeterminate:disabled
{
    border-image: url(:/dark/checkbox_indeterminate_disabled.svg);
}

QCheckBox::indicator:checked:disabled,
QGroupBox::indicator:checked:disabled
{
    border-image: url(:/dark/checkbox_checked_disabled.svg);
}

QCheckBox::indicator:unchecked:disabled,
QGroupBox::indicator:unchecked:disabled
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QRadioButton
{
    spacing: 0.5ex;
    outline: none;
    color: #eff0f1;
    margin-bottom: 0.2ex;
}

QRadioButton:disabled
{
    color: #76797c;
}

QRadioButton::indicator:unchecked,
QRadioButton::indicator:unchecked:focus
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}


QRadioButton::indicator:unchecked:hover,
QRadioButton::indicator:unchecked:pressed
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_unchecked.svg);
}


QRadioButton::indicator:checked
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_checked.svg);
}

QRadioButton::indicator:checked:hover,
QRadioButton::indicator:checked:focus,
QRadioButton::indicator:checked:pressed
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_checked.svg);
}

QRadioButton::indicator:checked:disabled
{
    outline: none;
    border-image: url(:/dark/radio_checked_disabled.svg);
}

QRadioButton::indicator:unchecked:disabled
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenuBar
{
    background-color: #31363b;
    color: #eff0f1;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 0.1ex solid #76797c;
}

QMenuBar::item:pressed
{
    border: 0.1ex solid #76797c;
    background-color: #3daee9;
    color: #eff0f1;
    margin-bottom: -0.1ex;
    padding-bottom: 0.1ex;
}

QMenu
{
    border: 0.1ex solid #76797c;
    color: #eff0f1;
    margin: 0.2ex;
}

QMenu::icon
{
    margin: 0.5ex;
}

QMenu::item
{
    padding: 0.5ex 3ex 0.5ex 3ex;
    margin-left: 0.5ex;
    border: 0.1ex solid transparent; /* reserve space for selection border */
}

QMenu::item:selected
{
    color: #eff0f1;
}

QMenu::separator
{
    height: 0.2ex;
    background: lightblue;
    margin-left: 1ex;
    margin-right: 0.5ex;
}

/* non-exclusive indicator = check box style indicator
   (see QActionGroup::setExclusive) */
QMenu::indicator:non-exclusive:unchecked
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:unchecked:selected
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:checked
{
    border-image: url(:/dark/checkbox_checked.svg);
}

QMenu::indicator:non-exclusive:checked:selected
{
    border-image: url(:/dark/checkbox_checked.svg);
}

/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:exclusive:unchecked
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:unchecked:selected
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:checked
{
    border-image: url(:/dark/radio_checked.svg);
}

QMenu::indicator:exclusive:checked:selected
{
    border-image: url(:/dark/radio_checked.svg);
}

QMenu::right-arrow
{
    margin: 0.5ex;
    border-image: url(:/light/right_arrow.svg);
    width: 0.6ex;
    height: 0.9ex;
}


QWidget:disabled
{
    color: #454545;
    background-color: #31363b;
}

QAbstractItemView
{
    alternate-background-color: #31363b;
    color: #eff0f1;
    border: 0.1ex solid 3A3939;
    border-radius: 0.2ex;
}

QWidget:focus,
QMenuBar:focus
{
    border: 0.1ex solid #3daee9;
}

QTabWidget:focus,
QCheckBox:focus,
QRadioButton:focus,
QSlider:focus
{
    border: none;
}

QLineEdit
{
    background-color: #232629;
    padding: 0.5ex;
    border-style: solid;
    border: 0.1ex solid #76797c;
    border-radius: 0.2ex;
    color: #eff0f1;
}

QGroupBox
{
    border: 0.1ex solid #76797c;
    border-radius: 0.2ex;
    padding-top: 1ex;
    margin-top: 1ex;
}

QGroupBox::title
{
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 0.1ex;
    padding-right: 0.1ex;
    margin-top: -0.7ex;
}

QAbstractScrollArea
{
    border-radius: 0.2ex;
    border: 0.1ex solid #76797c;
    background-color: transparent;
}

QScrollBar:horizontal
{
    height: 1.5ex;
    margin: 0.3ex 1.5ex 0.3ex 1.5ex;
    border: 0.1ex transparent #2A2929;
    border-radius: 0.4ex;
    background-color: #2A2929;
}

QScrollBar::handle:horizontal
{
    background-color: #3daee9;
    min-width: 0.5ex;
    border-radius: 0.4ex;
}

QScrollBar::add-line:horizontal
{
    margin: 0px 0.3ex 0px 0.3ex;
    border-image: url(:/dark/right_arrow_disabled.svg);
    width: 1ex;
    height: 1ex;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal
{
    margin: 0ex 0.3ex 0ex 0.3ex;
    border-image: url(:/dark/left_arrow_disabled.svg);
    width: 1ex;
    height: 1ex;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,
QScrollBar::add-line:horizontal:on
{
    border-image: url(:/dark/right_arrow.svg);
    width: 1ex;
    height: 1ex;
    subcontrol-position: right;
    subcontrol-origin: margin;
}


QScrollBar::sub-line:horizontal:hover,
QScrollBar::sub-line:horizontal:on
{
    border-image: url(:/dark/left_arrow.svg);
    width: 1ex;
    height: 1ex;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal
{
    background: none;
}


QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal
{
    background: none;
}

QScrollBar:vertical
{
    background-color: #2A2929;
    width: 1.5ex;
    margin: 1.5ex 0.3ex 1.5ex 0.3ex;
    border: 0.1ex transparent #2A2929;
    border-radius: 0.4ex;
}

QScrollBar::handle:vertical
{
    background-color: #3daee9;
    min-height: 0.5ex;
    border-radius: 0.4ex;
}

QScrollBar::sub-line:vertical
{
    margin: 0.3ex 0ex 0.3ex 0ex;
    border-image: url(:/dark/up_arrow_disabled.svg);
    height: 1ex;
    width: 1ex;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical
{
    margin: 0.3ex 0ex 0.3ex 0ex;
    border-image: url(:/dark/down_arrow_disabled.svg);
    height: 1ex;
    width: 1ex;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,
QScrollBar::sub-line:vertical:on
{

    border-image: url(:/dark/up_arrow.svg);
    height: 1ex;
    width: 1ex;
    subcontrol-position: top;
    subcontrol-origin: margin;
}


QScrollBar::add-line:vertical:hover,
QScrollBar::add-line:vertical:on
{
    border-image: url(:/dark/down_arrow.svg);
    height: 1ex;
    width: 1ex;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
    background: none;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
    background: none;
}

QTextEdit
{
    background-color: #232629;
    color: #eff0f1;
    border: 0.1ex solid #76797c;
}

QPlainTextEdit
{
    background-color: #232629;;
    color: #eff0f1;
    border-radius: 0.2ex;
    border: 0.1ex solid #76797c;
}

QHeaderView::section
{
    background-color: #76797c;
    color: #eff0f1;
    padding: 0.5ex;
    border: 0.1ex solid #76797c;
}

QSizeGrip
{
    border-image: url(:/dark/sizegrip.svg);
    width: 1.2ex;
    height: 1.2ex;
}

QMainWindow::separator
{
    background-color: #31363b;
    color: white;
    padding-left: 0.4ex;
    spacing: 0.2ex;
    border: 0.1ex dashed #76797c;
}

QMainWindow::separator:hover
{

    background-color: #787876;
    color: white;
    padding-left: 0.4ex;
    border: 0.1ex solid #76797c;
    spacing: 0.2ex;
}

QMenu::separator
{
    height: 0.1ex;
    background-color: #76797c;
    color: white;
    padding-left: 0.4ex;
    margin-left: 1ex;
    margin-right: 0.5ex;
}

QFrame[frameShape="2"],  /* QFrame::Panel == 0x0003 */
QFrame[frameShape="3"],  /* QFrame::WinPanel == 0x0003 */
QFrame[frameShape="4"],  /* QFrame::HLine == 0x0004 */
QFrame[frameShape="5"],  /* QFrame::VLine == 0x0005 */
QFrame[frameShape="6"]  /* QFrame::StyledPanel == 0x0006 */
{
    border-width: 0.1ex;
    padding: 0.1ex;
    border-style: solid;
    border-color: #31363b;
    background-color: #76797c;
    border-radius: 0.5ex;
}

QStackedWidget
{
    border: 0.1ex transparent black;
}

QToolBar
{
    border: 0.1ex transparent #393838;
    background: 0.1ex solid #31363b;
    font-weight: bold;
}

QToolBar::handle:horizontal
{
    border-image: url(:/dark/hmovetoolbar.svg);
    width = 1.6ex;
    height = 6.4ex;
}

QToolBar::handle:vertical
{
    border-image: url(:/dark/vmovetoolbar.svg);
    width = 5.4ex;
    height = 1ex;
}

QToolBar::separator:horizontal
{
    border-image: url(:/dark/hsepartoolbar.svg);
    width = 0.7ex;
    height = 6.3ex;
}

QToolBar::separator:vertical
{
    border-image: url(:/dark/vsepartoolbars.svg);
    width = 6.3ex;
    height = 0.7ex;
}

QPushButton
{
    color: #eff0f1;
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #3b4045, stop: 0.5 #31363b);
    border-width: 0.1ex;
    border-color: #76797c;
    border-style: solid;
    padding: 0.5ex;
    border-radius: 0.2ex;
    outline: none;
}

QPushButton:disabled
{
    background-color: #31363b;
    border-width: 0.1ex;
    border-color: #454545;
    border-style: solid;
    padding-top: 0.5ex;
    padding-bottom: 0.5ex;
    padding-left: 1ex;
    padding-right: 1ex;
    border-radius: 0.2ex;
    color: #454545;
}

QPushButton:focus
{
    color: white;
}

QPushButton:pressed
{
    background-color: #31363b;
    padding-top: -1.5ex;
    padding-bottom: -1.7ex;
}

QComboBox
{
    selection-background-color: #3daee9;
    border-style: solid;
    border: 0.1ex solid #76797c;
    border-radius: 0.2ex;
    padding: 0.5ex;
    min-width: 7.5ex;
}

QPushButton:checked
{
    background-color: #76797c;
    border-color: #6A6969;
}

QPushButton:hover
{
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #454a4f, stop: 0.5 #3b4045);
    border: 0.1ex solid #3daee9;
    color: #eff0f1;
}

QPushButton:checked:hover
{
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #808386, stop: 0.5 #76797c);
    border: 0.1ex solid #3daee9;
    color: #eff0f1;
}

QComboBox:hover,
QAbstractSpinBox:hover,
QLineEdit:hover,
QTextEdit:hover,
QPlainTextEdit:hover,
QAbstractView:hover,
QTreeView:hover
{
    border: 0.1ex solid #3daee9;
    color: #eff0f1;
}

QComboBox:hover:pressed,
QPushButton:hover:pressed,
QAbstractSpinBox:hover:pressed,
QLineEdit:hover:pressed,
QTextEdit:hover:pressed,
QPlainTextEdit:hover:pressed,
QAbstractView:hover:pressed,
QTreeView:hover:pressed
{
    background-color: #31363b;
}

QComboBox:on
{
    padding-top: 0.3ex;
    padding-left: 0.4ex;
    selection-background-color: #4a4a4a;
}

QComboBox QAbstractItemView
{
    background-color: #232629;
    border-radius: 0.2ex;
    border: 0.1ex solid #76797c;
    selection-background-color: #3daee9;
}

QComboBox::drop-down
{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 1.5ex;

    border-left-width: 0ex;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 0.3ex;
    border-bottom-right-radius: 0.3ex;
}

QComboBox::down-arrow
{
    border-image: url(:/dark/down_arrow_disabled.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QComboBox::down-arrow:on,
QComboBox::down-arrow:hover,
QComboBox::down-arrow:focus
{
    border-image: url(:/dark/down_arrow.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QAbstractSpinBox
{
    padding: 0.5ex;
    border: 0.1ex solid #76797c;
    background-color: #232629;
    color: #eff0f1;
    border-radius: 0.2ex;
    min-width: 7.5ex;
}

QAbstractSpinBox:up-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: center right;
}

QAbstractSpinBox:down-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: center left;
}

QAbstractSpinBox::up-arrow,
QAbstractSpinBox::up-arrow:disabled,
QAbstractSpinBox::up-arrow:off
{
    border-image: url(:/dark/up_arrow_disabled.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QAbstractSpinBox::up-arrow:hover
{
    border-image: url(:/dark/up_arrow.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QAbstractSpinBox::down-arrow,
QAbstractSpinBox::down-arrow:disabled,
QAbstractSpinBox::down-arrow:off
{
    border-image: url(:/dark/down_arrow_disabled.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QAbstractSpinBox::down-arrow:hover
{
    border-image: url(:/dark/down_arrow.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QLabel
{
    border: 0ex solid black;
}

/* BORDERS */
QTabWidget::pane
{
    padding: 0.5ex;
    margin: 0.1ex;
}

QTabWidget::pane:top
{
    border: 0.1ex solid #76797c;
    top: -0.1ex;
}

QTabWidget::pane:bottom
{
    border: 0.1ex solid #76797c;
    bottom: -0.1ex;
}

QTabWidget::pane:left
{
    border: 0.1ex solid #76797c;
    right: -0.1ex;
}

QTabWidget::pane:right
{
    border: 0.1ex solid #76797c;
    left: -0.1ex;
}


QTabBar
{
    qproperty-drawBase: 0;
    left: 0.5ex; /* move to the right by 0.5ex */
    border-radius: 0.3ex;
}

QTabBar:focus
{
    border: 0ex transparent black;
}

QTabBar::close-button
{
    border-image: url(:/dark/close.svg);
    background: transparent;
}

QTabBar::close-button:hover
{
    border-image: url(:/dark/close-hover.svg);
    width: 1.2ex;
    height: 1.2ex;
    background: transparent;
}

QTabBar::close-button:pressed
{
    border-image: url(:/dark/close-pressed.svg);
    width: 1.2ex;
    height: 1.2ex;
    background: transparent;
}

/* TOP TABS */
QTabBar::tab:top
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-top: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    min-width: 50px;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:last,
QTabBar::tab:top:only-one
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-right: 0.1ex solid #76797c;
    border-top: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    min-width: 50px;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:first:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
    border-left: 0.1ex solid #76797c;
}

QTabBar::tab:top:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
}

/* BOTTOM TABS */

QTabBar::tab:bottom
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-bottom: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-width: 50px;
}

QTabBar::tab:bottom:last,
QTabBar::tab:bottom:only-one
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-right: 0.1ex solid #76797c;
    border-bottom: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-width: 50px;
}

QTabBar::tab:bottom:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #76797c;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
}

QTabBar::tab:bottom:first:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:bottom:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
    border-left: 0.1ex solid #76797c;
}

QTabBar::tab:bottom:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
}

/* LEFT TABS */
QTabBar::tab:left
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-right: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-height: 50px;
}

QTabBar::tab:left:last,
QTabBar::tab:left:only-one
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-bottom: 0.1ex solid #76797c;
    border-right: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-height: 50px;
}

QTabBar::tab:left:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
}

QTabBar::tab:left:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
    border-top: 0.1ex solid #76797c;
}

QTabBar::tab:left:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
}

/* RIGHT TABS */
QTabBar::tab:right
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-left: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
    min-height: 50px;
}

QTabBar::tab:right:last,
QTabBar::tab:right:only-one
{
    color: #eff0f1;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-bottom: 0.1ex solid #76797c;
    border-left: 0.1ex solid #76797c;
    background-color: #31363b;
    padding: 0.5ex;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
    min-height: 50px;
}

QTabBar::tab:right:!selected
{
    color: #eff0f1;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #76797c;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
}

QTabBar::tab:right:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
    border-top: 0.1ex solid #76797c;
}

QTabBar::tab:right:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    border: 0.1ex rgba(61, 173, 232, 0.2);
}

QTabBar QToolButton::right-arrow:enabled
{
    border-image: url(:/dark/right_arrow.svg);
}

QTabBar QToolButton::left-arrow:enabled
{
    border-image: url(:/dark/left_arrow.svg);
}

QTabBar QToolButton::right-arrow:disabled
{
    border-image: url(:/dark/right_arrow_disabled.svg);
}

QTabBar QToolButton::left-arrow:disabled
{
    border-image: url(:/dark/left_arrow_disabled.svg);
}

QDockWidget
{
    background: #31363b;
    border: 0.1ex solid #403F3F;
    titlebar-close-icon: url(:/dark/transparent.svg);
    titlebar-normal-icon: url(:/dark/transparent.svg);
}

QDockWidget::close-button,
QDockWidget::float-button
{
    border: 0.1ex solid transparent;
    border-radius: 0.2ex;
    background: transparent;
}

QDockWidget::float-button
{
    border-image: url(:/dark/undock.svg);
}

QDockWidget::float-button:hover
{
    border-image: url(:/dark/undock-hover.svg) ;
}

QDockWidget::close-button
{
    border-image: url(:/dark/close.svg) ;
}

QDockWidget::close-button:hover
{
    border-image: url(:/dark/close-hover.svg) ;
}

QDockWidget::close-button:pressed
{
    border-image: url(:/dark/close-pressed.svg) ;
}

QTreeView,
QListView
{
    border: 0.1ex solid #76797c;
    background-color: #232629;
}

QTreeView::branch:has-siblings:!adjoins-item
{
    border-image: url(:/dark/stylesheet-vline.svg) 0;
}

QTreeView::branch:has-siblings:adjoins-item
{
    border-image: url(:/dark/stylesheet-branch-more.svg) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item
{
    border-image: url(:/dark/stylesheet-branch-end.svg) 0;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings
{
    border-image: url(:/dark/stylesheet-branch-end-closed.svg) 0;
    image: url(:/dark/branch_closed.svg);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings
{
    border-image: url(:/dark/stylesheet-branch-end-open.svg) 0;
    image: url(:/dark/branch_open.svg);
}

/*
QTreeView::branch:has-siblings:!adjoins-item {
        background: cyan;
}

QTreeView::branch:has-siblings:adjoins-item {
        background: red;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        background: blue;
}

QTreeView::branch:closed:has-children:has-siblings {
        background: pink;
}

QTreeView::branch:has-children:!has-siblings:closed {
        background: gray;
}

QTreeView::branch:open:has-children:has-siblings {
        background: magenta;
}

QTreeView::branch:open:has-children:!has-siblings {
        background: green;
}
*/

QTableView::item,
QListView::item,
QTreeView::item
{
    padding: 0.3ex;
}

QTableView::item:!selected:hover,
QListView::item:!selected:hover,
QTreeView::item:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.2);
    outline: 0;
    color: #eff0f1;
    padding: 0.3ex;
}


QSlider::groove:horizontal
{
    border: 0.1ex solid #31363b;
    height: 0.4ex;
    background: #565a5e;
    margin: 0ex;
    border-radius: 0.2ex;
}

QSlider::handle:horizontal
{
    background: #232629;
    border: 0.1ex solid #626568;
    width: 1.6ex;
    height: 1.6ex;
    margin: -0.8ex 0;
    border-radius: 0.9ex;
}

QSlider::groove:vertical
{
    border: 0.1ex solid #31363b;
    width: 0.4ex;
    background: #565a5e;
    margin: 0ex;
    border-radius: 0.3ex;
}

QSlider::handle:vertical
{
    background: #232629;
    border: 0.1ex solid #626568;
    width: 1.6ex;
    height: 1.6ex;
    margin: 0 -0.8ex;
    border-radius: 0.9ex;
}

QSlider::handle:horizontal:hover,
QSlider::handle:horizontal:focus,
QSlider::handle:vertical:hover,
QSlider::handle:vertical:focus
{
    border: 0.1ex solid #3daee9;
}

QSlider::sub-page:horizontal,
QSlider::add-page:vertical
{
    background: #3daee9;
    border-radius: 0.3ex;
}

QSlider::add-page:horizontal,
QSlider::sub-page:vertical
{
    background: #626568;
    border-radius: 0.3ex;
}

QToolButton
{
    background-color: transparent;
    border: 0.1ex solid #76797c;
    border-radius: 0.2ex;
    margin: 0.3ex;
    padding: 0.5ex;
}

QToolButton[popupMode="1"]  /* only for MenuButtonPopup */
{
    padding-right: 2ex; /* make way for the popup button */
}

QToolButton[popupMode="2"]  /* only for InstantPopup */
{
    padding-right: 1ex; /* make way for the popup button */
}

QToolButton::menu-indicator
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
    top: -0.7ex;
    left: -0.2ex;
}

QToolButton::menu-arrow
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
}

QToolButton:hover,
QToolButton::menu-button:hover
{
    background-color: transparent;
    border: 0.1ex solid #3daee9;
}

QToolButton:checked,
QToolButton:pressed,
QToolButton::menu-button:pressed
{
    background-color: #3daee9;
    border: 0.1ex solid #3daee9;
    padding: 0.5ex;
}

QToolButton::menu-button
{
    border: 0.1ex solid #76797c;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    /* 1ex width + 0.4ex for border + no text = 2ex allocated above */
    width: 1ex;
    padding: 0.5ex;
    outline: none;
}

QToolButton::menu-arrow:open
{
    border: 0.1ex solid #76797c;
}

QPushButton::menu-indicator
{
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
    left: 0.8ex;
}

QTableView
{
    border: 0.1ex solid #76797c;
    gridline-color: #31363b;
    background-color: #232629;
}


QTableView,
QHeaderView
{
    border-radius: 0px;
}

QTableView::item:pressed,
QListView::item:pressed,
QTreeView::item:pressed
{
    background: #3daee9;
    color: #eff0f1;
}

QTableView::item:selected:active,
QTreeView::item:selected:active,
QListView::item:selected:active
{
    background: #3daee9;
    color: #eff0f1;
}

QListView::item:selected:hover,
QTreeView::item:selected:hover
{
    background-color: #47b8f3;
    color: #eff0f1;
}

QHeaderView
{
    background-color: #31363b;
    border: 0.1ex transparent;
    border-radius: 0px;
    margin: 0px;
    padding: 0px;

}

QHeaderView::section
{
    background-color: #31363b;
    color: #eff0f1;
    padding: 0.5ex;
    border: 0.1ex solid #76797c;
    border-radius: 0px;
    text-align: center;
}

QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-top: 0.1ex solid #76797c;
}

QHeaderView::section::vertical
{
    border-top: transparent;
}

QHeaderView::section::horizontal::first,
QHeaderView::section::horizontal::only-one
{
    border-left: 0.1ex solid #76797c;
}

QHeaderView::section::horizontal
{
    border-left: transparent;
}


QHeaderView::section:checked
{
    color: white;
    background-color: #334e5e;
}

 /* style the sort indicator */
QHeaderView::down-arrow
{
    image: url(:/dark/down_arrow.svg);
}

QHeaderView::up-arrow
{
    image: url(:/dark/up_arrow.svg);
}

QTableCornerButton::section
{
    background-color: #31363b;
    border: 0.1ex transparent #76797c;
    border-radius: 0px;
}

QToolBox
{
    padding: 0.5ex;
    border: 0.1ex transparent black;
}

QToolBox:selected
{
    background-color: #31363b;
    border-color: #3daee9;
}

QToolBox:hover
{
    border-color: #3daee9;
}

QStatusBar::item
{
    border: 0px transparent dark;
}

QFrame[height="3"],
QFrame[width="3"]
{
    background-color: #76797c;
}

QSplitter::handle
{
    border: 0.1ex dashed #76797c;
}

QSplitter::handle:hover
{
    background-color: #787876;
    border: 0.1ex solid #76797c;
}

QSplitter::handle:horizontal
{
    width: 0.1ex;
}

QSplitter::handle:vertical
{
    height: 0.1ex;
}

QProgressBar:horizontal
{
    background-color: #626568;
    border: 0.1ex solid #31363b;
    border-radius: 0.3ex;
    height: 0.5ex;
    text-align: right;
    margin-top: 0.5ex;
    margin-bottom: 0.5ex;
    margin-right: 5ex;
    padding: 0px;
}

QProgressBar::chunk:horizontal
{
    background-color: #3daee9;
    border: 0.1ex transparent;
    border-radius: 0.3ex;
}

QSpinBox,
QDoubleSpinBox
{
    padding-right: 1.5ex;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button
{
    subcontrol-origin: content;
    subcontrol-position: right top;

    width: 1.6ex;
    border-width: 0.1ex;
}

QSpinBox::up-arrow,
QDoubleSpinBox::up-arrow
{
    border-image: url(:/dark/up_arrow.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QSpinBox::up-arrow:hover,
QSpinBox::up-arrow:pressed,
QDoubleSpinBox::up-arrow:hover,
QDoubleSpinBox::up-arrow:pressed
{
    border-image: url(:/dark/up_arrow-hover.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QSpinBox::up-arrow:disabled,
QSpinBox::up-arrow:off,
QDoubleSpinBox::up-arrow:disabled,
QDoubleSpinBox::up-arrow:off
{
   border-image: url(:/dark/up_arrow_disabled.svg);
}

QSpinBox::down-button,
QDoubleSpinBox::down-button
{
    subcontrol-origin: content;
    subcontrol-position: right bottom;

    width: 1.6ex;
    border-width: 0.1ex;
}

QSpinBox::down-arrow,
QDoubleSpinBox::down-arrow
{
    border-image: url(:/dark/down_arrow.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QSpinBox::down-arrow:hover,
QSpinBox::down-arrow:pressed,
QDoubleSpinBox::down-arrow:hover,
QDoubleSpinBox::down-arrow:pressed
{
    border-image: url(:/dark/down_arrow-hover.svg);
    width: 0.9ex;
    height: 0.6ex;
}

QSpinBox::down-arrow:disabled,
QSpinBox::down-arrow:off,
QDoubleSpinBox::down-arrow:disabled,
QDoubleSpinBox::down-arrow:off
{
   border-image: url(:/dark/down_arrow_disabled.svg);
}
        '''
        self.tabWidget.setStyleSheet(style2)
    def style3(self):
        style3='''/*
 * The MIT License (MIT)
 *
 * Copyright (c) <2013-2014> <Colin Duquesnoy>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

QProgressBar:horizontal {
    border: 1px solid #3A3939;
    text-align: center;
    padding: 1px;
    background: #201F1F;
}
QProgressBar::chunk:horizontal {
    background-color: qlineargradient(spread:reflect, x1:1, y1:0.545, x2:1, y2:0, stop:0 rgba(28, 66, 111, 255), stop:1 rgba(37, 87, 146, 255));
}

QToolTip
{
    border: 1px solid #3A3939;
    background-color: rgb(90, 102, 117);;
    color: white;
    padding: 1px;
    opacity: 200;
}

QWidget
{
    color: silver;
    background-color: #302F2F;
    selection-background-color:#3d8ec9;
    selection-color: black;
    background-clip: border;
    border-image: none;
    outline: 0;
}

QWidget:item:hover
{
    background-color: #78879b;
    color: black;
}

QWidget:item:selected
{
    background-color: #3d8ec9;
}

QCheckBox
{
    spacing: 5px;
    outline: none;
    color: #bbb;
    margin-bottom: 2px;
}

QCheckBox:disabled
{
    color: #777777;
}
QCheckBox::indicator,
QGroupBox::indicator
{
    width: 18px;
    height: 18px;
}
QGroupBox::indicator
{
    margin-left: 2px;
}

QCheckBox::indicator:unchecked,
QCheckBox::indicator:unchecked:hover,
QGroupBox::indicator:unchecked,
QGroupBox::indicator:unchecked:hover
{
    image: url(:/dark_blue/img/checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:focus,
QCheckBox::indicator:unchecked:pressed,
QGroupBox::indicator:unchecked:focus,
QGroupBox::indicator:unchecked:pressed
{
  border: none;
    image: url(:/dark_blue/img/checkbox_unchecked_focus.png);
}

QCheckBox::indicator:checked,
QCheckBox::indicator:checked:hover,
QGroupBox::indicator:checked,
QGroupBox::indicator:checked:hover
{
    image: url(:/dark_blue/img/checkbox_checked.png);
}

QCheckBox::indicator:checked:focus,
QCheckBox::indicator:checked:pressed,
QGroupBox::indicator:checked:focus,
QGroupBox::indicator:checked:pressed
{
  border: none;
    image: url(:/dark_blue/img/checkbox_checked_focus.png);
}

QCheckBox::indicator:indeterminate,
QCheckBox::indicator:indeterminate:hover,
QCheckBox::indicator:indeterminate:pressed
QGroupBox::indicator:indeterminate,
QGroupBox::indicator:indeterminate:hover,
QGroupBox::indicator:indeterminate:pressed
{
    image: url(:/dark_blue/img/checkbox_indeterminate.png);
}

QCheckBox::indicator:indeterminate:focus,
QGroupBox::indicator:indeterminate:focus
{
    image: url(:/dark_blue/img/checkbox_indeterminate_focus.png);
}

QCheckBox::indicator:checked:disabled,
QGroupBox::indicator:checked:disabled
{
    image: url(:/dark_blue/img/checkbox_checked_disabled.png);
}

QCheckBox::indicator:unchecked:disabled,
QGroupBox::indicator:unchecked:disabled
{
    image: url(:/dark_blue/img/checkbox_unchecked_disabled.png);
}

QRadioButton
{
    spacing: 5px;
    outline: none;
    color: #bbb;
    margin-bottom: 2px;
}

QRadioButton:disabled
{
    color: #777777;
}
QRadioButton::indicator
{
    width: 21px;
    height: 21px;
}

QRadioButton::indicator:unchecked,
QRadioButton::indicator:unchecked:hover
{
    image: url(:/dark_blue/img/radio_unchecked.png);
}

QRadioButton::indicator:unchecked:focus,
QRadioButton::indicator:unchecked:pressed
{
  border: none;
  outline: none;
    image: url(:/dark_blue/img/radio_unchecked_focus.png);
}

QRadioButton::indicator:checked,
QRadioButton::indicator:checked:hover
{
  border: none;
  outline: none;
    image: url(:/dark_blue/img/radio_checked.png);
}

QRadioButton::indicator:checked:focus,
QRadioButton::indicato::menu-arrowr:checked:pressed
{
  border: none;
  outline: none;
    image: url(:/dark_blue/img/radio_checked_focus.png);
}

QRadioButton::indicator:indeterminate,
QRadioButton::indicator:indeterminate:hover,
QRadioButton::indicator:indeterminate:pressed
{
        image: url(:/dark_blue/img/radio_indeterminate.png);
}

QRadioButton::indicator:checked:disabled
{
  outline: none;
  image: url(:/dark_blue/img/radio_checked_disabled.png);
}

QRadioButton::indicator:unchecked:disabled
{
    image: url(:/dark_blue/img/radio_unchecked_disabled.png);
}


QMenuBar
{
    background-color: #302F2F;
    color: silver;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #3A3939;
}

QMenuBar::item:pressed
{
    border: 1px solid #3A3939;
    background-color: #3d8ec9;
    color: black;
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #3A3939;
    color: silver;
    margin: 1px;
}

QMenu::icon
{
    margin: 1px;
}

QMenu::item
{
    padding: 2px 2px 2px 25px;
    margin-left: 5px;
    border: 1px solid transparent; /* reserve space for selection border */
}

QMenu::item:selected
{
    color: black;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 16px;
    height: 16px;
}

/* non-exclusive indicator = check box style indicator
   (see QActionGroup::setExclusive) */
QMenu::indicator:non-exclusive:unchecked {
    image: url(:/dark_blue/img/checkbox_unchecked.png);
}

QMenu::indicator:non-exclusive:unchecked:selected {
    image: url(:/dark_blue/img/checkbox_unchecked_disabled.png);
}

QMenu::indicator:non-exclusive:checked {
    image: url(:/dark_blue/img/checkbox_checked.png);
}

QMenu::indicator:non-exclusive:checked:selected {
    image: url(:/dark_blue/img/checkbox_checked_disabled.png);
}

/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:exclusive:unchecked {
    image: url(:/dark_blue/img/radio_unchecked.png);
}

QMenu::indicator:exclusive:unchecked:selected {
    image: url(:/dark_blue/img/radio_unchecked_disabled.png);
}

QMenu::indicator:exclusive:checked {
    image: url(:/dark_blue/img/radio_checked.png);
}

QMenu::indicator:exclusive:checked:selected {
    image: url(:/dark_blue/img/radio_checked_disabled.png);
}

QMenu::right-arrow {
    margin: 5px;
    image: url(:/dark_blue/img/right_arrow.png)
}


QWidget:disabled
{
    color: #808080;
    background-color: #302F2F;
}

QAbstractItemView
{
    alternate-background-color: #3A3939;
    color: silver;
    border: 1px solid 3A3939;
    border-radius: 2px;
    padding: 1px;
}

QWidget:focus, QMenuBar:focus
{
    border: 1px solid #78879b;
}

QTabWidget:focus, QCheckBox:focus, QRadioButton:focus, QSlider:focus
{
    border: none;
}

QLineEdit
{
    background-color: #201F1F;
    padding: 2px;
    border-style: solid;
    border: 1px solid #3A3939;
    border-radius: 2px;
    color: silver;
}

QGroupBox {
    border:1px solid #3A3939;
    border-radius: 2px;
    margin-top: 20px;
    background-color: #302F2F;
    color: silver;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 10px;
}

QAbstractScrollArea
{
    border-radius: 2px;
    border: 1px solid #3A3939;
    background-color: transparent;
}

QScrollBar:horizontal
{
    height: 15px;
    margin: 3px 15px 3px 15px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
    background-color: #2A2929;
}

QScrollBar::handle:horizontal
{
    background-color: #605F5F;
    min-width: 5px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal
{
    margin: 0px 3px 0px 3px;
    border-image: url(:/dark_blue/img/right_arrow_disabled.png);
    width: 10px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal
{
    margin: 0px 3px 0px 3px;
    border-image: url(:/dark_blue/img/left_arrow_disabled.png);
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
{
    border-image: url(:/dark_blue/img/right_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}


QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
{
    border-image: url(:/dark_blue/img/left_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
{
    background: none;
}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
    background: none;
}

QScrollBar:vertical
{
    background-color: #2A2929;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
}

QScrollBar::handle:vertical
{
    background-color: #605F5F;
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::sub-line:vertical
{
    margin: 3px 0px 3px 0px;
    border-image: url(:/dark_blue/img/up_arrow_disabled.png);
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical
{
    margin: 3px 0px 3px 0px;
    border-image: url(:/dark_blue/img/down_arrow_disabled.png);
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
{

    border-image: url(:/dark_blue/img/up_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}


QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
{
    border-image: url(:/dark_blue/img/down_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
    background: none;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
    background: none;
}

QTextEdit
{
    background-color: #201F1F;
    color: silver;
    border: 1px solid #3A3939;
}

QPlainTextEdit
{
    background-color: #201F1F;;
    color: silver;
    border-radius: 2px;
    border: 1px solid #3A3939;
}

QHeaderView::section
{
    background-color: #3A3939;
    color: silver;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QSizeGrip {
    image: url(:/dark_blue/img/sizegrip.png);
    width: 12px;
    height: 12px;
}

QMainWindow
{
    background-color: #302F2F;

}

QMainWindow::separator
{
    background-color: #302F2F;
    color: white;
    padding-left: 4px;
    spacing: 2px;
    border: 1px dashed #3A3939;
}

QMainWindow::separator:hover
{

    background-color: #787876;
    color: white;
    padding-left: 4px;
    border: 1px solid #3A3939;
    spacing: 2px;
}


QMenu::separator
{
    height: 1px;
    background-color: #3A3939;
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}


QFrame
{
    border-radius: 2px;
    border: 1px solid #444;
}

QFrame[frameShape="0"]
{
    border-radius: 2px;
    border: 1px transparent #444;
}

QStackedWidget
{
    background-color: #302F2F;
    border: 1px transparent black;
}

QToolBar {
    border: 1px transparent #393838;
    background: 1px solid #302F2F;
    font-weight: bold;
}

QToolBar::handle:horizontal {
    image: url(:/dark_blue/img/Hmovetoolbar.png);
}
QToolBar::handle:vertical {
    image: url(:/dark_blue/img/Vmovetoolbar.png);
}
QToolBar::separator:horizontal {
    image: url(:/dark_blue/img/Hsepartoolbar.png);
}
QToolBar::separator:vertical {
    image: url(:/dark_blue/img/Vsepartoolbars.png);
}

QPushButton
{
    color: silver;
    background-color: #302F2F;
    border-width: 2px;
    border-color: #4A4949;
    border-style: solid;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 4px;
    /* outline: none; */
    /* min-width: 40px; */
}

QPushButton:disabled
{
    background-color: #302F2F;
    border-width: 2px;
    border-color: #3A3939;
    border-style: solid;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 10px;
    padding-right: 10px;
    /*border-radius: 2px;*/
    color: #808080;
}

QPushButton:focus {
    background-color: #3d8ec9;
    color: white;
}

QComboBox
{
    selection-background-color: #3d8ec9;
    background-color: #201F1F;
    border-style: solid;
    border: 1px solid #3A3939;
    border-radius: 2px;
    padding: 2px;
    min-width: 75px;
}

QPushButton:checked{
    background-color: #4A4949;
    border-color: #6A6969;
}

QPushButton:hover {
    border: 2px solid #78879b;
    color: silver;
}

QComboBox:hover, QAbstractSpinBox:hover,QLineEdit:hover,QTextEdit:hover,QPlainTextEdit:hover,QAbstractView:hover,QTreeView:hover
{
    border: 1px solid #78879b;
    color: silver;
}

QComboBox:on
{
    background-color: #626873;
    padding-top: 3px;
    padding-left: 4px;
    selection-background-color: #4a4a4a;
}

QComboBox QAbstractItemView
{
    background-color: #201F1F;
    border-radius: 2px;
    border: 1px solid #444;
    selection-background-color: #3d8ec9;
    color: silver;
}

QComboBox::drop-down
{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 0px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow
{
    image: url(:/dark_blue/img/down_arrow_disabled.png);
}

QComboBox::down-arrow:on, QComboBox::down-arrow:hover,
QComboBox::down-arrow:focus
{
    image: url(:/dark_blue/img/down_arrow.png);
}

QPushButton:pressed
{
    background-color: #484846;
}

QAbstractSpinBox {
    padding-top: 2px;
    padding-bottom: 2px;
    border: 1px solid #3A3939;
    background-color: #201F1F;
    color: silver;
    border-radius: 2px;
    min-width: 75px;
}

QAbstractSpinBox:up-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: top right;
}

QAbstractSpinBox:down-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: bottom right;
}

QAbstractSpinBox::up-arrow,QAbstractSpinBox::up-arrow:disabled,QAbstractSpinBox::up-arrow:off {
    image: url(:/dark_blue/img/up_arrow_disabled.png);
    width: 10px;
    height: 10px;
}
QAbstractSpinBox::up-arrow:hover
{
    image: url(:/dark_blue/img/up_arrow.png);
}


QAbstractSpinBox::down-arrow,QAbstractSpinBox::down-arrow:disabled,QAbstractSpinBox::down-arrow:off
{
    image: url(:/dark_blue/img/down_arrow_disabled.png);
    width: 10px;
    height: 10px;
}
QAbstractSpinBox::down-arrow:hover
{
    image: url(:/dark_blue/img/down_arrow.png);
}


QLabel
{
    border: 0px solid black;
}

QTabWidget{
    border: 1px transparent black;
}

QTabWidget::pane {
    border: 1px solid #444;
    border-radius: 3px;
    padding: 3px;
}

QTabBar
{
    qproperty-drawBase: 0;
    left: 5px; /* move to the right by 5px */
}

QTabBar:focus
{
    border: 0px transparent black;
}

QTabBar::close-button  {
    image: url(:/dark_blue/img/close.png);
    background: transparent;
}

QTabBar::close-button:hover
{
    image: url(:/dark_blue/img/close-hover.png);
    background: transparent;
}

QTabBar::close-button:pressed {
    image: url(:/dark_blue/img/close-pressed.png);
    background: transparent;
}

/* TOP TABS */
QTabBar::tab:top {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-bottom: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
}

QTabBar::tab:top:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-bottom: 1px transparent #4A4949;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

QTabBar::tab:top:!selected:hover {
    background-color: #48576b;
}

/* BOTTOM TABS */
QTabBar::tab:bottom {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-top: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-bottom-left-radius: 2px;
    border-bottom-right-radius: 2px;
}

QTabBar::tab:bottom:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-top: 1px transparent #4A4949;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}

QTabBar::tab:bottom:!selected:hover {
    background-color: #78879b;
}

/* LEFT TABS */
QTabBar::tab:left {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-left: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-right-radius: 2px;
    border-bottom-right-radius: 2px;
}

QTabBar::tab:left:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-right: 1px transparent #4A4949;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}

QTabBar::tab:left:!selected:hover {
    background-color: #48576b;
}


/* RIGHT TABS */
QTabBar::tab:right {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-right: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
}

QTabBar::tab:right:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-right: 1px transparent #4A4949;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
}

QTabBar::tab:right:!selected:hover {
    background-color: #48576b;
}

QTabBar QToolButton::right-arrow:enabled {
     image: url(:/dark_blue/img/right_arrow.png);
 }

 QTabBar QToolButton::left-arrow:enabled {
     image: url(:/dark_blue/img/left_arrow.png);
 }

QTabBar QToolButton::right-arrow:disabled {
     image: url(:/dark_blue/img/right_arrow_disabled.png);
 }

 QTabBar QToolButton::left-arrow:disabled {
     image: url(:/dark_blue/img/left_arrow_disabled.png);
 }


QDockWidget {
    border: 1px solid #403F3F;
    titlebar-close-icon: url(:/dark_blue/img/close.png);
    titlebar-normal-icon: url(:/dark_blue/img/undock.png);
}

QDockWidget::close-button, QDockWidget::float-button {
    border: 1px solid transparent;
    border-radius: 2px;
    background: transparent;
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background: rgba(255, 255, 255, 10);
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
    padding: 1px -1px -1px 1px;
    background: rgba(255, 255, 255, 10);
}

QTreeView, QListView, QTextBrowser, AtLineEdit, AtLineEdit::hover {
    border: 1px solid #444;
    background-color: silver;
    border-radius: 3px;
    margin-left: 3px;
    color: black;
}

QTreeView:branch:selected, QTreeView:branch:hover {
    background: url(:/dark_blue/img/transparent.png);
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(:/dark_blue/img/transparent.png);
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(:/dark_blue/img/transparent.png);
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(:/dark_blue/img/transparent.png);
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    image: url(:/dark_blue/img/branch_closed.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
    image: url(:/dark_blue/img/branch_open.png);
}

QTreeView::branch:has-children:!has-siblings:closed:hover,
QTreeView::branch:closed:has-children:has-siblings:hover {
    image: url(:/dark_blue/img/branch_closed-on.png);
    }

QTreeView::branch:open:has-children:!has-siblings:hover,
QTreeView::branch:open:has-children:has-siblings:hover  {
    image: url(:/dark_blue/img/branch_open-on.png);
    }

QListView::item:!selected:hover, QListView::item:!selected:hover, QTreeView::item:!selected:hover  {
    background: rgba(0, 0, 0, 0);
    outline: 0;
    color: #FFFFFF
}

QListView::item:selected:hover, QListView::item:selected:hover, QTreeView::item:selected:hover  {
    background: #3d8ec9;
    color: #FFFFFF;
}

QSlider::groove:horizontal {
    border: 1px solid #3A3939;
    height: 8px;
    background: #201F1F;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 2px;
}

QSlider::groove:vertical {
    border: 1px solid #3A3939;
    width: 8px;
    background: #201F1F;
    margin: 0 0px;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 silver,
    stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: 0 -4px;
    border-radius: 2px;
}

QToolButton {
    /*  background-color: transparent; */
    border: 2px transparent #4A4949;
    border-radius: 4px;
    background-color: dimgray;
    margin: 2px;
    padding: 2px;
}

QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
 padding-right: 20px; /* make way for the popup button */
 border: 2px transparent #4A4949;
 border-radius: 4px;
}

QToolButton[popupMode="2"] { /* only for InstantPopup */
 padding-right: 10px; /* make way for the popup button */
 border: 2px transparent #4A4949;
}


QToolButton:hover, QToolButton::menu-button:hover {
    border: 2px solid #78879b;
}

QToolButton:checked, QToolButton:pressed,
    QToolButton::menu-button:pressed {
    background-color: #4A4949;
    border: 2px solid #78879b;
}

/* the subcontrol below is used only in the InstantPopup or DelayedPopup mode */
QToolButton::menu-indicator {
    image: url(:/dark_blue/img/down_arrow.png);
    top: -7px; left: -2px; /* shift it a bit */
}

/* the subcontrols below are used only in the MenuButtonPopup mode */
QToolButton::menu-button {
    border: 1px transparent #4A4949;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    /* 16px width + 4px for border = 20px allocated above */
    width: 16px;
    outline: none;
}

QToolButton::menu-arrow {
    image: url(:/dark_blue/img/down_arrow.png);
}

QToolButton::menu-arrow:open {
    top: 1px; left: 1px; /* shift it a bit */
    border: 1px solid #3A3939;
}

QPushButton::menu-indicator  {
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
    left: 4px;
}

QTableView
{
    border: 1px solid #444;
    gridline-color: #6c6c6c;
    background-color: #201F1F;
}


QTableView, QHeaderView
{
    border-radius: 0px;
}

QTableView::item:pressed, QListView::item:pressed, QTreeView::item:pressed  {
    background: #78879b;
    color: #FFFFFF;
}

QTableView::item:selected:active, QTreeView::item:selected:active, QListView::item:selected:active  {
    background: #3d8ec9;
    color: #FFFFFF;
}


QHeaderView
{
    border: 1px transparent;
    border-radius: 2px;
    margin: 0px;
    padding: 0px;
}

QHeaderView::section  {
    background-color: #3A3939;
    color: silver;
    padding: 4px;
    border: 1px solid #6c6c6c;
    border-radius: 0px;
    text-align: center;
}

QHeaderView::section::vertical::first, QHeaderView::section::vertical::only-one
{
    border-top: 1px solid #6c6c6c;
}

QHeaderView::section::vertical
{
    border-top: transparent;
}

QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one
{
    border-left: 1px solid #6c6c6c;
}

QHeaderView::section::horizontal
{
    border-left: transparent;
}


QHeaderView::section:checked
 {
    color: white;
    background-color: #5A5959;
 }

 /* style the sort indicator */
QHeaderView::down-arrow {
    image: url(:/dark_blue/img/down_arrow.png);
}

QHeaderView::up-arrow {
    image: url(:/dark_blue/img/up_arrow.png);
}


QTableCornerButton::section {
    background-color: #3A3939;
    border: 1px solid #3A3939;
    border-radius: 2px;
}

QToolBox  {
    padding: 3px;
    border: 1px transparent black;
}

QToolBox::tab {
    color: #b1b1b1;
    background-color: #302F2F;
    border: 1px solid #4A4949;
    border-bottom: 1px transparent #302F2F;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

 QToolBox::tab:selected { /* italicize selected tabs */
    font: italic;
    background-color: #302F2F;
    border-color: #3d8ec9;
 }

QStatusBar::item {
    border: 1px solid #3A3939;
    border-radius: 2px;
 }


QFrame[height="3"], QFrame[width="3"] {
    background-color: #AAA;
}


QSplitter::handle {
    border: 1px dashed #3A3939;
}

QSplitter::handle:hover {
    background-color: #787876;
    border: 1px solid #3A3939;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

QListWidget {
    background-color: silver;
    border-radius: 5px;
    margin-left: 5px;
}

QListWidget::item {
    color: black;
}

QMessageBox {
    messagebox-critical-icon	: url(:/dark_blue/img/critical.png);
    messagebox-information-icon	: url(:/dark_blue/img/information.png);
    messagebox-question-icon	: url(:/dark_blue/img/question.png);
    messagebox-warning-icon:    : url(:/dark_blue/img/warning.png);
}

ColorButton::enabled {
    border-radius: 0px;
    border: 1px solid #444444;
}

ColorButton::disabled {
    border-radius: 0px;
    border: 1px solid #AAAAAA;
}
        '''
        self.tabWidget.setStyleSheet(style3)
    def style4(self):
        style4='''/*
Ubuntu Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Company: GTRONICK
Last updated: 09/10/2019 (dd/mm/yyyy), 12:31.
Available at: https://github.com/GTRONICK/QSS/blob/master/Ubuntu.qss
*/
QMainWindow {
	background-color:#f0f0f0;
}
QCheckBox {
	padding:2px;
}
QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	border-width:1px;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-color: rgb(255,150,60);
	background-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(190, 90, 50, 50), stop:1 rgba(250, 130, 40, 50));
}
QCheckBox::indicator:checked {
	border-radius:4px;
	border-style:solid;
	border-width:1px;
	border-color: rgb(246, 134, 86);
  	background-color:rgb(246, 134, 86)
}
QCheckBox::indicator:unchecked {
	border-radius:4px;
	border-style:solid;
	border-width:1px;
	border-color:rgb(246, 134, 86);
  	background-color:rgb(255,255,255);
}
QColorDialog {
	background-color:#f0f0f0;
}
QComboBox {
	color:rgb(81,72,65);
	background: #ffffff;
}
QComboBox:editable {
	background: #ffffff;
	color: rgb(81,72,65);
	selection-color:rgb(81,72,65);
	selection-background-color: #ffffff;
}
QComboBox QAbstractItemView {
	color:rgb(81,72,65);	
	background: #ffffff;
	selection-color: #ffffff;
	selection-background-color: rgb(246, 134, 86);
}
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
	color:  #1e1d23;	
	background: #ffffff;
}
QDateTimeEdit {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QDateEdit {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QDialog {
	background-color:#f0f0f0;
}
QDoubleSpinBox {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QFontComboBox {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QLabel {
	color:rgb(17,17,17);
}
QLineEdit {
	background-color:rgb(255,255,255);
	selection-background-color:rgb(236,116,64);
	color:rgb(17,17,17);
}
QMenuBar {
	color:rgb(223,219,210);
	background-color:rgb(65,64,59);
}
QMenuBar::item {
	padding-top:4px;
	padding-left:4px;
	padding-right:4px;
	color:rgb(223,219,210);
	background-color:rgb(65,64,59);
}
QMenuBar::item:selected {
	color:rgb(255,255,255);
	padding-top:2px;
	padding-left:2px;
	padding-right:2px;
	border-top-width:2px;
	border-left-width:2px;
	border-right-width:2px;
	border-top-right-radius:4px;
	border-top-left-radius:4px;
	border-style:solid;
	background-color:rgb(65,64,59);
	border-top-color: rgb(47,47,44);
	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(90, 87, 78, 255), stop:1 rgba(47,47,44, 255));
	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(90, 87, 78, 255), stop:1 rgba(47,47,44, 255));
}
QMenu {
	color:rgb(223,219,210);
	background-color:rgb(65,64,59);
}
QMenu::item {
	color:rgb(223,219,210);
	padding-left:20px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:10px;
}
QMenu::item:selected {
	color:rgb(255,255,255);
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(225, 108, 54, 255), stop:1 rgba(246, 134, 86, 255));
	border-style:solid;
	border-width:3px;
	padding-left:17px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	border-bottom-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(175,85,48,255), stop:1 rgba(236,114,67, 255));
	border-top-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
	border-right-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
	border-left-color:qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
}
QPlainTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color:transparent;
	color:rgb(17,17,17);
	selection-background-color:rgb(236,116,64);
}
QProgressBar {
	text-align: center;
	color: rgb(0, 0, 0);
	border-width: 1px; 
	border-radius: 10px;
	border-style: inset;
	border-color: rgb(150,150,150);
	background-color:rgb(221,221,219);
}
QProgressBar::chunk:horizontal {
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(225, 108, 54, 255), stop:1 rgba(246, 134, 86, 255));
	border-style: solid;
	border-radius:8px;
	border-width:1px;
	border-bottom-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(175,85,48,255), stop:1 rgba(236,114,67, 255));
	border-top-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
	border-right-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
	border-left-color:qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));
}
QPushButton{
	color:rgb(17,17,17);
	border-width: 1px;
	border-radius: 6px;
	border-bottom-color: rgb(150,150,150);
	border-right-color: rgb(165,165,165);
	border-left-color: rgb(165,165,165);
	border-top-color: rgb(180,180,180);
	border-style: solid;
	padding: 4px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));
}
QPushButton:hover{
	color:rgb(17,17,17);
	border-width: 1px;
	border-radius:6px;
	border-top-color: rgb(255,150,60);
	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));
	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));
	border-bottom-color: rgb(200,70,20);
	border-style: solid;
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));
}
QPushButton:default{
	color:rgb(17,17,17);
	border-width: 1px;
	border-radius:6px;
	border-top-color: rgb(255,150,60);
	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));
	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));
	border-bottom-color: rgb(200,70,20);
	border-style: solid;
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));
}
QPushButton:pressed{
	color:rgb(17,17,17);
	border-width: 1px;
	border-radius: 6px;
	border-width: 1px;
	border-top-color: rgba(255,150,60,200);
	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 200));
	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 200));
	border-bottom-color: rgba(200,70,20,200);
	border-style: solid;
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));
}
QPushButton:disabled{
	color:rgb(174,167,159);
	border-width: 1px;
	border-radius: 6px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(200, 200, 200, 255), stop:1 rgba(230, 230, 230, 255));
}
QRadioButton {
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: rgba(246, 134, 86, 255);
	color: #a9b7c6;
	background-color:rgba(246, 134, 86, 255);
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: rgb(246, 134, 86);
	color: #a9b7c6;
	background-color: transparent;
}
QScrollArea {
	color: #FFFFFF;
	background-color:#f0f0f0;
}
QSlider::groove {
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
}
QSlider::groove:horizontal {
	height: 5px;
	background: rgb(246, 134, 86);
}
QSlider::groove:vertical {
	width: 5px;
	background: rgb(246, 134, 86);
}
QSlider::handle:horizontal {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	width: 12px;
	margin: -5px 0;
	border-radius: 7px;
}
QSlider::handle:vertical {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	height: 12px;
	margin: 0 -5px;
	border-radius: 7px;
}
QSlider::add-page:horizontal {
 	background: white;
}
QSlider::add-page:vertical {
	background: white;
}
QSlider::sub-page:horizontal {
	background: rgb(246, 134, 86);
}
QSlider::sub-page:vertical {
  	background: rgb(246, 134, 86);
}
QStatusBar {
	color:rgb(81,72,65);
}
QSpinBox {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QScrollBar:horizontal {
	max-height: 20px;
	border: 1px transparent grey;
	margin: 0px 20px 0px 20px;
}
QScrollBar::handle:horizontal {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	border-radius: 7px;
	min-width: 25px;
}
QScrollBar::handle:horizontal:hover {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(255,150,60);
	border-radius: 7px;
	min-width: 25px;
}
QScrollBar::add-line:horizontal {
  	border: 1px solid;
  	border-color: rgb(207,207,207);
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-right-radius: 7px;
  	background: rgb(255, 255, 255);
  	width: 20px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:hover {
  	border: 1px solid;
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-right-radius: 7px;
  	border-color: rgb(255,150,60);
  	background: rgb(255, 255, 255);
  	width: 20px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:pressed {
  	border: 1px solid grey;
  	border-top-left-radius: 7px;
  	border-top-right-radius: 7px;
  	border-bottom-right-radius: 7px;
  	background: rgb(231,231,231);
  	width: 20px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
  	border: 1px solid;
  	border-color: rgb(207,207,207);
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-left-radius: 7px;
  	background: rgb(255, 255, 255);
  	width: 20px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:hover {
  	border: 1px solid;
  	border-color: rgb(255,150,60);
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-left-radius: 7px;
  	background: rgb(255, 255, 255);
  	width: 20px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:pressed {
  	border: 1px solid grey;
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-left-radius: 7px;
  	background: rgb(231,231,231);
  	width: 20px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::left-arrow:horizontal {
  	border: 1px transparent grey;
  	border-top-left-radius: 3px;
  	border-bottom-left-radius: 3px;
  	width: 6px;
  	height: 6px;
  	background: rgb(230,230,230);
}
QScrollBar::right-arrow:horizontal {
	border: 1px transparent grey;
	border-top-right-radius: 3px;
	border-bottom-right-radius: 3px;
  	width: 6px;
  	height: 6px;
 	background: rgb(230,230,230);
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
 	background: none;
} 
QScrollBar:vertical {
	max-width: 20px;
	border: 1px transparent grey;
	margin: 20px 0px 20px 0px;
}
QScrollBar::add-line:vertical {
	border: 1px solid;
	border-color: rgb(207,207,207);
	border-bottom-right-radius: 7px;
	border-bottom-left-radius: 7px;
	border-top-left-radius: 7px;
	background: rgb(255, 255, 255);
  	height: 20px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover {
  	border: 1px solid;
  	border-color: rgb(255,150,60);
  	border-bottom-right-radius: 7px;
  	border-bottom-left-radius: 7px;
  	border-top-left-radius: 7px;
  	background: rgb(255, 255, 255);
  	height: 20px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:pressed {
  	border: 1px solid grey;
  	border-bottom-left-radius: 7px;
  	border-bottom-right-radius: 7px;
  	border-top-left-radius: 7px;
  	background: rgb(231,231,231);
  	height: 20px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
  	border: 1px solid;
  	border-color: rgb(207,207,207);
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-left-radius: 7px;
  	background: rgb(255, 255, 255);
  	height: 20px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover {
  	border: 1px solid;
  	border-color: rgb(255,150,60);
  	border-top-right-radius: 7px;
  	border-top-left-radius: 7px;
  	border-bottom-left-radius: 7px;
	background: rgb(255, 255, 255);
  	height: 20px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:pressed {
  	border: 1px solid grey;
  	border-top-left-radius: 7px;
  	border-top-right-radius: 7px;
  	background: rgb(231,231,231);
 	height: 20px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
QScrollBar::handle:vertical {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	border-radius: 7px;
	min-height: 25px;
}
QScrollBar::handle:vertical:hover {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(255,150,60);
	border-radius: 7px;
	min-height: 25px;
}
QScrollBar::up-arrow:vertical {
	border: 1px transparent grey;
  	border-top-left-radius: 3px;
	border-top-right-radius: 3px;
  	width: 6px;
  	height: 6px;
  	background: rgb(230,230,230);
}
QScrollBar::down-arrow:vertical {
  	border: 1px transparent grey;
  	border-bottom-left-radius: 3px;
  	border-bottom-right-radius: 3px;
  	width: 6px;
  	height: 6px;
  	background: rgb(230,230,230);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  	background: none;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:rgb(247,246,246);
}
QTabWidget::pane {
	border-color: rgb(180,180,180);
	background-color:rgb(247,246,246);
	border-style: solid;
	border-width: 1px;
  	border-radius: 6px;
}
QTabBar::tab {
	padding-left:4px;
	padding-right:4px;
	padding-bottom:2px;
	padding-top:2px;
	color:rgb(81,72,65);
  	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(221,218,217,255), stop:1 rgba(240,239,238,255));
	border-style: solid;
	border-width: 1px;
  	border-top-right-radius:4px;
	border-top-left-radius:4px;
	border-top-color: rgb(180,180,180);
	border-left-color: rgb(180,180,180);
	border-right-color: rgb(180,180,180);
	border-bottom-color: transparent;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	background-color:rgb(247,246,246);
  	margin-left: 0px;
  	margin-right: 1px;
}
QTabBar::tab:!selected {
	margin-top: 1px;
	margin-right: 1px;
}
QTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color:transparent;
	color:rgb(17,17,17);
	selection-background-color:rgb(236,116,64);
}
QTimeEdit {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QToolBox {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QToolBox::tab {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
QToolBox::tab:selected {
	color:rgb(81,72,65);
	background-color: #ffffff;
}
        '''
        self.tabWidget.setStyleSheet(style4)
    def style5(self):
        style5='''QToolTip
{
     border: 1px solid black;
     background-color: #ffa02f;
     padding: 1px;
     border-radius: 3px;
     opacity: 100;
}

QWidget
{
    color: #b1b1b1;
    background-color: #323232;
}

QTreeView, QListView
{
    background-color: silver;
    margin-left: 5px;
}

QWidget:item:hover
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
    color: #000000;
}

QWidget:item:selected
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #ffaa00;
}

QMenuBar::item:pressed
{
    background: #444;
    border: 1px solid #000;
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:1 #212121,
        stop:0.4 #343434/*,
        stop:0.2 #343434,
        stop:0.1 #ffaa00*/
    );
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #000;
}

QMenu::item
{
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
    color: #000000;
}

QWidget:disabled
{
    color: #808080;
    background-color: #323232;
}

QAbstractItemView
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);
}

QWidget:focus
{
    /*border: 1px solid darkgray;*/
}

QLineEdit
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
    padding: 1px;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QPushButton
{
    color: #b1b1b1;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
    min-width: 40px;
}

QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}

QComboBox
{
    selection-background-color: #ffaa00;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QComboBox:hover,QPushButton:hover
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}


QComboBox:on
{
    padding-top: 3px;
    padding-left: 4px;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
    selection-background-color: #ffaa00;
}

QComboBox QAbstractItemView
{
    border: 2px solid darkgray;
    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QComboBox::drop-down
{
     subcontrol-origin: padding;
     subcontrol-position: top right;
     width: 15px;

     border-left-width: 0px;
     border-left-color: darkgray;
     border-left-style: solid; /* just a single line */
     border-top-right-radius: 3px; /* same radius as the QComboBox */
     border-bottom-right-radius: 3px;
 }

QComboBox::down-arrow
{
     image: url(:/dark_orange/img/down_arrow.png);
}

QGroupBox
{
    border: 1px solid darkgray;
    margin-top: 10px;
}

QGroupBox:focus
{
    border: 1px solid darkgray;
}

QTextEdit:focus
{
    border: 1px solid darkgray;
}

QScrollBar:horizontal {
     border: 1px solid #222222;
     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
     height: 7px;
     margin: 0px 16px 0 16px;
}

QScrollBar::handle:horizontal
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
      subcontrol-position: right;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
     subcontrol-position: left;
     subcontrol-origin: margin;
}

QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
      background: none;
}

QScrollBar:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
      width: 7px;
      margin: 16px 0 16px 0;
      border: 1px solid #222222;
}

QScrollBar::handle:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
      height: 14px;
      subcontrol-position: bottom;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);
      height: 14px;
      subcontrol-position: top;
      subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
      background: none;
}

QTextEdit
{
    background-color: #242424;
}

QPlainTextEdit
{
    background-color: #242424;
}

QHeaderView::section
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QCheckBox:disabled
{
color: #414141;
}

QDockWidget::title
{
    text-align: center;
    spacing: 3px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button, QDockWidget::float-button
{
    text-align: center;
    spacing: 1px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover
{
    background: #242424;
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
{
    padding: 1px -1px -1px 1px;
}

QMainWindow::separator
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    border: 1px solid #4c4c4c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QMainWindow::separator:hover
{

    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QToolBar::handle
{
     spacing: 3px; /* spacing between items in the tool bar */
     background: url(:/dark_orange/img/handle.png);
}

QMenu::separator
{
    height: 2px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}

QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk
{
    background-color: #d7801a;
    width: 2.15px;
    margin: 0.5px;
}

QTabBar::tab {
    color: #b1b1b1;
    border: 1px solid #444;
    border-bottom-style: none;
    background-color: #323232;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 2px;
    margin-right: -1px;
}

QTabWidget::pane {
    border: 1px solid #444;
    top: 1px;
}

QTabBar::tab:last
{
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
    border-top-right-radius: 3px;
}

QTabBar::tab:first:!selected
{
 margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */


    border-top-left-radius: 3px;
}

QTabBar::tab:!selected
{
    color: #b1b1b1;
    border-bottom-style: solid;
    margin-top: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);
}

QTabBar::tab:selected
{
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    margin-bottom: 0px;
}

QTabBar::tab:!selected:hover
{
    /*border-top: 2px solid #ffaa00;
    padding-bottom: 3px;*/
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);
}

QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    border-radius: 6px;
}

QRadioButton::indicator:checked
{
    background-color: qradialgradient(
        cx: 0.5, cy: 0.5,
        fx: 0.5, fy: 0.5,
        radius: 1.0,
        stop: 0.25 #ffaa00,
        stop: 0.3 #323232
    );
}

QCheckBox::indicator{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    width: 9px;
    height: 9px;
}

QRadioButton::indicator
{
    border-radius: 6px;
}

QRadioButton::indicator:hover, QCheckBox::indicator:hover
{
    border: 1px solid #ffaa00;
}

QCheckBox::indicator:checked
{
    image:url(:/dark_orange/img/checkbox.png);
}

QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
{
    border: 1px solid #444;
}


QSlider::groove:horizontal {
    border: 1px solid #3A3939;
    height: 8px;
    background: #201F1F;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 2px;
}

QSlider::groove:vertical {
    border: 1px solid #3A3939;
    width: 8px;
    background: #201F1F;
    margin: 0 0px;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 silver,
      stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: 0 -4px;
    border-radius: 2px;
}

QAbstractSpinBox {
    padding-top: 2px;
    padding-bottom: 2px;
    border: 1px solid darkgray;

    border-radius: 2px;
    min-width: 50px;
}'''
        self.tabWidget.setStyleSheet(style5)
    def style6(self):
        style6='''/*
Material Dark Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Inspired on https://github.com/jxfwinter/qt-material-stylesheet
Company: GTRONICK
Last updated: 04/12/2018, 15:00.
Available at: https://github.com/GTRONICK/QSS/blob/master/MaterialDark.qss
*/
QMainWindow {
	background-color:#1e1d23;
}
QDialog {
	background-color:#1e1d23;
}
QColorDialog {
	background-color:#1e1d23;
}
QTextEdit {
	background-color:#1e1d23;
	color: #a9b7c6;
}
QPlainTextEdit {
	selection-background-color:#007b50;
	background-color:#1e1d23;
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	color: #a9b7c6;
}
QPushButton{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QPushButton::default{
	border-style: inset;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-width: 1px;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QToolButton {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QToolButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 1px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 2px;
	background-color: #1e1d23;
}
QPushButton:pressed{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #37efba;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #808086;
	border-bottom-width: 2px;
	border-style: solid;
	color: #808086;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: #a9b7c6;
	background:#1e1d23;
	selection-background-color:#007b50;
	selection-color: #FFFFFF;
}
QLabel {
	color: #a9b7c6;
}
QLCDNumber {
	color: #37e6b4;
}
QProgressBar {
	text-align: center;
	color: rgb(240, 240, 240);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	background-color:#1e1d23;
}
QProgressBar::chunk {
	background-color: #04b97f;
	border-radius: 5px;
}
QMenuBar {
	background-color: #1e1d23;
}
QMenuBar::item {
	color: #a9b7c6;
  	spacing: 3px;
  	padding: 1px 4px;
  	background: #1e1d23;
}

QMenuBar::item:selected {
  	background:#1e1d23;
	color: #FFFFFF;
}
QMenu::item:selected {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: #04b97f;
	border-bottom-color: transparent;
	border-left-width: 2px;
	color: #FFFFFF;
	padding-left:15px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu::item {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding-left:17px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu{
	background-color:#1e1d23;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:#1e1d23;
}
QTabWidget::pane {
		border-color: rgb(77,77,77);
		background-color:#1e1d23;
		border-style: solid;
		border-width: 1px;
    	border-radius: 6px;
}
QTabBar::tab {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #808086;
	padding: 3px;
	margin-left:3px;
	background-color: #1e1d23;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-left: 3px;
	padding-bottom: 2px;
	margin-left:3px;
	background-color: #1e1d23;
}

QCheckBox {
	color: #a9b7c6;
	padding: 2px;
}
QCheckBox:disabled {
	color: #808086;
	padding: 2px;
}

QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: rgb(87, 97, 106);
	background-color:#1e1d23;
}
QCheckBox::indicator:checked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: #04b97f;
}
QCheckBox::indicator:unchecked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: transparent;
}
QRadioButton {
	color: #a9b7c6;
	background-color: #1e1d23;
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: #04b97f;
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: transparent;
}
QStatusBar {
	color:#027f7f;
}
QSpinBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDoubleSpinBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QTimeEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDateTimeEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDateEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QComboBox {
	color: #a9b7c6;	
	background: #1e1d23;
}
QComboBox:editable {
	background: #1e1d23;
	color: #a9b7c6;
	selection-background-color: #1e1d23;
}
QComboBox QAbstractItemView {
	color: #a9b7c6;	
	background: #1e1d23;
	selection-color: #FFFFFF;
	selection-background-color: #1e1d23;
}
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
	color: #a9b7c6;	
	background: #1e1d23;
}
QFontComboBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QToolBox {
	color: #a9b7c6;
	background-color: #1e1d23;
}
QToolBox::tab {
	color: #a9b7c6;
	background-color: #1e1d23;
}
QToolBox::tab:selected {
	color: #FFFFFF;
	background-color: #1e1d23;
}
QScrollArea {
	color: #FFFFFF;
	background-color: #1e1d23;
}
QSlider::groove:horizontal {
	height: 5px;
	background: #04b97f;
}
QSlider::groove:vertical {
	width: 5px;
	background: #04b97f;
}
QSlider::handle:horizontal {
	background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	width: 14px;
	margin: -5px 0;
	border-radius: 7px;
}
QSlider::handle:vertical {
	background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	height: 14px;
	margin: 0 -5px;
	border-radius: 7px;
}
QSlider::add-page:horizontal {
    background: white;
}
QSlider::add-page:vertical {
    background: white;
}
QSlider::sub-page:horizontal {
    background: #04b97f;
}
QSlider::sub-page:vertical {
    background: #04b97f;
}
        '''
        self.tabWidget.setStyleSheet(style6)
    def style7(self):
        style7='''/*
ElegantDark Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Company: GTRONICK
Last updated: 17/04/2018
Available at: https://github.com/GTRONICK/QSS/blob/master/ElegantDark.qss
*/
QMainWindow {
	background-color:rgb(82, 82, 82);
}
QTextEdit {
	background-color:rgb(42, 42, 42);
	color: rgb(0, 255, 0);
}
QPushButton{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}
QPushButton:hover{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-bottom-color: rgb(115, 115, 115);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(157, 157, 157, 255));
}
QPushButton:pressed{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(62, 62, 62, 255), stop:1 rgba(22, 22, 22, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}
QPushButton:disabled{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(0, 0, 0);
	padding: 2px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(57, 57, 57, 255), stop:1 rgba(77, 77, 77, 255));
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: rgb(255, 255, 255);
	background:rgb(100, 100, 100);
	selection-background-color: rgb(187, 187, 187);
	selection-color: rgb(60, 63, 65);
}
QLabel {
	color:rgb(255,255,255);	
}
QProgressBar {
	text-align: center;
	color: rgb(240, 240, 240);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	background-color:rgb(77,77,77);
}
QProgressBar::chunk {
	background-color: qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
	border-radius: 5px;
}
QMenuBar {
	background:rgb(82, 82, 82);
}
QMenuBar::item {
	color:rgb(223,219,210);
	spacing: 3px;
	padding: 1px 4px;
	background: transparent;
}

QMenuBar::item:selected {
	background:rgb(115, 115, 115);
}
QMenu::item:selected {
	color:rgb(255,255,255);
	border-width:2px;
	border-style:solid;
	padding-left:18px;
	padding-right:8px;
	padding-top:2px;
	padding-bottom:3px;
	background:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
}
QMenu::item {
	color:rgb(223,219,210);
	background-color:rgb(78,78,78);
	padding-left:20px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:10px;
}
QMenu{
	background-color:rgb(78,78,78);
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:rgb(247,246,246);
}
QTabWidget::pane {
		border-color: rgb(77,77,77);
		background-color:rgb(101,101,101);
		border-style: solid;
		border-width: 1px;
    	border-radius: 6px;
}
QTabBar::tab {
	padding:2px;
	color:rgb(250,250,250);
  	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
	border-style: solid;
	border-width: 2px;
  	border-top-right-radius:4px;
   border-top-left-radius:4px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
	border-bottom-color: rgb(101,101,101);
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	background-color:rgb(101,101,101);
  	margin-left: 0px;
  	margin-right: 1px;
}
QTabBar::tab:!selected {
    	margin-top: 1px;
		margin-right: 1px;
}
QCheckBox {
	color:rgb(223,219,210);
	padding: 2px;
}
QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: rgb(87, 97, 106);
	background-color:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 150), stop:1 rgba(93, 103, 113, 150));
}
QCheckBox::indicator:checked {
	border-radius:4px;
	border-style:solid;
	border-width:1px;
	border-color: rgb(180,180,180);
  	background-color:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
}
QCheckBox::indicator:unchecked {
	border-radius:4px;
	border-style:solid;
	border-width:1px;
	border-color: rgb(87, 97, 106);
  	background-color:rgb(255,255,255);
}
QStatusBar {
	color:rgb(240,240,240);
}'''
        self.tabWidget.setStyleSheet(style7)
    def style8(self):
        style8='''/*
Dark Console Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Company: GTRONICK
Last updated: 24/05/2018, 17:12.
Available at: https://github.com/GTRONICK/QSS/blob/master/ConsoleStyle.qss
*/
QWidget {
	background-color:rgb(0, 0, 0);
	color: rgb(240, 240, 240);
	border-color: rgb(58, 58, 58);
}

QPlainTextEdit {
	background-color:rgb(0, 0, 0);
	color: rgb(200, 200, 200);
	selection-background-color: rgb(255, 153, 0);
	selection-color: rgb(0, 0, 0);
}

QTabWidget::pane {
    	border-top: 1px solid #000000;
}

QTabBar::tab {
 	background-color:rgb(0, 0, 0);
 	border-style: outset;
	border-width: 1px;
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
  border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-top-width: 0px;
	border-style: solid;
	color: rgb(255, 153, 0);
	padding: 4px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
   color: rgb(255, 255, 255);
   background-color:rgb(0, 0, 0);
   border-color:rgb(42, 42, 42);
   margin-left: 0px;
   margin-right: 0px;
   border-bottom-right-radius:4px;
   border-bottom-left-radius:4px;
}

QTabBar::tab:last:selected {
  background-color:rgb(0, 0, 0);
	border-color:rgb(42, 42, 42);
	margin-left: 0px;
  	margin-right: 0px;
	border-bottom-right-radius:4px;
	border-bottom-left-radius:4px;
}

QTabBar::tab:!selected {
   margin-bottom: 4px;
   border-bottom-right-radius:4px;
   border-bottom-left-radius:4px;
}

QPushButton{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 6px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}

QPushButton:hover{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
	border-bottom-color: rgb(115, 115, 115);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 6px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(157, 157, 157, 255));
}

QPushButton:pressed{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(62, 62, 62, 255), stop:1 rgba(22, 22, 22, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(255, 255, 255);
	padding: 6px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}

QPushButton:disabled{
	border-style: outset;
	border-width: 2px;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
	border-bottom-color: rgb(58, 58, 58);
	border-bottom-width: 1px;
	border-style: solid;
	color: rgb(0, 0, 0);
	padding: 6px;
	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(57, 57, 57, 255), stop:1 rgba(77, 77, 77, 255));
}

QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: rgb(255, 255, 255);
	background:rgb(101, 101, 101);
	selection-background-color: rgb(187, 187, 187);
	selection-color: rgb(60, 63, 65);
}

QProgressBar {
	text-align: center;
	color: rgb(255, 255, 255);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
}

QProgressBar::chunk {
	background-color: qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(0, 200, 0, 255), stop:1 rgba(30, 230, 30, 255));
	border-radius: 10px;
}

QMenuBar {
	background:rgb(0, 0, 0);
	color: rgb(255, 153, 0);
}

QMenuBar::item {
  	spacing: 3px; 
	padding: 1px 4px;
  	background: transparent;
}

QMenuBar::item:selected { 
  	background:rgb(115, 115, 115);
}

QMenu {
	border-width: 2px; 
	border-radius: 10px;
	border-color: rgb(255, 153, 0);
	border-style: outset;
}

QMenu::item {
	spacing: 3px; 
	padding: 3px 15px;
}

QMenu::item:selected {
	spacing: 3px; 
	padding: 3px 15px;
	background:rgb(115, 115, 115);
	color:rgb(255, 255, 255);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
}'''
        self.tabWidget.setStyleSheet(style8)
    def style9(self):
        syle9='''QWidget {
    font-size: 11px;
}

QTableView {
    font-size: 10px;
    alternate-background-color: #EEEEFF;
}

Browser QPushButton {
    font-size: 10px;
    min-width: 10px;
}

ColorButton::enabled {
    border: 1px solid #444444;
}

ColorButton::disabled {
    border: 1px solid #AAAAAA;
}


Browser QGroupBox {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);
    border: 2px solid #999999;
    border-radius: 5px;
    margin-top: 1ex; /* leave space at the top for the title */
    font-size: 13px;
    color: black;
}

Browser QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding: 0 3px;
    font-size: 13px;
    color: black;
}

PluginItem {
    border: 2px solid black;
    background: white;
}


PluginItem Frame {
    background: #CCCCCC;
}


TabButton {
    border: 1px solid #8f8f91;
    border-radius: 2px;
    padding: 3px;
    min-width: 120px;
}

TabButton::checked {
    background-color: qlineargradient(x1: 0, y1: 0 , x2: 0, y2: 1,
                                      stop: 0 #9a9b9e, stop: 1 #babbbe);
}


TabButton::pressed {
    background-color: qlineargradient(x1: 0, y1: 0 , x2: 0, y2: 1,
                                      stop: 0 #9a9b9e, stop: 1 #babbbe);'''
        self.tabWidget.setStyleSheet(syle9)
    def style10(self):
        sty='''/*
ManjaroMix Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Company: GTRONICK
Last updated: 25/02/2020, 15:42.
Available at: https://github.com/GTRONICK/QSS/blob/master/ManjaroMix.qss
*/
QMainWindow {
	background-color:#151a1e;
}
QCalendar {
	background-color: #151a1e;
}
QTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}
QPlainTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}
QToolButton {
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: rgb(255,255,255);
}
QToolButton:hover{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(197, 197, 197), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(197, 197, 197));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(255,255,255);
}
QToolButton:pressed{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(142,142,142);
}
QPushButton{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #151a1e;
}
QPushButton::default{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #FFFFFF;
	padding: 2px;
	background-color: #151a1e;;
}
QPushButton:hover{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #1c1f1f;
}
QPushButton:pressed{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #2c2f2f;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: #808086;
	padding: 2px;
	background-color: rgb(142,142,142);
}
QLineEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}
QLabel {
	color: #d3dae3;
}
QLCDNumber {
	color: #4d9b87;
}
QProgressBar {
	text-align: center;
	color: #d3dae3;
	border-radius: 10px;
	border-color: transparent;
	border-style: solid;
	background-color: #52595d;
}
QProgressBar::chunk {
	background-color: #214037	;
	border-radius: 10px;
}
QMenuBar {
	background-color: #151a1e;
}
QMenuBar::item {
	color: #d3dae3;
  	spacing: 3px;
  	padding: 1px 4px;
	background-color: #151a1e;
}

QMenuBar::item:selected {
  	background-color: #252a2e;
	color: #FFFFFF;
}
QMenu {
	background-color: #151a1e;
}
QMenu::item:selected {
	background-color: #252a2e;
	color: #FFFFFF;
}
QMenu::item {
	color: #d3dae3;
	background-color: #151a1e;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:#000000;
}
QTabWidget::pane {
		border-color: #050a0e;
		background-color: #1e282c;
		border-style: solid;
		border-width: 1px;
    	border-bottom-left-radius: 4px;
		border-bottom-right-radius: 4px;
}
QTabBar::tab:first {
	border-style: solid;
	border-left-width:1px;
	border-right-width:0px;
	border-top-width:1px;
	border-bottom-width:0px;
	border-top-color: #050a0e;
	border-left-color: #050a0e;
	border-bottom-color: #050a0e;
	border-top-left-radius: 4px;
	color: #d3dae3;
	padding: 3px;
	margin-left:0px;
	background-color: #151a1e;
}
QTabBar::tab:last {
	border-style: solid;
	border-top-width:1px;
	border-left-width:1px;
	border-right-width:1px;
	border-bottom-width:0px;
	border-color: #050a0e;
	border-top-right-radius: 4px;
	color: #d3dae3;
	padding: 3px;
	margin-left:0px;
	background-color: #151a1e;
}
QTabBar::tab {
	border-style: solid;
	border-top-width:1px;
	border-bottom-width:0px;
	border-left-width:1px;
	border-top-color: #050a0e;
	border-left-color: #050a0e;
	border-bottom-color: #050a0e;
	color: #d3dae3;
	padding: 3px;
	margin-left:0px;
	background-color: #151a1e;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	border-style: solid;
  	border-left-width:1px;
	border-bottom-width:0px;
	border-right-color: transparent;
	border-top-color: #050a0e;
	border-left-color: #050a0e;
	border-bottom-color: #050a0e;
	color: #FFFFFF;
	padding: 3px;
	margin-left:0px;
	background-color: #1e282c;
}

QTabBar::tab:selected, QTabBar::tab:first:selected, QTabBar::tab:hover {
  	border-style: solid;
  	border-left-width:1px;
  	border-bottom-width:0px;
  	border-top-width:1px;
	border-right-color: transparent;
	border-top-color: #050a0e;
	border-left-color: #050a0e;
	border-bottom-color: #050a0e;
	color: #FFFFFF;
	padding: 3px;
	margin-left:0px;
	background-color: #1e282c;
}

QCheckBox {
	color: #d3dae3;
	padding: 2px;
}
QCheckBox:disabled {
	color: #808086;
	padding: 2px;
}

QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: transparent;
}
QCheckBox::indicator:checked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #4fa08b;
	color: #000000;
	background-color: qradialgradient(cx:0.4, cy:0.4, radius: 1.5,fx:0, fy:0, stop:0 #1e282c, stop:0.3 #1e282c, stop:0.4 #4fa08b, stop:0.5 #1e282c, stop:1 #1e282c);
}
QCheckBox::indicator:unchecked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #4fa08b;
	color: #000000;
}
QRadioButton {
	color: #d3dae3;
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #4fa08b;
	color: #a9b7c6;
	background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #4fa08b, stop:1 #1e282c);
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #4fa08b;
	color: #a9b7c6;
	background-color: transparent;
}
QStatusBar {
	color:#027f7f;
}
QSpinBox {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QDoubleSpinBox {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QTimeEdit {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QDateTimeEdit {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QDateEdit {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QFontComboBox {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}
QComboBox {
	color: #d3dae3;
	background-color: #222b2e;
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
}

QDial {
	background: #16a085;
}

QToolBox {
	color: #a9b7c6;
	background-color: #222b2e;
}
QToolBox::tab {
	color: #a9b7c6;
	background-color:#222b2e;
}
QToolBox::tab:selected {
	color: #FFFFFF;
	background-color:#222b2e;
}
QScrollArea {
	color: #FFFFFF;
	background-color:#222b2e;
}
QSlider::groove:horizontal {
	height: 5px;
	background-color: #52595d;
}
QSlider::groove:vertical {
	width: 5px;
	background-color: #52595d;
}
QSlider::handle:horizontal {
	background: #1a2224;
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	width: 12px;
	margin: -5px 0;
	border-radius: 7px;
}
QSlider::handle:vertical {
	background: #1a2224;
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	height: 12px;
	margin: 0 -5px;
	border-radius: 7px;
}
QSlider::add-page:horizontal {
    background: #52595d;
}
QSlider::add-page:vertical {
    background: #52595d;
}
QSlider::sub-page:horizontal {
    background-color: #15433a;
}
QSlider::sub-page:vertical {
    background-color: #15433a;
}
QScrollBar:horizontal {
	max-height: 10px;
	border: 1px transparent grey;
	margin: 0px 20px 0px 20px;
	background: transparent;
}
QScrollBar:vertical {
	max-width: 10px;
	border: 1px transparent grey;
	margin: 20px 0px 20px 0px;
	background: transparent;
}
QScrollBar::handle:horizontal {
	background: #52595d;
	border-style: transparent;
	border-radius: 4px;
	min-width: 25px;
}
QScrollBar::handle:horizontal:hover {
	background: #58a492;
	border-style: transparent;
	border-radius: 4px;
	min-width: 25px;
}
QScrollBar::handle:vertical {
	background: #52595d;
	border-style: transparent;
	border-radius: 4px;
	min-height: 25px;
}
QScrollBar::handle:vertical:hover {
	background: #58a492;
	border-style: transparent;
	border-radius: 4px;
	min-height: 25px;
}
QScrollBar::add-line:horizontal {
   border: 2px transparent grey;
   border-top-right-radius: 4px;
   border-bottom-right-radius: 4px;
   background: #15433a;
   width: 20px;
   subcontrol-position: right;
   subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:pressed {
   border: 2px transparent grey;
   border-top-right-radius: 4px;
   border-bottom-right-radius: 4px;
   background: rgb(181,181,181);
   width: 20px;
   subcontrol-position: right;
   subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
   border: 2px transparent grey;
   border-bottom-left-radius: 4px;
   border-bottom-right-radius: 4px;
   background: #15433a;
   height: 20px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:pressed {
   border: 2px transparent grey;
   border-bottom-left-radius: 4px;
   border-bottom-right-radius: 4px;
   background: rgb(181,181,181);
   height: 20px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
   border: 2px transparent grey;
   border-top-left-radius: 4px;
   border-bottom-left-radius: 4px;
   background: #15433a;
   width: 20px;
   subcontrol-position: left;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:pressed {
   border: 2px transparent grey;
   border-top-left-radius: 4px;
   border-bottom-left-radius: 4px;
   background: rgb(181,181,181);
   width: 20px;
   subcontrol-position: left;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
   border: 2px transparent grey;
   border-top-left-radius: 4px;
   border-top-right-radius: 4px;
   background: #15433a;
   height: 20px;
   subcontrol-position: top;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:pressed {
   border: 2px transparent grey;
   border-top-left-radius: 4px;
   border-top-right-radius: 4px;
   background: rgb(181,181,181);
   height: 20px;
   subcontrol-position: top;
   subcontrol-origin: margin;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
   background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
   background: none;
}'''
        self.tabWidget.setStyleSheet(sty)
    def sty11(self):
        styy='''/*
AMOLED Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Company: GTRONICK
Last updated: 15/10/2019, 11:40.
Available at: https://github.com/GTRONICK/QSS/blob/master/AMOLED.qss
*/
QMainWindow {
	background-color:#000000;
}
QDialog {
	background-color:#000000;
}
QColorDialog {
	background-color:#000000;
}
QTextEdit {
	background-color:#000000;
	color: #a9b7c6;
}
QPlainTextEdit {
	selection-background-color:#f39c12;
	background-color:#000000;
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	color: #a9b7c6;
}
QPushButton{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #000000;
}
QPushButton::default{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-width: 1px;
	color: #a9b7c6;
	padding: 2px;
	background-color: #000000;
}
QPushButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 1px;
	border-bottom-radius: 6px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 2px;
	background-color: #000000;
}
QPushButton:pressed{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 2px;
	border-bottom-radius: 6px;
	border-style: solid;
	color: #e67e22;
	padding-bottom: 1px;
	background-color: #000000;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 2px;
	border-bottom-radius: 6px;
	border-style: solid;
	color: #808086;
	padding-bottom: 1px;
	background-color: #000000;
}
QToolButton {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #000000;
}
QToolButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 2px;
	border-bottom-radius: 6px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 1px;
	background-color: #000000;
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: #a9b7c6;
	background:#000000;
	selection-background-color:#007b50;
	selection-color: #FFFFFF;
}
QLabel {
	color: #a9b7c6;
}
QLCDNumber {
	color: #e67e22;
}
QProgressBar {
	text-align: center;
	color: rgb(240, 240, 240);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	background-color:#000000;
}
QProgressBar::chunk {
	background-color: #e67e22;
	border-radius: 5px;
}
QMenu{
	background-color:#000000;
}
QMenuBar {
	background:rgb(0, 0, 0);
	color: #a9b7c6;
}
QMenuBar::item {
  	spacing: 3px; 
	padding: 1px 4px;
  	background: transparent;
}
QMenuBar::item:selected { 
  	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 1px;
	border-bottom-radius: 6px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 0px;
	background-color: #000000;
}
QMenu::item:selected {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: #e67e22;
	border-bottom-color: transparent;
	border-left-width: 2px;
	color: #FFFFFF;
	padding-left:15px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color:#000000;
}
QMenu::item {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding-left:17px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color:#000000;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:#000000;
}
QTabWidget::pane {
		border-color: rgb(77,77,77);
		background-color:#000000;
		border-style: solid;
		border-width: 1px;
    	border-radius: 6px;
}
QTabBar::tab {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #808086;
	padding: 3px;
	margin-left:3px;
	background-color:#000000;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #e67e22;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-left: 3px;
	padding-bottom: 2px;
	margin-left:3px;
	background-color:#000000;
}

QCheckBox {
	color: #a9b7c6;
	padding: 2px;
}
QCheckBox:disabled {
	color: #808086;
	padding: 2px;
}

QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: rgb(87, 97, 106);
	background-color:#000000;
}
QCheckBox::indicator:checked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #e67e22;
	color: #a9b7c6;
	background-color: #e67e22;
}
QCheckBox::indicator:unchecked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #e67e22;
	color: #a9b7c6;
	background-color: transparent;
}
QRadioButton {
	color: #a9b7c6;
	background-color:#000000;
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #e67e22;
	color: #a9b7c6;
	background-color: #e67e22;
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #e67e22;
	color: #a9b7c6;
	background-color: transparent;
}
QStatusBar {
	color:#027f7f;
}
QSpinBox {
	color: #a9b7c6;	
	background-color:#000000;
}
QDoubleSpinBox {
	color: #a9b7c6;	
	background-color:#000000;
}
QTimeEdit {
	color: #a9b7c6;	
	background-color:#000000;
}
QDateTimeEdit {
	color: #a9b7c6;	
	background-color:#000000;
}
QDateEdit {
	color: #a9b7c6;	
	background-color:#000000;
}
QComboBox {
	color: #a9b7c6;	
	background: #1e1d23;
}
QComboBox:editable {
	background: #1e1d23;
	color: #a9b7c6;
	selection-background-color:#000000;
}
QComboBox QAbstractItemView {
	color: #a9b7c6;	
	background: #1e1d23;
	selection-color: #FFFFFF;
	selection-background-color:#000000;
}
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
	color: #a9b7c6;	
	background: #1e1d23;
}
QFontComboBox {
	color: #a9b7c6;	
	background-color:#000000;
}
QToolBox {
	color: #a9b7c6;
	background-color:#000000;
}
QToolBox::tab {
	color: #a9b7c6;
	background-color:#000000;
}
QToolBox::tab:selected {
	color: #FFFFFF;
	background-color:#000000;
}
QScrollArea {
	color: #FFFFFF;
	background-color:#000000;
}
QSlider::groove:horizontal {
	height: 5px;
	background: #e67e22;
}
QSlider::groove:vertical {
	width: 5px;
	background: #e67e22;
}
QSlider::handle:horizontal {
	background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	width: 14px;
	margin: -5px 0;
	border-radius: 7px;
}
QSlider::handle:vertical {
	background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	height: 14px;
	margin: 0 -5px;
	border-radius: 7px;
}
QSlider::add-page:horizontal {
    background: white;
}
QSlider::add-page:vertical {
    background: white;
}
QSlider::sub-page:horizontal {
    background: #e67e22;
}
QSlider::sub-page:vertical {
    background: #e67e22;
}
QScrollBar:horizontal {
	max-height: 20px;
	background: rgb(0,0,0);
	border: 1px transparent grey;
	margin: 0px 20px 0px 20px;
}
QScrollBar::handle:horizontal {
	background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
	border-style: solid;
	border-width: 1px;
	border-color: rgb(0,0,0);
	min-width: 25px;
}
QScrollBar::handle:horizontal:hover {
	background: rgb(230, 126, 34);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(0,0,0);
	min-width: 25px;
}
QScrollBar::add-line:horizontal {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
  	background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
  	width: 20px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:hover {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:pressed {
  	border: 1px solid;
  	border-color: grey;
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: right;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
  	background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
  	width: 20px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:hover {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:pressed {
  	border: 1px solid;
  	border-color: grey;
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: left;
  	subcontrol-origin: margin;
}
QScrollBar::left-arrow:horizontal {
  	border: 1px transparent grey;
  	border-radius: 3px;
  	width: 6px;
  	height: 6px;
 	background: rgb(0,0,0);
}
QScrollBar::right-arrow:horizontal {
	border: 1px transparent grey;
	border-radius: 3px;
  	width: 6px;
  	height: 6px;
 	background: rgb(0,0,0);
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
 	background: none;
} 
QScrollBar:vertical {
	max-width: 20px;
	background: rgb(0,0,0);
	border: 1px transparent grey;
	margin: 20px 0px 20px 0px;
}
QScrollBar::add-line:vertical {
	border: 1px solid;
  	border-color: rgb(0,0,0);
  	background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
  	height: 20px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:pressed {
  	border: 1px solid;
  	border-color: grey;
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: bottom;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
	background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
  	height: 20px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover {
  	border: 1px solid;
  	border-color: rgb(0,0,0);
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:pressed {
  	border: 1px solid;
  	border-color: grey;
	border-radius: 8px;
  	background: rgb(230, 126, 34);
  	height: 16px;
  	width: 16px;
  	subcontrol-position: top;
  	subcontrol-origin: margin;
}
	QScrollBar::handle:vertical {
	background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
	border-style: solid;
	border-width: 1px;
	border-color: rgb(0,0,0);
	min-height: 25px;
}
QScrollBar::handle:vertical:hover {
	background: rgb(230, 126, 34);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(0,0,0);
	min-heigth: 25px;
}
QScrollBar::up-arrow:vertical {
	border: 1px transparent grey;
	border-radius: 3px;
  	width: 6px;
  	height: 6px;
 	background: rgb(0,0,0);
}
QScrollBar::down-arrow:vertical {
  	border: 1px transparent grey;
  	border-radius: 3px;
  	width: 6px;
  	height: 6px;
 	background: rgb(0,0,0);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  	background: none;
	}'''
        self.tabWidget.setStyleSheet(styy)
def main():
    app = QApplication(sys.argv)                            
    window = App_Window()
    window.show()
    app.exec_()
if __name__ == "__main__":
    main()
