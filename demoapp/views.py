from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import EmployeeRegistrationForm,ProductForm,AdminLoginForm,DepartmentForm,UpdateDepartmentForm
from .models import Employee,Department,Admin,Product


def index(request):
    return render(request,"index.html")

def empregistration(request):
    form = EmployeeRegistrationForm()
    if request.method == "POST":
        formdata = EmployeeRegistrationForm(request.POST)
        if formdata.is_valid():
            formdata.save()
            msg="Employee Registered Successfully"
            return render(request, "empregistration.html", {"empform": form,"msg":msg})
        else:
            msg = "Failed to Register Employee"
            return render(request, "empregistration.html", {"empform": form, "msg": msg})
    return render(request,"empregistration.html",{"empform":form})

def emplogin(request):
    return render(request,"emplogin.html")

def checkemplogin(request):
    uname = request.POST["eusername"]
    pwd = request.POST["epassword"]

    flag = Employee.objects.filter(Q(username=uname) & Q(password=pwd))

    print(flag)

    if flag:
        emp = Employee.objects.get(username=uname)
        print(emp)
        request.session["eid"] = emp.id
        request.session["ename"] = emp.fullname
        return render(request, "emphome.html", {"eid": emp.id, "ename": emp.fullname})
    else:
        msg = "Login Failed"
        return render(request, "emplogin.html", {"msg": msg})


def emphome(request):
    eid=request.session["eid"]
    ename=request.session["ename"]

    return render(request,"emphome.html",{"eid":eid,"ename":ename})

def empprofile(request):
    eid=request.session["eid"]
    ename=request.session["ename"]
    emp = Employee.objects.get(id=eid)
    return render(request,"empprofile.html",{"eid":eid,"ename":ename,"emp":emp})

def empchangepwd(request):
    eid=request.session["eid"]
    ename=request.session["ename"]
    return render(request,"empchangepwd.html",{"eid":eid,"ename":ename})

def empupdatepwd(request):
    eid=request.session["eid"]
    ename=request.session["ename"]

    opwd=request.POST["opwd"]
    npwd=request.POST["npwd"]

    flag = Employee.objects.filter(Q(id=eid) & Q(password=opwd))

    if flag:
        Employee.objects.filter(id=eid).update(password=npwd)
        msg = "Password Updated Successfully"
        return render(request, "empchangepwd.html", {"eid": eid, "ename": ename,"msg":msg})
    else:
        msg = "Old Password is Incorrect"
        return render(request, "empchangepwd.html", {"eid": eid, "ename": ename,"msg":msg})

def vieweproducts(request):

    eid=request.session["eid"]
    ename=request.session["ename"]

    productlist = Product.objects.all()

    return render(request,"vieweproducts.html",{"eid": eid, "ename": ename,"productlist":productlist})

def displayeproducts(request):

    eid=request.session["eid"]
    ename=request.session["ename"]

    pname = request.POST["pname"]
    print(pname)

    productlist = Product.objects.filter(name__icontains=pname)

    return render(request,"displayeproducts.html",{"eid": eid, "ename": ename,"productlist":productlist})


def emplogout(request):
    return render(request,"emplogin.html")

def adminlogin(request):
    return render(request,"adminlogin.html")

def checkadminlogin(request):
    uname = request.POST["ausername"]
    pwd = request.POST["apassword"]

    flag = Admin.objects.filter(Q(username__exact=uname) & Q(password__exact=pwd))
    print(flag)

    if flag:
        admin = Admin.objects.get(username=uname)
        print(admin)
        request.session["auname"] = admin.username
        return render(request, "adminhome.html", {"auname": admin.username})
    else:
        msg = "Login Failed"
        return render(request, "adminlogin.html", {"msg": msg})


def adminhome(request):
    auname=request.session["auname"]
    return render(request,"adminhome.html",{"auname":auname})

def adddepartment(request):
    auname = request.session["auname"]
    form = DepartmentForm()
    if request.method == "POST":
        formdata = DepartmentForm(request.POST)
        if formdata.is_valid():
            formdata.save()
            msg="Department Added Successfully"
            return render(request, "adddept.html", {"auname":auname,"deptform": form,"msg":msg})
        else:
            msg = "Failed to Add Department"
            return render(request, "adddept.html", {"auname":auname,"deptform": form, "msg": msg})
    return render(request,"adddept.html",{"auname":auname,"deptform":form})

def updatedepartment(request):
    auname = request.session["auname"]
    form = UpdateDepartmentForm()
    if request.method == "POST":
        formdata = UpdateDepartmentForm(request.POST)

        deptid = formdata.data['id']
        deptname = formdata.data['name']
        deptloc = formdata.data['location']

        flag = Department.objects.filter(id=deptid)

        if flag:
            Department.objects.filter(id=deptid).update(name=deptname,location=deptloc)
            msg="Department Updated Successfully"
            return render(request, "updatedept.html", {"auname":auname,"deptform": form,"msg":msg})
        else:
            msg = "Department ID Not Found"
            return render(request, "updatedept.html", {"auname":auname,"deptform": form, "msg": msg})

    return render(request,"updatedept.html",{"auname":auname,"deptform":form})

def addproduct(request):
    auname = request.session["auname"]
    form = ProductForm()
    if request.method == "POST":
        formdata = ProductForm(request.POST,request.FILES)
        if formdata.is_valid():
            formdata.save()
            msg="Product Added Successfully"
            return render(request, "addproduct.html", {"auname":auname,"productform": form,"msg":msg})
        else:
            msg = "Failed to Add Product"
            return render(request, "addproduct.html", {"auname":auname,"productform": form, "msg": msg})
    return render(request,"addproduct.html",{"auname":auname,"productform":form})

def viewemployees(request):
    auname=request.session["auname"]
    emplist = Employee.objects.all()
    count = Employee.objects.count()
    return render(request,"viewemps.html",{"auname":auname,"emplist":emplist,"count":count})

def viewdepartments(request):
    auname=request.session["auname"]
    deptlist = Department.objects.all()
    count = Department.objects.count()
    return render(request,"viewdepts.html",{"auname":auname,"deptlist":deptlist,"count":count})

def viewaproducts(request):
    auname=request.session["auname"]
    productlist = Product.objects.all()
    count = Product.objects.count()
    return render(request,"viewaproducts.html",{"auname":auname,"productlist":productlist,"count":count})

def deleteemp(reequest,eid):
    Employee.objects.filter(id=eid).delete()
    return redirect("viewemps")

def adminlogout(request):
    return render(request,"adminlogin.html")
