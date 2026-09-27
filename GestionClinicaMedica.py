import datetime
import re  

# Excepción personalizada para datos inválidos.
class DatoInvalidoError(Exception):
    # Excepción lanzada cuando un dato no cumple con el formato esperado.
    def __init__(self, mensaje):
        super().__init__(mensaje)
        
        
# -- CLASES -- 

# Clase Base Persona con atributos comunes a médicos y pacientes, y validaciones de formato.
class Persona:
    # Clase padre que representa una persona genérica.
    def __init__(self, dni, nombre, edad, genero, correo, telefono):
        self.dni = dni
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.correo = correo
        self.telefono = telefono

    # Getters y Setters con validaciones de la clase Persona
    
    @property
    def dni(self):
        return self._dni
    
    # Valida que el DNI tenga el formato correcto (8 números y 1 letra) usando Regex.
    @dni.setter
    def dni(self, valor):
        patron = r"^\d{8}[A-Za-z]$"
        if not re.match(patron, valor):
            raise DatoInvalidoError(f"El DNI '{valor}' no es válido. Debe tener 8 números y 1 letra.\n")
        self._dni = valor.upper()

    @property
    def correo(self):
        return self._correo
    
    # Valida que el correo tenga un formato básico (texto@dominio.extensión).
    @correo.setter
    def correo(self, valor):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor):
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.\n")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono
    
    # Valida que el teléfono tenga exactamente 9 dígitos numéricos.
    @telefono.setter
    def telefono(self, valor):
        patron = r"^\d{9}$"
        if not re.match(patron, valor):
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener 9 dígitos numéricos.\n")
        self._telefono = valor

    #Getters y Setters del resto de atributos
    
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, val): self._nombre = val
    
    @property
    def edad(self): return self._edad
    @edad.setter
    def edad(self, val): self._edad = val
    
    @property
    def genero(self): return self._genero
    
    # Valida que el género sea M (Masculino), F (Femenino) u O (Otro).
    @genero.setter
    def genero(self, val): 
        if(val.upper()) not in ["M","F","O"]:
            raise DatoInvalidoError(f"El género '{val}' no es válido. Debe ser 'M', 'F' u 'O'.\n")
        self._genero = val.upper() 

    # Retorna un string con la información básica de la persona.
    def descripcion(self):
        return f"DNI: {self.dni} | Nombre: {self.nombre} | Edad: {self.edad} | Género: {self.genero} | Correo: {self.correo} | Teléfono: {self.telefono}\n"


# Clase Medico que hereda de Persona y tiene su propia especialidad, citas y pacientes asignados.

