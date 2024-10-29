from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MaestroConductor
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    total_conductor = MaestroConductor.objects.all().count()
    
    context = {
        'total_conductor': total_conductor
    }
    return render(request, 'home.html', context)

def RegistrarConductor(request):
    dniConductorExiste = False
    if request.method == 'POST':
        dniRegistro = request.POST['dni-registro']
        breveteRegistro = request.POST['brevete-registro']
        nombreRegistro = request.POST['nombre-registro']
        vencimientoBrevete = request.POST['vencimiento-brevete']
        apellidoRegistro = request.POST['apellido-registro']
        telefonoRegistro = request.POST['telefono-registro']

        dniConductorExiste = MaestroConductor.objects.filter(dni_conductor__iexact=dniRegistro).exists()

        if dniConductorExiste:
            messages.error(request, "El Conductor ya existe")
            return redirect('buscar-conductor')
        else:
            MaestroConductor.objects.create(
                dni_conductor=dniRegistro,
                brevete_conductor=breveteRegistro,
                nombre_conductor=nombreRegistro,
                vencimiento_brevete=vencimientoBrevete,
                apellido_conductor=apellidoRegistro,
                celular_conductor=telefonoRegistro
            )
            messages.success(request, "Conductor Registrado Correctamente")
            return redirect('buscar-conductor')

    context = {
        'dniConductorExiste': dniConductorExiste,
    }
    return render(request, 'admin-buscar-conductor.html', context)


def BuscarConductor(request):
    
    if 'buscar' in request.GET:
        buscarConductor = request.GET['buscar']
        listabusquedaConductor = MaestroConductor.objects.filter(
            Q(dni_conductor__icontains=buscarConductor) |
            Q(apellido_conductor__icontains=buscarConductor)
        ).order_by('apellido_conductor')
    else:
        listabusquedaConductor = MaestroConductor.objects.all().order_by('apellido_conductor')

    paginator = Paginator(listabusquedaConductor, 10)
    pagina = request.GET.get('page') or 1
    listabusquedaConductor = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listabusquedaConductor.paginator.num_pages + 1)

    context = {
        'listabusquedaConductor': listabusquedaConductor,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
    }
    return render(request, 'admin-buscar-conductor.html', context)

