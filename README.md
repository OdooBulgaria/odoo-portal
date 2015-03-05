# Modulos Portal Odoo 8


## security_portal
Este modulo hace los siguientes cambios:
* Crea un grupo llamado portal manager que hereda los permisos del grupo portal.
* Modifica los permisos de los menus disponibles en portal para que:
    * Portal user:
        * Bandeja de entrada.
        * Incidencias.
    * Portal manager:
        * Bandeja de entrada.
        * Presupuestos.
        * Pedidos.
        * Facturas.
        * Proyectos.
        * Incidencias.
* Modifica el formulario de alta de acceso al portal, para poder asignar contactos
al grupo portal manager.


## followers_portal
Modulo para añadir como seguidores en los pedidos de ventas y las facturas, los 
usuarios que pertenezcan al grupo Portal Manager.