class Medico(Persona):
    
    lista_especialidades = ["Cardiología", "Dermatología", "Neurología", "Pediatría", "Psiquiatría", "Oncología", "Ginecología", "Traumatología"]
    
    def __init__(self, dni, nombre, edad, genero, correo, telefono, especialidad, citas=None,pacientes_asignados=None):
        super().__init__(dni, nombre, edad, genero, correo, telefono)
        self.especialidad = especialidad
        if(citas is None):
            self.citas = {}
        else:
            self.citas = citas
        
        if pacientes_asignados is None:
            self.pacientes_asignados = []
        else:
            self.pacientes_asignados = pacientes_asignados
    
    # Getters y Setters con validaciones de la clase Medico

    @property
    def especialidad(self):
        return self._especialidad
    
    # Valida que la especialidad esté en la lista predefinida. Intenta corregir capitalización.
    @especialidad.setter
    def especialidad(self, valor):
        valor_cap = valor.capitalize() 
        if valor not in Medico.lista_especialidades:
             if valor_cap in Medico.lista_especialidades:
                 self._especialidad = valor_cap
                 return

             raise DatoInvalidoError(f"La especialidad '{valor}' no es válida. Debe ser una de: {', '.join(Medico.lista_especialidades)}.\n")
        self._especialidad = valor
    
    # Añade un paciente a la lista de asignados del médico y vincula al médico en el paciente.
    def asignar_paciente(self, paciente):
        self.pacientes_asignados.append(f"{paciente.nombre} (DNI: {paciente.dni})")
        paciente.asignar_medico(self)
        
    # Crea un registro médico con fecha y diagnóstico y lo añade al historial del paciente.
    def realizar_diagnostico(self, paciente, diagnostico, informe):
        registro = {
            "fecha": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "paciente": f"{paciente.nombre} (DNI: {paciente.dni})",
            "diagnostico": diagnostico,
            "informe": informe,
            "especialidad_medica": self.especialidad,
            "medico": f"Dr/a {self.nombre}"
        }
        
        paciente.agregar_al_historial(registro)
        print(f"\nDiagnóstico realizado para {paciente.nombre} por Dr/a {self.nombre}.\n\n")
    
    # Agrega una cita al diccionario de citas del médico y sincroniza con el paciente.
    def anadirCita(self, cita):
        self.citas[cita.fecha] = cita
        if cita.fecha not in cita.paciente.citas:
            cita.paciente.anadirCita(cita)
            
    # Imprime por pantalla todas las citas programadas del médico.
    def mostrar_citas(self):
        print(f"\n--- Citas del Dr./Dra. {self.nombre} ---\n")
        if not self.citas:
            print("No hay citas programadas.\n")
        else:
            for cita in self.citas.values():
                print(cita.descripcion()+"\n")
                
    # Muestra la lista de pacientes que tiene asignados este médico.
    def ver_pacientes(self):
        print(f"\n--- Pacientes asignados al Dr./Dra. {self.nombre} ---\n")
        if not self.pacientes_asignados:
            print("\nNo hay pacientes asignados.\n")
        else:
            for p in self.pacientes_asignados:
                print(p)
    
    # Sobrescribe la descripción base para añadir la especialidad.
    def descripcion(self):
        desc_base = super().descripcion()
        return (f"{desc_base}| Especialidad: {self.especialidad}\n")


# Clase Paciente que hereda de Persona y tiene su propio historial clínico, médicos asignados y citas.

class Paciente(Persona):
    
    def __init__(self, dni, nombre, edad, genero, correo, telefono,citas=None):
        super().__init__(dni, nombre, edad, genero, correo, telefono)
        self._historial_clinico = []
        self._medicos_asignados = [] 
        
        if citas is None:
            citas = {}
            
        self.citas = citas

       
    #Getters y Setters con de la clase Paciente
    
    @property
    def historial_clinico(self):
        return self._historial_clinico
    
    @historial_clinico.setter
    def historial_clinico(self, valor):
        self._historial_clinico = valor
        
    @property
    def medicos_asignados(self):
        return self._medicos_asignados
    
    @medicos_asignados.setter
    def medicos_asignados(self, valor):
        self._medicos_asignados = valor
        
    @property
    def citas(self):
        return self._citas

    @citas.setter
    def citas(self, valor):
        if not isinstance(valor, dict):
            raise DatoInvalidoError("Las citas deben ser un diccionario.")
        self._citas = valor
    
    
    # Recibe un diccionario con datos del diagnóstico y lo guarda en la lista.
    def agregar_al_historial(self, registro):
        self._historial_clinico.append(registro)

    # Imprime todo el historial clínico (diagnósticos pasados) del paciente.
    def ver_historial(self):
        print(f"\n--- Historial Clínico de {self.nombre} ---\n")
        if not self._historial_clinico:
            print("No hay entradas en el historial clínico.\n")
        else:
            for ficha in self._historial_clinico:
                print(f"Fecha: {ficha['fecha']}")
                print(f"Médico: {ficha['medico']}")
                print(f"Especialidad: {ficha['especialidad_medica']}")
                print(f"Diagnóstico: {ficha['diagnostico']}")
                print(f"Informe: {ficha['informe']}")
                
                print("-" * 30)
    
    # Vincula un médico a este paciente si no estaba ya asignado.
    def asignar_medico(self, medico):
        # El isinstance verifica que el objeto pasado sea de la clase Medico 
        if isinstance(medico, Medico):
            datos = {}
            datos[medico.nombre] = medico.especialidad
            if datos not in self._medicos_asignados:
                self._medicos_asignados.append(datos)
                print(f"Médico {medico.nombre} asignado al paciente {self.nombre}\n")
            else:
                print(f"El médico {medico.nombre} ya está asignado al paciente {self.nombre}.\n")
        else:
            print("Error: El dato pasado no es un médico válido.\n")
    
    # Añade la cita a la agenda del paciente y sincroniza con el médico.
    def anadirCita(self, cita):
        self.citas[cita.fecha] = cita
        if cita.fecha not in cita.medico.citas:
            cita.medico.anadirCita(cita)
        
    # Muestra las citas futuras del paciente.
    def mostrar_citas(self):
        print(f"--- Citas de {self.nombre} ---\n")
        if not self.citas:
            print("No hay citas programadas.\n")
        else:
            for cita in self.citas.values():
                print(cita.descripcion()+"\n")
    
    # Descripción extendida con resumen de historial y médicos.
    def descripcion(self):
        desc_base = super().descripcion()
        if not self._medicos_asignados:
            medicos_str = "Ninguno"
        else:
            medicos_str = ', '.join(self._medicos_asignados[0].keys())
        return (f"{desc_base}Historial Medico: {len(self._historial_clinico)} | Médicos: {medicos_str}\n")


