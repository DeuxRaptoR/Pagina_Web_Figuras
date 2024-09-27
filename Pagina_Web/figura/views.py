from django.shortcuts import render
from figura.models import Usuario , Figura


def mostrarMenuPrincipal(request):

    fig = Figura.objects.all().values().order_by("nombre_figura")

    datos = {
        'fig' : fig
    } 
    return render(request, 'menu_principal.html', datos)


def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtnom"]
        con = request.POST["txtcon"]

        comprobarLogin = Usuario.objects.filter(nombre_usuario = nom, contraseña_usuario = con).values()

        fig = Figura.objects.all().values().order_by("nombre_figura")

        if comprobarLogin:
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]['id']
            request.session["nomUsuario"] = nom.upper()

            datos = {
                'nomUsuario' : nom.upper(),
                'fig' : fig
            } 

            if nom.upper() == "ADMIN":
                    return render(request, 'menu_admin.html', datos)
            else:
                    return render(request, 'menu_usuario.html', datos)
        
        else:
            datos = { 'r2' : 'Error De Usuario y/o Contraseña!!' }
            return render(request, 'login.html', datos)
    
    else: 
        return render(request, 'login.html')            


    
def cerrarSesion(request):
    try:
        nom = request.session['nomUsuario']
        del request.session['nomUsuario']
        del request.session['estadoSesion']


        return render(request, 'login.html')
    except:
        return render(request, 'login.html')



def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            fig = Figura.objects.all().all().order_by("nombre_figura")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'fig' : fig
            }
            return render(request, 'menu_admin.html', datos)
        else:
            datos = { 'r2' : 'Usuario y/o contraseña incorrectas!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
    


def mostrarMenuUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper()!="ADMIN":
            datos = { 'nomUsuario' : request.session["nomUsuario"] }
            return render(request, 'menu_usuario.html', datos)
        else:
            datos = { 'r2' : 'Usuario y/o contraseña incorrectas!!' }
            return render(request, 'login.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'login.html', datos) 





def mostrarRegistrarFigura(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":

            fig = Figura.objects.all().values().order_by("nombre_figura")
            
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'fig' : fig
            }

            return render(request, 'registrar_admin.html', datos)
        else:

            datos = { 'r' : 'No Tiene Privilegios Suficientes Para Acceder!!' }
            return render(request, 'login.html', datos)
            
    else:
        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'login.html', datos)



def registrarFigura(request):
    if request.method == 'POST':
        nom = request.POST['txtnom']
        per = request.POST['txtper']
        fab = request.POST['txtfab']
        pre = request.POST['numpre']
        tam = request.POST['numtam']
        mat = request.POST['txtmat']
        acc = request.POST['txtacc']
        cat = request.POST['txtcat']
        try:
            img = request.FILES['txtimg']
        except:
            img = "imagenes/noimage.png"    

        fig = Figura(nombre_figura = nom, personaje = per, fabricante = fab, precio = pre, tamaño = tam,
        material = mat, accesorios = acc, categoria = cat, imagen = img )
        fig.save()
        datos = {'r' : 'Figura registrada correctamente'}
        return render(request, 'registrar_admin.html', datos)
    else:
        datos = {'r2' : 'No se puede procesar la solicitud'}
        return render(request,'registrar_admin.html', datos)





def mostrarActualizarFigura(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:

            fig = Figura.objects.get(id=id)

            datos = { 
                'nomUsuario' : request.session["nomUsuario"],
                'fig' : fig,
            }
            return render(request, 'actualizar_registro.html', datos)
        else:

            datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'login.html', datos)
    except:

        fig = Figura.objects.all().all().values()

        datos = { 
            'nomUsuario' : request.session["nomUsuario"],
            'fig' : fig,
            'r2':"El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
        }
        return render(request, 'menu_admin.html', datos)



def actualizarFigura(request,id):
    try:
        nom = request.POST['txtnom']
        per = request.POST['txtper']
        fab = request.POST['txtfab']
        pre = request.POST['numpre']
        tam = request.POST['numtam']
        mat = request.POST['txtmat']
        acc = request.POST['txtacc']
        cat = request.POST['txtcat']

        fig = Figura.objects.get (id=id)

        try:
            img = request.FILES['txtimg']

            ruta_imagen = "media/"+str(fig.imagen)
            import os
            if ruta_imagen != "media/imagenes/noimage.png":
                os.remove(ruta_imagen)
        except:
            img = fig.imagen 

        fig.nombre_figura = nom
        fig.personaje = per
        fig.fabricante = fab
        fig.precio = pre
        fig.tamaño = tam
        fig.material = mat
        fig.accesorios = acc
        fig.categoria = cat
        fig.imagen = img    
        fig.save()     

        fig = Figura.objects.all().values()
        datos = {
            'fig' : fig,
            'r' : 'Datos Modificados Correctamente'
        }
        return render(request, 'menu_admin.html', datos)  

    except:

        fig = Figura.objects.all().values()
        
        datos = {
            'fig' : fig,
            'r2' : 'El ID ('+str(id)+') No Existe'
        }
        
        return render(request, 'menu_admin.html', datos)


# Create your views here.
 