# Clase Cita que representa una cita médica entre un paciente y un médico, con validación de fecha.

class Cita:
    def __init__(self, paciente, medico , fecha, motivo):
        self._paciente = paciente
        self._medico = medico
        self._motivo = motivo
        self._fecha = self.validar_fecha(fecha) # Valida al instanciar
        self._estado = "Pendiente"
        
        # Al crear la cita, se añade automáticamente a ambas partes
        self._paciente.anadirCita(self) 
        self._medico.anadirCita(self)
        
    # Getters y Setters con validaciones de la clase Cita
        
    @property
    def paciente(self): return self._paciente
    @paciente.setter
    def paciente(self, valor): self._paciente = valor
            
    @property
    def medico(self): return self._medico
    @medico.setter
    def medico(self, valor): self._medico = valor
            
    @property
    def motivo(self): return self._motivo
    @motivo.setter
    def motivo(self, valor): self._motivo = valor
        
    @property
    def fecha(self): return self._fecha
    @fecha.setter
    def fecha(self, valor): self._fecha = self.validar_fecha(valor)
            
    @property
    def estado(self): return self._estado
    @estado.setter
    def estado(self, valor): self._estado = valor
        
        
    # Valida que la fecha tenga formato correcto y que no sea anterior al momento actual.
    def validar_fecha(self, fecha):
        try:
            fecha_validada = datetime.datetime.strptime(fecha,"%d/%m/%Y %H:%M")

            if fecha_validada < datetime.datetime.now():
                raise DatoInvalidoError("Esta fecha ya a ha pasado")

            return fecha_validada
        except ValueError:
            raise DatoInvalidoError(f"Formato de fecha '{fecha}' incorrecto")
        
        
    # Cambia el estado de la cita a Realizada.
    def finalizar_cita(self):
        self.estado = "Realizada"
        self.paciente.anadirCita(self) 
        self.medico.anadirCita(self)
        
    # Devuelve un resumen de la cita.
    def descripcion(self):
        fecha = self.fecha.strftime("%d/%m/%Y a las %H:%M")
        
        return (f"   CITA ({self.estado})\n"
                f"   Paciente: {self.paciente.nombre} | Dr: {self.medico.nombre}\n"
                f"   Fecha: {fecha} | Motivo: {self.motivo}")


# Clase Hospital para gestionar médicos, pacientes y citas.

class Hospital:
    
    lista_hospitales = []
    
    # Crea un hospital y lo añade a la lista global de hospitales.
    def __init__(self, nombre):
        self.nombre = nombre
        self.pacientes = []
        self.medicos = []
        self.citas = []
        Hospital.registrar_hospital(self)
        
    
    # Getters y Setters de la clase Hospital
    
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, valor): self._nombre = valor

    @property
    def pacientes(self): return self._pacientes
    @pacientes.setter
    def pacientes(self, valor): self._pacientes = valor

    @property
    def medicos(self): return self._medicos
    @medicos.setter
    def medicos(self, valor): self._medicos = valor

    @property
    def citas(self): return self._citas
    @citas.setter
    def citas(self, valor): self._citas = valor


    # Metodos de clase para gestionar la lista de hospitales 
    
    # Añade un hospital a la lista estática, evitando duplicados por nombre.
    @classmethod
    def registrar_hospital(cls,hospital):
        if any(h.nombre == hospital.nombre for h in cls.lista_hospitales):
            print(f"\nEl hospital {hospital.nombre} ya está registrado.\n")
        else:
            cls.lista_hospitales.append(hospital)
            print(f"\nEl hospital {hospital.nombre} ha sido registrado.\n")
            
    
    # Muestra todos los hospitales disponibles en el sistema.
    @classmethod
    def mostrar_hospitales(cls):
        print("\n--- HOSPITALES REGISTRADOS ---\n")
        if not cls.lista_hospitales:
             print("No hay hospitales registrados.\n")
        else:
            for hospital in cls.lista_hospitales:
                print(f"Nombre: {hospital.nombre} | Médicos: {len(hospital.medicos)} | Pacientes: {len(hospital.pacientes)}")
        print("\n\n")
            
            
    # Devuelve la cantidad de hospitales registrados.
    @classmethod
    def len_hospitales(cls):
        return len(cls.lista_hospitales)
        
    
    # Registra un médico en la lista del hospital actual, verificando DNI.
    def registrar_medico(self, medico):
        if any(m.dni == medico.dni for m in self.medicos):
            print(f"\nEl médico con DNI {medico.dni} ya está registrado.\n")    
        else:
            self.medicos.append(medico)
            print(f"\nDr/a {medico.nombre} registrado exitosamente.\n")


    # Registra un paciente en la lista del hospital actual, verificando DNI.
    def registrar_paciente(self, paciente):
        if any(p.dni == paciente.dni for p in self.pacientes):
            print(f"\nEl paciente con DNI {paciente.dni} ya está registrado.\n")    

        else:
            self.pacientes.append(paciente)
            print(f"\nPaciente {paciente.nombre} registrado exitosamente.\n")   

    # Busca un médico por nombre (ignorando mayúsculas/minúsculas).
    def buscar_medico_por_nombre(self, nombre):
        for medico in self.medicos:
            if medico.nombre.lower() == nombre.lower():
                return medico
        raise DatoInvalidoError(f"No se encontró ningún médico con el nombre '{nombre}'.\n")
    
    # Busca un paciente por nombre (ignorando mayúsculas/minúsculas).
    def buscar_paciente_por_nombre(self, nombre):
        for paciente in self.pacientes:
            if paciente.nombre.lower() == nombre.lower():
                return paciente
        raise DatoInvalidoError(f"No se encontró ningún paciente con el nombre '{nombre}'.\n")
    
    # Muestra la lista de médicos del hospital actual.
    def mostrar_medicos(self):
        print(f"\n--- MÉDICOS DEL HOSPITAL {self.nombre.upper()} ---\n")
        if not self.medicos:
            print("No hay médicos registrados aún.")
            return False
        
        for medico in self.medicos:
            print(f"Nombre: {medico.nombre}, DNI: {medico.dni}, Especialidad: {medico.especialidad}")
        print("\n")
        return True
                
    # Muestra la lista de pacientes del hospital actual.
    def mostrar_pacientes(self):
        print(f"\n--- PACIENTES DEL HOSPITAL {self.nombre.upper()} ---\n")
        if not self.pacientes:
            print("No hay pacientes registrados aún.")
            return False

        for paciente in self.pacientes:
            print(f"Nombre: {paciente.nombre}, DNI: {paciente.dni}, Edad: {paciente.edad}")
        print("\n")
        return True




# -- METODOS GLOBALES / CONTROLADOR --

# Solicita al usuario una opción numérica y maneja errores de entrada no numérica.
def obtener_opcion():
    try:
        opcion = int(input("Seleccione una opción del menú: "))
        return opcion
    except ValueError:
        return -1 


# Imprime las opciones del menú principal y devuelve la elección del usuario.
def menu():
    print("\n----- MENÚ DE GESTIÓN DE CLÍNICA MÉDICA -----\n")
    print("1. Registrar Hospital") 
    print("2. Seleccionar Hospital a Gestionar") 
    print("3. Registrar Paciente") 
    print("4. Registrar Médico") 
    print("5. Pedir Cita") 
    print("6. Asignar un Medico a un Paciente")
    print("-------------")
    print("7. Atender a un paciente")
    print("8. Ver Historial Clínico de un Paciente") 
    print("9. Ver Pacientes de un Médico") 
    print("10. Ver Citas de un Paciente o Médico") 
    print("11. Mostrar Pacientes del Hospital Actual") 
    print("12. Mostrar Médicos del Hospital Actual") 
    print("-------------")
    print("13. Mostrar Hospitales Registrados") 
    print("14. Salir")
    print("---------------------------------------------")
    return obtener_opcion()


# Controlador que ejecuta la lógica correspondiente a la opción elegida del menú.
def opciones_menu(opcion):
    
    global hospital_actual
    
    # Comprobaciones de seguridad para obligar a seleccionar hospital
    if opcion != 1 and opcion != 2 and opcion != 13 and opcion != 14:
        if hospital_actual is None:
             print("\nATENCIÓN: No ha seleccionado ningún hospital.")
             print("Por favor, registre uno (Opción 1) o seleccione uno existente (Opción 2).\n")
             return

    if opcion == 1:
        hospital = registrar_hospital()
        if hospital_actual is None:
            hospital_actual = hospital
    elif Hospital.len_hospitales() == 0 and opcion != 14:
        print("\nPrimero debe registrar un hospital.\n")
  
    else:
        if opcion == 2:
            seleccionar_hospital()
        elif opcion == 3:
            registrar_paciente()
        elif opcion == 4:
            registrar_medico()
        elif opcion == 5:
            registrar_cita(None) 
        elif opcion == 6:
            asignar_medico_a_paciente()    
        elif opcion == 7:
            atender_paciente()      
        elif opcion == 8:
            mostrar_historial_paciente()
        elif opcion == 9:
            mostrar_pacientes_medico()           
        elif opcion == 10:
            mostrar_citas_persona()        
        elif opcion == 11:
            mostrar_pacientes_hospital()    
        elif opcion == 12:
            mostrar_medicos_hospital()    
        elif opcion == 13:
            Hospital.mostrar_hospitales()
        else:
            print("\nOpción no válida. Intente nuevamente.")

 
# Metodos de registro y adicion de citas 

# Pide nombre y crea instancia de Hospital.
def registrar_hospital():
    nombre=input("\nIngrese el nombre del hospital: \n")
    hospital=Hospital(nombre)
    return hospital
    
# Solicita datos para crear un Paciente. Usa recursividad en caso de error.
def registrar_paciente():
    global hospital_actual
    
    print("\n--- REGISTRO DE PACIENTE ---")
    try:
        dni=input("Ingrese el DNI del paciente: \n")
        if existe_paciente_o_medico(dni):
            print("\nEl DNI ya está registrado. Inténtelo de nuevo.\n")
            registrar_paciente() 
            return

        nombre=input("Ingrese el nombre del paciente: \n")
        edad_str=input("Ingrese la edad del paciente: \n")
        
        if not edad_str.isdigit():
             raise ValueError("La edad debe ser un número entero.")
        edad = int(edad_str)
        
        genero=input("Ingrese el género del paciente (M,F,O): \n")
        correo=input("Ingrese el correo del paciente: \n")
        telefono=input("Ingrese el teléfono del paciente: \n")
        
        # Validamos al crear el objeto
        paciente=Paciente(dni, nombre, edad, genero, correo, telefono)
        
        hospital_actual.registrar_paciente(paciente)
        
        # Opcional: añadir cita inmediatamente
        tiene_cita=input("¿Desea añadir una cita ahora? (s/n): \n").lower()
        if tiene_cita == 's':
            anadir_cita_p('s', paciente)
        
    except (DatoInvalidoError, Exception) as e:
        print(f"\nERROR DE DATOS: {e}")
        print("Reiniciando formulario de paciente...\n")
        registrar_paciente() # Recursividad
        return 

    except ValueError as e:
        print(f"\nERROR DE FORMATO: {e}")
        registrar_paciente() 
        return 


# Solicita datos para crear un Médico. Usa recursividad en caso de error.
def registrar_medico():
    global hospital_actual
    
    print("\n--- REGISTRO DE MÉDICO ---")
    try:
        dni=input("Ingrese el DNI del médico: \n")
        if existe_paciente_o_medico(dni):
            print("\nEl DNI ya está registrado.\n")
            registrar_medico()
            return 

        nombre=input("Ingrese el nombre del médico: \n")
        edad_str=input("Ingrese la edad del médico: \n")
        
        if not edad_str.isdigit():
             raise ValueError("La edad debe ser un número entero.")
        edad = int(edad_str)

        genero=input("Ingrese el género del médico (M,F,O): \n")
        correo=input("Ingrese el correo del médico: \n")
        telefono=input("Ingrese el teléfono del médico: \n")
    
        mostrar_especialidades()
        especialidad=input("Ingrese la especialidad del médico: \n")
        
        medico=Medico(dni, nombre, edad, genero, correo, telefono, especialidad)
        hospital_actual.registrar_medico(medico)

    except (DatoInvalidoError, Exception) as e:
        print(f"\nERROR: {e}")
        registrar_medico()
        return 
        
    except ValueError as e:
        print(f"\nERROR DE FORMATO: {e}")
        registrar_medico()
        return 
    
 

# Crear citas. Dirige a médico o paciente según la elección.
def registrar_cita(usuario):
    global hospital_actual
    
    if usuario is None:
        usuario = input("¿Para quién es la cita? (p: paciente, m: médico): ").lower()

    if usuario == 'p':
            try:
                paciente_nombre = input("Ingrese el nombre del paciente para la cita: \n")
                paciente= hospital_actual.buscar_paciente_por_nombre(paciente_nombre)
                anadir_cita_p('s', paciente)
                
            except (DatoInvalidoError, Exception) as e:
                print(f"\nERROR: {e}")
                registrar_cita('p')
                return
    
    elif usuario == 'm':
            try:
                medico_nombre = input("Ingrese el nombre del médico para la cita: \n")
                medico= hospital_actual.buscar_medico_por_nombre(medico_nombre)
                anadir_cita_m('s', medico)
            except (DatoInvalidoError, Exception) as e:
                print(f"\nERROR: {e}")
                registrar_cita('m') 
                return
    else:
        print("Opción no válida. Intente de nuevo.")
        registrar_cita(None)
        return
    
    
    
# Añadir citas desde la perspectiva del PACIENTE.
def anadir_cita_p(repetir, paciente):
    global hospital_actual
    
    while repetir.lower() == 's':
        if hospital_actual.mostrar_medicos():
            
            try:
                medico_nombre=input("Ingrese el nombre del médico: \n")
                medicoO = hospital_actual.buscar_medico_por_nombre(medico_nombre)

                fecha=input("Ingrese la fecha de la cita (dd/mm/yyyy): \n")
                hora=input("Ingrese la hora de la cita (hh:mm): \n")
                motivo=input("Ingrese el motivo de la cita: \n")
                
                # Esto puede lanzar error si la fecha es inválida
                Cita(paciente, medicoO, f"{fecha} {hora}", motivo)
        
                print(f"\nCita añadida para el paciente {paciente.nombre} con el médico {medicoO.nombre}")
                repetir=input("¿Desea añadir más citas? (s/n): \n")
            
            except (DatoInvalidoError, Exception) as e:
                print(f"\nERROR EN LA CITA: {e}")
                print("Inténtelo de nuevo.\n")

                continue 
        else:
            repetir='n'
        
# Añadir citas desde la perspectiva del MÉDICO.
def anadir_cita_m(repetir, medico):
    global hospital_actual
    
    while repetir.lower() == 's':
        if hospital_actual.mostrar_pacientes():
            
            try:
                paciente_nombre=input("Ingrese el nombre del paciente: \n")
                pacienteO = hospital_actual.buscar_paciente_por_nombre(paciente_nombre)

                fecha=input("Ingrese la fecha de la cita (dd/mm/yyyy): \n")
                hora=input("Ingrese la hora de la cita (hh:mm): \n")
                motivo=input("Ingrese el motivo de la cita: \n")
                
                Cita(pacienteO, medico, f"{fecha} {hora}", motivo)
        
                print(f"\nCita añadida para el paciente {pacienteO.nombre} con el médico {medico.nombre}")
                repetir=input("¿Desea añadir más citas? (s/n): \n")

            except (DatoInvalidoError, Exception) as e:
                print(f"\nERROR EN LA CITA: {e}")
                print("Inténtelo de nuevo.\n")
                continue
        else:
            repetir='n'


# Metodos de visualizacion y validación

# Muestra la lista de especialidades disponibles.
def mostrar_especialidades():
    print("\n--- ESPECIALIDADES MÉDICAS DISPONIBLES ---\n")
    for especialidad in Medico.lista_especialidades:
        print(f"- {especialidad}")
    print("\n\n")
    
    
# Verifica si el DNI ya existe en la lista de pacientes o médicos del hospital actual.
def existe_paciente_o_medico(dni):
    global hospital_actual
    
    if hospital_actual is None: return False

    for paciente in hospital_actual.pacientes:
        if paciente.dni == dni:
            return True
    
    for medico in hospital_actual.medicos:
        if medico.dni == dni:
            return True
    
    return False
    
# Permite al usuario cambiar el hospital que se está gestionando actualmente.
def seleccionar_hospital():
    global hospital_actual
    
    Hospital.mostrar_hospitales()
    nombre_buscar = input("Ingrese el nombre del hospital a gestionar: ")
    
    for hospital in Hospital.lista_hospitales:
        if hospital.nombre == nombre_buscar:
            hospital_actual = hospital 
            print(f"\n--- Ahora estás gestionando: {hospital.nombre} ---\n")
            return
            
    print("Hospital no encontrado.\n")
    
# Permite a un médico realizar un diagnóstico a un paciente, añadiendo el registro al historial clínico del paciente.

def atender_paciente():
    global hospital_actual
    
    
    if hospital_actual.mostrar_medicos():
        nombre_medico = input("Nombre del médico que pasará consulta: ")
        try:
            medico = hospital_actual.buscar_medico_por_nombre(nombre_medico)
            
            
            print(f"\n--- PACIENTES CON CITA PARA EL DR/A. {medico.nombre} ---")
            pacientes_con_cita = []
            
            if not medico.citas:
                print("Este médico no tiene citas programadas.")
                return
            
            
            for fecha, cita in medico.citas.items():
                if cita.estado == "Pendiente":
                    print(f"- Paciente: {cita.paciente.nombre} | Fecha: {fecha}")
                    pacientes_con_cita.append(cita.paciente.nombre.lower())

            if not pacientes_con_cita:
                print("No hay citas pendientes para atender.")
                return

            
            nombre_p = input("\nIngrese el nombre del paciente a atender: ")
            
            if nombre_p.lower() in pacientes_con_cita:
                paciente = hospital_actual.buscar_paciente_por_nombre(nombre_p)
                
                diagnostico = input("Ingrese el diagnóstico: ")
                informe = input("Ingrese el informe detallado: ")
                
                
                medico.realizar_diagnostico(paciente, diagnostico, informe)
                
               
                for fecha, cita in medico.citas.items():
                    if cita.paciente.nombre.lower() == nombre_p.lower() and cita.estado == "Pendiente":
                        cita.finalizar_cita()
                        break
            else:
                print("El paciente indicado no tiene una cita pendiente con este médico.")

        except DatoInvalidoError as e:
            print(f"Error: {e}")
    
# 
  
def asignar_medico_a_paciente(): # Cambié el nombre para no confundir con el método de la clase
    global hospital_actual
    
    print("\n---- ASIGNAR MÉDICO A PACIENTE ----")
    
    if not hospital_actual.mostrar_pacientes(): return
    nombre_p = input("Introduzca el nombre del paciente: ")
    
    try:
        paciente = hospital_actual.buscar_paciente_por_nombre(nombre_p)
        
        if not hospital_actual.mostrar_medicos(): return
        nombre_m = input("Introduzca el nombre del médico que desea asignarle: ")
        medico = hospital_actual.buscar_medico_por_nombre(nombre_m)
        

        paciente.asignar_medico(medico)
        
        # También es buena idea que el médico sepa que tiene ese paciente
        medico.pacientes_asignados.append(f"{paciente.nombre} (DNI: {paciente.dni})")

    except DatoInvalidoError as e:
        print(f"Error: {e}")
    
# Pide el nombre de un paciente y muestra su historial si existe.
def mostrar_historial_paciente():
    global hospital_actual
    
    if hospital_actual.mostrar_pacientes():
        nombre_buscar = input("Ingrese el nombre del paciente para ver su historial clínico: ")
        
        for paciente in hospital_actual.pacientes:
            if paciente.nombre.lower() == nombre_buscar.lower():
                paciente.ver_historial()
                return
            
        print("Paciente no encontrado.\n")
    

# Pide el nombre de un médico y muestra sus pacientes asignados.
def mostrar_pacientes_medico():
    global hospital_actual
    
    if hospital_actual.mostrar_medicos():
        nombre_buscar= input("Ingrese el nombre del médico para ver sus pacientes asignados: ")
        
        for medico in hospital_actual.medicos:
            if medico.nombre.lower() == nombre_buscar.lower():
                medico.ver_pacientes()
                return
        print("Médico no encontrado.\n")
    
        
        
# Muestra las citas filtrando por médico o por paciente según elección.
def mostrar_citas_persona():
    global hospital_actual
    
    tipo = input("¿Desea ver las citas de un paciente o un médico? (p/m): ").lower()
    
    if tipo == 'p':
        if hospital_actual.mostrar_pacientes():
            nombre_buscar = input("Ingrese el nombre del paciente para ver sus citas: ")
            
            for paciente in hospital_actual.pacientes:
                if paciente.nombre.lower() == nombre_buscar.lower():
                    paciente.mostrar_citas()
                    return
            print("Paciente no encontrado.\n")
    
    elif tipo == 'm':
        if hospital_actual.mostrar_medicos():
            nombre_buscar = input("Ingrese el nombre del médico para ver sus citas: ")
            
            for medico in hospital_actual.medicos:
                if medico.nombre.lower() == nombre_buscar.lower():
                    medico.mostrar_citas()
                    return
            print("Médico no encontrado.\n")
    
    else:
        print("Opción no válida. Por favor, ingrese 'p' para paciente o 'm' para médico.\n")
    
    
# Mostrar pacientes del hospital actual.
def mostrar_pacientes_hospital():
    global hospital_actual
    hospital_actual.mostrar_pacientes()
    
# Mostrar médicos del hospital actual.
def mostrar_medicos_hospital():
    global hospital_actual
    hospital_actual.mostrar_medicos()
    

#-- PROGRAMA PRINCIPAL --

# Función principal: bucle del menú y manejo de excepciones generales.
def main():
    global hospital_actual
    hospital_actual = None
    
    opcion = menu()
    while opcion != 14:
        try:
            opciones_menu(opcion)
            
        except DatoInvalidoError as e:
            print(f"\nERROR DE VALIDACIÓN: {e}")
            
        except Exception as e:
            print(f"\nOCURRIÓ UN ERROR INESPERADO: {e}")
            
        opcion = menu()


#Punto de entrada del programa, llama a la funcion main"""
if __name__ == "__main__":
    main()