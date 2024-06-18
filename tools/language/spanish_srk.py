# -*- coding: utf-8 -*-

# Main Menu
title_main = "Menú principal"
title_choose = "Selecciona un proyecto:"
title_delete = "Eliminar proyectos:"
title_extract = "Opciones de extracción:"
menu_create = "Crea un nuevo proyecto"
menu_choose = "Elige un proyecto diferente"
menu_delete = "Eliminar un proyecto"
menu_extract = "Extraer ROM"
menu_updates = "Buscar actualizaciones"
menu_misc = "Herramientas varias"
menu_boot_recovery = "Herramientas Boot / Recovery"
menu_rom_tools = "Menú de herramientas ROM"
menu_new = "Nuevo proyecto"
menu_quit = "Abandonar"
menu_back = "Volver"
menu_skip = "Omitir"

# ROM Tools Menu
menu_deodex = "Opción Deodexar ROM"
menu_perm_type = "Cambiar el tipo de permisos"
menu_root = "Menú Root"
menu_asserts = "Menú Asserts"
menu_extra_dir = "Menú extra del directorio"
menu_rom_debloat = "Menú Debloat"
menu_build_menu = "Menú de compilación"

# Startup
startup_project = "PROYECTO ACTUAL: "
startup_version = "VERSIÓN DE ANDROID: "
startup_mdepend = "FALTAN DEPENDENCIAS: "
startup_need_java = "Necesitas al menos Java 8 para usar esta cocina."
startup_copy_extract = "Copia tu firmware al directorio"
startup_copy_extract2 = "del proyecto y elije la opción 4 para extraerlo."
startup_title_no_rom = "Sin ROM"
startup_no_projects = "No hay proyecto para trabajar."
startup_prep_updater_script = "Preparación del script de actualización ..."
startup_no_rom = "No hay ROM para trabajar."
startup_srkuser = "Inserte el nombre de usuario de su cocina (no el correo electrónico): "
startup_srkuser_pass = "Contraseña de cocina: "
startup_srkuser_error = "No inserte su correo electrónico, solo el nombre de usuario."
startup_srkuser_error2 = "no se encontró en la base de datos de la cocina, o"
startup_srkuser_error3 = "la contraseña fue incorrecta. Asegúrate de escribir"
startup_srkuser_error4 = "el nombre de usuario / contraseña que usaste cuando"
startup_srkuser_error5 = "registraste la cocina."
startup_srkuser_noauth = "Este PC no tiene Autorización."
startup_srkuser_unknown = "Se ha producido un error desconocido. Por favor, póngase en contacto con SuperR."
startup_srkuser_q = "¿Es este el nombre de usuario de tu cocina? y / n"
startup_srkpass_q = "¿Deseas guardar tu contraseña? y / n"
startup_error = "Algo está mal en la instalación. Prueba con una nueva instalación."
startup_checksum = "Las siguientes sumas de comprobación no coinciden:"
startup_environ_error = "La cocina no puede funcionar en este sistema"
startup_vdisk_error = "La cocina no se puede ejecutar en un disco virtual en modo Live"
startup_remdisk_error = "La cocina no se puede ejecutar en un disco extraíble en modo Live"
startup_wsl_warning = "Estás usando la cocina en WSL1."
startup_wsl_warning2 = " Se recomienda WSL2 para habilitar todas las capacidades de la cocina."
startup_wsl2_warning = "La cocina no se está ejecutando en el directorio /home."
startup_wsl2_warning2 = "Esto puede causar errores de permisos de Windows y lentitud general."
startup_win_warning = "La cocina nativa de Windows se está eliminando gradualmente."
startup_win_warning2 = "WSL2 es la manera perfecta de ejecutar la cocina Linux en Windows."

# Build
menu_build_zip = "Empaquetar zip completo de la ROM"
menu_sys_img = "Empaquerar EXT4 img"
menu_sign = "Firmar el zip"
donate_menu_zipalign = "Hacer Zipalign a las apk"
donate_menu_custom_id = "Personalizar ro.build.display.id"
menu_custom_zip = "Menú zip personalizado"
build_selinux_error = "O bien el Kernel no es compatible con Selinux, o"
build_selinux_error2 = "la cocina no puede encontrar lo que necesita. Si estás seguro de que tu"
build_selinux_error3 = "dispositivo es compatible con selinux, puedes copiar el archivo_contexts"
build_selinux_error4 = "desde ramdisk a tu directorio 00_project_files"
build_selinux_error5 = "para usar esta característica."
build_selinux_error6 = "Por ahora, necesitarás usar set_perm o raw_img."
build_patient = "Esto puede tardar un rato. Por favor se paciente ..."
build_prep_img = "Preparando archivos para la creación de img ..."
build_check_ziplog = "Algo salió mal. Comprueba el archivo zip.log para ver los errores."
build_prep_sys_img = "Preparación de archivos para la creación img EXT4 ..."
build_img_error = "Hubo un problema al crear la imagen."
build_img_which = "¿Qué versión img EXT4 quieres crear?"
build_img_nocon = "La cocina no encontró el archivo file_contexts."
build_img_nocon2 = "Asegúrate que el archivo boot.img está en el directorio del proyecto, o copia"
build_img_nocon3 = "file_contexts en el directorio de tu proyecto 00_project_files"
build_img_nocon4 = "e intentalo de nuevo."
build_no_zip = "No hay zip para firmar."
build_no_boot_q = "Tu ROM no contiene un archivo boot.img o kernel.img / ramdisk.img."
build_no_boot_q2 = "¿Te gustaría continuar de cualquier modo? y / n"
build_cho_zip = "Elije el zip para firmar: "
build_man_img_size = "Quieres usar el siguiente tamaño?  y/n"
zipalign_q = "¿Quieres hacer zipalign antes de empaquetar el zip? y / n"
zipalign = "Haciendo Zipalign"
zipalign_frame_q = "¿Quieres hacer zipalign a los archivos apk en / framework? y / n"
zipalign_complete = "Zipalign completo"
donate_bdisplay = "¿Qué deseas mostrar en la pantalla de compilación?"

# Custom zip
title_cho_cust_zip = "Elige un zip personalizado para compilar:"
cust_deldir_q = "¿Quieres que el zip elimine los directorios"
cust_deldir_q2 = "existentes antes de flashear? y / n"
cust_meta_prep = "Preparación del directorio META-INF ..."
cust_not_exist = "Uno o más directorios que deseas comprimir no existen."
cust_dir_info = "Asegúrate de tener al menos uno de los siguientes"
cust_file_check = "Asegúrate de tener system, META-INF y boot.img dentro"
cust_prep = "Preparando los archivos..."
cust_convert_binary_q = "¿Quieres convertir el updater-script"
cust_convert_binary_q2 = "en un update-binary? y / n"
cust_convert_binary = "Convirtiendo updater-script a update-binary ..."

# Debloat
menu_debloat = "Hacer Debloat a la ROM"
menu_debloat_cust = "Debloat personalizado"
menu_debloat_knox = "Eliminar Samsung Knox"
menu_debloat_restore = "Restaurar Bloat / Knox"
menu_debloat_refresh = "Actualizar el estado del Debloat"
bloat_already_debloated = "Esta ROM ya está Debloated"
bloat_list_menu = "Lista de archivos que se eliminarán"
bloat_list_files = "Los siguientes archivos se eliminarán:"
bloat_rem = "Eliminando Bloat ..."
bloat_moved = "Bloat ha sido movido a: "
bloat_cust_info = "Agregue contenido a uno de los siguientes archivos para usar esta función"
bloat_knox_not_exist = "Knox No existe en esta ROM"
bloat_knox_rem = "Quitando knox ..."
bloat_knox_moved = "Knox ha sido movido a: "
bloat_no_files_restore = "No hay archivos para restaurar"
bloat_restore = "Restaurando Bloat ..."
bloat_has_restored = "Los archivos Bloat han sido restaurados."
bloat_restore_q = "¿Quieres restaurar los archivos Bloat? y / n"
debloated = "Debloated"
bloated = "Bloated"
bloat_dir_emply = "bloat_custom está VACÍO"

# Root
title_cho_root_zip = "Elija Root Zip:"
menu_root_method = "¿Qué método de root prefieres?"
menu_ss_method = "¿Qué tipo de instalación de SuperSU quieres?"
menu_supersucho = "Deja que SuperSU decida"
menu_system_install = "Instalación del sistema (SYSTEMLES = false)"
menu_inject = "Inyectar cambios de sepolicy e instalación del sistema"
menu_download_inject = "Descargar / Instalar inject-sepolicy-addon"
menu_root_unroot = "Root / Unroot ROM"
menu_busybox = "Busybox Agregar / Eliminar"
menu_add_remove_sud = "Agregar / quitar soporte de su.d"
root_already = "Ya tienes root"
root_must_add = "Debes agregar root primero."
busybox_already = "Ya tienes Busybox."
busybox_q = "Quieres agregar Busybox a la ROM? y / n"
root_sud_add_q = "¿Quieres agregar su.d a la rom? y / n"
root_sud_rem_q = "¿Quieres eliminar el soporte de su.d? y / n"
root_supersu_q = "SuperSU es un proyecto sin desarrollo. ¿Está seguro de que desea agregarlo?  y/n"
root_remove = "Quitando root ..."

# General
general_remove_q = "Quieres eliminarlo? y / n"
general_continue_q = "¿Quieres continuar? y / n"
general_cont_anyway_q = "¿Sequro quieres continuar de cualquier modo? y / n"
general_extracting = "Extrayendo "
general_create = "ha sido creado en "
general_build = "está creandose en "
no_python = "Debe instalar Python3.5 o superior para usar esta característica."
more_info_link = "Visita el siguiente link para más información:"
spaces_not_allowed = "No se permiten espacios"

# Status
enabled = "Habilitado"
disabled = "Deshabilitado"
add_support = "Añadir soporte"
yes = "Sí"
no = "No"
secure = "Seguro"
insecure = "Inseguro"
no_knox = "No Knox"
knox = "Knox existe"
no_root = "Sin Root"

# Boot/Recovery Tools
title_boot = "Menú de herramientas Boot / Recovery"
title_cho_boot = "Elija boot o recovery img"
title_unpack = "Extraer para más opciones"
title_current = "ACTUALMENTE: "
menu_pack_boot = "Empacando  "
menu_insecure = "Inseguro / Seguro el "
menu_dmverity = "Eliminar dm-verity"
menu_forcee = "Agregar / Eliminar Forceencrypt"
menu_deopatch = "Parchear sepolicy para Oreo deodex"
menu_deopatch_fail = "El parche falló, o sepolicy ya ha sido parcheado"
menu_deopatch_sepol = "sepolicy no fue encontrado"
menu_deopatch_add = "sepolicy ha sido parcheado para Oreo deodex"
menu_unpack = "Extraer "
menu_boot_flashable = "Crear flasehable para "
menu_boot_restore = "Restaurar a origen: "
menu_switch_boot = "Cambiar entre Boot / Recovery"
boot_repack = "Recompilando "
boot_repack_problem = "Hubo un problema al recompilar"
boot_packed_d = " es el archivo"
boot_no_img = "No hay boot.img o recovery.img en "
boot_prop_warn = "Copia el build.prop en el directorio del proyecto y vuelve a intentarlo."
boot_prep_build = "Preparándose para crear ..."
boot_unpack = "Desempacando "
boot_unpack_problem = "Hubo un problema al desempacar tu "
boot_unpack_noram = "No hay ramdisk en este boot.img."
boot_need_img = "Necesitas un img para este proceso."
boot_permission_error = "Hay un error de permisos. Comprueba el boot.log"
boot_permission_error2 = "Este post proporciona soluciones: "
# Plugin Manager
menu_plugin_menu = "Menú de plugins (complementos)"
menu_plugin_run = "Ejecutar un plugin"
menu_plugin_install = "Instalar un plugin"
menu_plugin_delete = "Eliminar un plugin"
menu_plugin_updates = "Verificar actualizaciones de los plugins descargados"
menu_plugin_updates_info = "Actualizaciones disponibles: "
menu_plugin_get = "Obteniendo lista de plugins ..."
menu_plugin_bashwin = "No puede ejecutar Bash plugins en Windows. Utilizar el"
menu_plugin_bashwin2 = "administrador de plugins para eliminar y reinstalar la versión correcta."

# Misc Tools Menu
title_misc = "Menú de herramientas"
menu_language = "Restablecer idioma"
menu_heapsize = "Menú tamaño asignación Java"
menu_support = "Soporte: Crear zip para enviar"
menu_zip_devices = "Dispositivo Zip / capfiles para compartir"
menu_ubinary = "Opciones de zip flashable"
menu_flashable = "Opciones de zip flashable (global)"
menu_extract_options = "Opciones de extracción"
menu_mount_extract = "Utiliza el montaje de exracción para archivos .img"
menu_case_fix = "Corrección de nombres de archivos que no distinguen entre mayúsculas y minúsculas"
menu_extract_all_img = "Extraer e incluir todos los archivos img"
menu_tools_reset = "Restablecer todas las herramientas"
menu_tools_reset_go = "Eliminando todas las herramientas ..."
menu_device_reset = "Actualizar la base de datos"
menu_choose_server = "Ubicación del servidor principal"
menu_ext4exe = "Utilizar make_ext4fs.exe"
menu_zip_compression = "Nivel de compresión zip ROM"
menu_zip_compression2 = "Introduzca el nivel de compresión del zip deseado "
menu_tools_update = "La actualización se completará al reiniciar"
menu_offline_auth = "Menú autorización sin conexión"
menu_offline_renew = "Renovar la autorización sin conexión"
menu_offline_enable = "Activar/Desactivar autorización sin conexión"
menu_renew_now = "Renovar ahora"
auth_reset = "La autorización sin conexión se ha habilitado/renovado. La cocina tiene que reiniciarse."
auth_reset2 = "Se requiere acceso a Internet para el primer reinicio."
auth_max_days = "Máximo de días de autorización fuera de línea: "
auth_expired = "La sesión de autorización sin conexión ha caducado."
support_create = "Creando support.zip ..."
support_finish = "support.zip se ha creado en el directorio del proyecto"
support_finish_up = "support.zip ha sido cargado"
heapsize_q = "Ingresa el tamaño personalizado de uso en Java en MB. Debe ser"
heapsize_q2 = "menor que el tamaño de tu ram física total:"
heapsize_choose = "Que quieres hacer?"
heapsize_custom = "Cambiar el tamaño de asignación para java"
heapsize_reset = "Volver a la asignación predeterminada"
heapsize_num_error = "Debes introducir un número en MB (Ej. 1024)"
heapsize_error = "El tamaño de asignación debe ser igual o menor que el de"
heapsize_error2 = "la RAM física instalada."
physical_ram = "Tamaño de RAM Física: "
heapsize_auto = "Por defecto"
ask_b = "Preguntar siempre para la conversión a script update-binary"
ask_s = "Pregunta cuando quieras"
always_b = "Convertir siempre en script update-binary"
always_s = "Convertir siempre"
never_b = "Nunca convertir a script update-binary"
never_s = "Nunca convertir"
metasize = "Corto/largo set_metadata Updater-script (global)"
metasize_s = "Corto"
metasize_l = "Largo"
metasize_q = "¿Qué set_metadata Updater-script debemos utilizar?"
brotli_q = "¿Deseas utilizar compresión brotli (dat.br)?"
brotli_level = "Introduzce el nivel de compresión de brotli deseado "
brotli_menu = "Compresión Sparse_dat Brotli (dat.br)"

# Asserts
menu_add_assert = "Añadir / quitar dispositivo"
menu_asserts_custom = "Añadir Asserts, lineas de confirmación de dispositivo"
menu_asserts_remove = "Eliminar las lineas de confirmación de la ROM"
menu_asserts_reset = "Restablecer asserts por defecto"
asserts_no_assert = "No hay assert."
asserts_current = "ASSERTS ACTUALES DEL DISPOSITIVO: "
asserts_enter = "La confirmación del dispositivo, permite / o impide el flasheo de la ROM. Si"
asserts_enter2 = "pemites que la ROM se flashee en un dispositivo incorrecto puedes"
asserts_enter3 = "tener graves problemas. Quedas advertido :)"
asserts_enter4 = "Por favor introduce la información del dispositivo separado por comas."
asserts_enter5 = "El dispositivo actual ya debería estar en la lista"
asserts_enter6 = "pero aseguraté que lo está. Pulsa ENTER cuando termines."
asserts_prep = "Preparando lineas de confirmación de dispositivo..."
asserts_type = "Escribe tus lineas de confirmación personalizadas a continuación. Pulsa ENTER cuando termines."
asserts_cust_error = "La sintaxis debe ser "
asserts_prep_cust = "Preparando lineas de confirmación personalizadas ..."

# Extra Directory
menu_data = "/ data / app"
menu_cust_dir = "Personalizado"
menu_cctr = "No activo"
extra_data_added = "/ data / app support ha sido agregado. Coloque aplicaciones en:"
extra_already_data = "Ya tiene soporte para / data / app."
extra_already_data2 = "El directorio / data en tu proyecto se mantandrá."
extra_already_data3 = "¿Quieres eliminarlo? y / n"
extra_data_rem = "Soporte / data / app  ha sido eliminado"
extra_cust_name = "Escribe el nombre del directorio personalizado, luego pulsa ENTER."
extra_cust_loc = "¿Dónde se debe mostrar el directorio personalizado?"
extra_cust_name_q = "se incluirá en tu ROM. ¿Se debe mostrar en una partición? y / n"
extra_cust_setup = "Configuración"
extra_cust_add = "se ha agregado soporte"
extra_data = "tipos de permisos en data: "
extra_data_q = "¿Quieres agregar soporte a / data / app? y / n"
extra_data_perm = "Por favor elije el tipo de permisos de /data: "
extra_cust_already = " ya existe."

# Selection
select = "Selecciona: "
select_enter = "Selecciona y presiona ENTER: "

# Notices
example = "EJEMPLO: "
warning = "ADVERTENCIA: "
notice = "AVISO: "
missing = "ARCHIVOS PERDIDOS: "
current = "SELECCIONADO"
expires = "Expira: "
error = "ERROR: "
success = "COMPLETADO: "
error_mess = "Algo salió mal."

# Press ENTER
enter_rom_tools = "Pulsa ENTER para volver al menú herramientas de la ROM"
enter_continue = "Pulsa ENTER para continuar"
enter_main_menu = "Pulsa ENTER para volver al menú principal"
enter_boot_menu = "Pulsa ENTER para volver al menú Herramientas de Boot / Recovery"
enter_build_menu = "Pulsa ENTER para volver al menú de compilación"
enter_change_perm_menu = "Pulsa ENTER para volver al menú Cambiar Permisos."
enter_debloat_menu = "Pulsa ENTER para volver al menú Debloat"
enter_extra_dir_menu = "Pulsa ENTER para volver al menú Extra Directory"
enter_cho_another_detection = "Pulsa ENTER para elegir otro método de detección"
enter_ready = "Pulsa ENTER cuando estés listo"
enter_kitchen_updater = "Pulsa ENTER para volver al Actualizador de Cocina"
enter_misc_tools_menu = "Pulsa ENTER para volver al menú de herramientas"
enter_heapsize_menu = "Pulsa ENTER para volver al menú asignación memmoria Java"
enter_continue_extracting = "Pulsa ENTER para continuar extrayendo"
enter_try_again = "Pulsa ENTER para intentarlo de nuevo"
enter_root_menu = "Pulsa ENTER para volver al menú root"
enter_plug_menu = "Presiona ENTER para volver al administrador de complementos"
enter_exit = "Pulsa ENTER para salir"

# Perm Type
perm_title = "Menú Cambiar / Selecionar Permisos"
perm_set_metadata_cur = "set_metadata"
perm_set_metadata = "set_metadata (KitKat y superior)"
perm_set_perm = "set_perm (JellyBean y versiones inferiores)"
perm_sparse = "Sparse dat"
perm_sparse_red = "Sparse dat (no es compatible con este dispositivo)"
perm_raw_img = "raw_img"
perm_check_symlinks = "Comprobando symlinks ..."
perm_set_metadata_error = "Esta ROM NO es KitKat o superior"
perm_set_perm_error = "Esta ROM NO es JellyBean o inferior"
perm_changing_perm = "Cambiando el tipo de permisos ..."
perm_which = "¿Qué tipo de permisos deseas usar?"

# Delete Project
delete_has_been = " ha sido eliminado."
delete_q = "será borrado. ¿Continuar? y / n"

# Deodex
deodex_copy_frame_prop = "Debes copiar el directorio de framework y build.prop"
deodex_copy_frame_prop2 = "desde tu ROM a "
deodex_no_odex = "No hay archivos odex en esta rom."
deodex_no_boot_oat = "No hay boot.oat en esta rom. No se puede deodexar."
deodex_no_plat = "El deodexado de esta API no es compatible con esta plataforma"
deodex_no_valgrind = "Instala valgrind, y prueva de nuevo"
deodex_disclaimer = "Las ROM deodexadas pueden No funcionar. Puede tener"
deodex_disclaimer2 = "errores, puede que no arranque, o ambos. Se consciente de"
deodex_disclaimer3 = "esos problemas. A menos que sepas cómo solucionarlos,"
deodex_disclaimer4 = "por favor no postees sobre esto. Gracias :)"
deodex_use_method = "¿Qué método de deodex quieres usar?"
deodex_oat2dex_ver = "¿Qué versión de oat2dex quieres usar?"
deodex_oat2dex_official = "Oficial v0.86"
deodex_oat2dex_latest = "Último actualizado"
title_cho_oat2dex = "Elegir oat2dex: "
title_cho_smali = "Elegir smali: "
title_cho_baksmali = "Elegir baksmali: "
deodex_no_api = "La versión de Android no ha sido detectada."
deodex_config_arch = "Configura la arquitectura de tu dispositivo."
deodex_config_arch2 = "SUGERENCIA: "
deodex_config_arch3 = "Comprueba en el directorio de framework, se debería ver"
deodex_config_arch4 = "otro directorio dentro. El nombre debe estar"
deodex_config_arch5 = "ahí (ex. arm, arm64, x86)."
deodex_config_arch6 = "Si no puedes comprobar esto, comprueba lo siguiente:"
deodex_config_arch7 = "1. Asegúrate de escribir la variable de la arquitectura correctamente."
deodex_config_arch8 = "2. Asegúrate de que tu rom aún no esté deodexada."
deodex_config_arch9 = "Escribe la arquitectura de tu dispositivo y pulsa ENTER."
deodex_extract_txt = "Extrayendo archivos odex ..."
deodex_extract = "... Extrayendo "
deodex_move = "Mover aplicaciones adicionales ..."
deodex_deop = "Deoptimizando boot.oat ..."
deodex_start_app = "Empezando a deodexar / system / app ..."
deodex_start_priv = "Empezando a deodexar / system / priv-app ..."
deodex_start_frame = "Empezando a deodexar/ system/ framework ..."
deodex_deodexing = "... Deodexando"
deodex_app_already = "ya está deodexado ..."
deodex_clean = "Limpiando ..."
deodex_complete = "Deodexado completo"
deodex_remain = "Los siguientes archivos odex todavía están en su ROM"
deodex_method = "MÉTODO: "
deodex_problems = "Hubo problemas para deodexar"
deodex_problems2 = "y esto puede dar problemas si flasheas la ROM."
deodex_problems3 = "Has sido advertido: "
deodex_try_smali = "SUGERENCIA: Prueba con smali / baksmali"
deodex_api = "NIVEL API "
deodex_arch = "ARCO: "
deodex_arch2 = "ARCH2: "
deodex_move_odex = "Mover archivos odex ..."
deodex_try_anyway = "¿Te gustaría intentarlo de todos modos? y / n"
deodex_continue_q = "¿Te gustaría continuar con el deodex? y / n"
deodex_del_meta_inf_q = "Android Nougat utiliza la firmas de APK Scheme v2, y"
deodex_del_meta_inf_q2 = "esto puede causar problemas al deodexar. Eliminando"
deodex_del_meta_inf_q3 = "META-INF de los archivos apk debería solucionar este problema."
deodex_del_meta_inf_q4 = "¿Deseas eliminar el directorio META-INF de"
deodex_del_meta_inf_q5 = "todos los archivos apk de tu ROM? y / n"
deodex_del_meta_inf = "Eliminando META-INF de apk´s ..."
deodex_del_arch = "¿Deseas eliminar los directorios del framework mostrados a continuación? y / n"
deodex_pack_jar = "Empaquetando dex dentro de los archivo .jar ..."
deodex_server_disabled = "la conversión de CDex en el servidor está actualmente deshabilitada "
deodex_server_cdex = "convirtiendo cdex en el servidor... "
deodex_server_error1 = "Error en la subida"
deodex_server_error2 = "Error al mover el archivo al directorio de trabajo"
deodex_server_error3 = "Error de extracción del zip cdex"
deodex_server_error4 = "Error al crear la creación de zip dex en el servidor "
deodex_no_dex = "No hay dex en vdex. Saltar."

# Extract
extract_title = "Menú de extracción"
extract_no_files_message = "1) Añade una ROM en zip, tar / boot.img, system.img / boot.img o"
extract_no_files_message2 = "  win / boot.win y luego elige esta opción."
extract_no_files_message3 = "2) Extrae system, vendor, boot y recovery de tu"
extract_no_files_message4 = " dispositivo rooteado, o de tu archivo personalizado del recovery para su extracción."
extract_cho_option = "Elije la opción para extraer imágenes"
extract_cho_option2 = "** Si obtienes un error, puedes probar otra opción **"
extract_cho_option3 = "1) Mi dispositivo arranca en recovery personalizado (con el stock no funciona)"
extract_cho_option4 = "2) Mi dispositivo arranca en Android (debe estar rooteado)"
extract_plug = "** Conecta tu dispositivo"
extract_detect_part = "Detectando información de las particiónes ..."
extract_detect_part2 = "Si estás atascado aquí, prueba a cambiar a modo USB en"
extract_detect_part3 = "el dispositivo, cambiando de carga a modo transferencia de archivos (MTP)"
extract_pull_error = "Algo salió mal. Lo más probable es que no tengas permiso para"
extract_pull_error2 = "extraer imágenes de tu dispositivo."
extract_pulling = "Extrayendo "
extract_prep = "Preparándose para extraer ..."
extract_zip_fail = "Este zip no contiene nada que la cocina"
extract_zip_fail2 = "pueda extraer."
extract_zip = "Extrayendo zip ..."
extract_dat = "Extrayendo system.new.dat, system.transfer.list y boot.img ..."
extract_convert_br = "Descomprimiendo dat.br ..."
extract_convert_sys = "Convirtiendo a "
extract_img_from_zip = "Extrayendo imágenes desde el zip ..."
extract_tar_boot = "Extrayendo sistema.ext4.tar.a y boot.img ..."
extract_img = "Extrayendo imágenes ..."
extract_fail = "Algo salió mal en la extracción."
extract_tar_md5 = "Extrayendo archivos tar.md5 ..."
extract_chunk = "Extrayendo sparsechunks y boot.img ..."
extract_pbin = "Extrayendo payload.bin ..."
extract_multi = "Extrayendo sistema multi-part ..."
extract_convert_chunk = "Conversión de fragmentos sparse en archivos .img ..."
extract_fix_img = "Fijando "
extract_general = "Extrayendo a "
extract_check_firm = "Comprobando los archivos del firmware ..."
extract_tgz_fail = "El archivo tgz no parece ser"
extract_tgz_fail2 = "firmware oficial de Nexus."
extract_files = "Extrayendo archivos ..."
extract_md5_fail = "No hay system.img.ext4 en tu archivo tar.md5"
extract_xz_fail = "No hay system.img en este archivo xz"
extract_tar_fail = "Parece que el archivo .tar que tienes no es de una copia de seguridad nandroid"
extract_tar = "Extrayendo nombre"
extract_extra_extract_q = "¿Quieres extraer particiones adicionales (modem.bin, etc.)? y / n "
extract_cache_extract_q = "¿Quieres extraer cache.img? y / n "
extract_cache_include_q = "¿Quieres incluir los archivos de cache.img"
extract_cache_include_q2 = "al proyecto de tu rom? y / n"
extract_cache = "Incluyendo archivos cache.img ..."
extract_cache_fail = "No hay csc.zip en tu archivo cache.img"
extract_rom_fail = "Hubo un problema en la extracción de la ROM."
extract_rom_fail_ext4 = "El archivo imagen no parece ser válido en .ext4."
extract_cho_part_detect = "Elije el método de detección de tamaño de partición para"
extract_adb_shell = "tu dispositivo a través de adb shell"
extract_project_dir = "Directorio de proyectos (BETA): "
extract_manual = "Introducir manualmente"
extract_detect = "Determinando el tamaño de la partición para "
extract_beta = "Esta característica está en fase beta. Es posible que no se visualice correctamente."
extract_beta2 = "Puedes obtener un error como el siguiente: "
extract_beta3 = "blkdiscard failed: Argumento inválido"
extract_beta4 = "Puedes cambiar los permisos a set_metadata o set_perm a"
extract_beta5 = "evita el uso de esta función"
extract_manual_bytes = "Introduzce el tamaño de la partición en bytes para "
extract_detect_fail = " el tamaño de la partición está vacío o no es numérico. Inténtalo de nuevo."
extract_sparse_convert = "Convirtiendo sparse img..."
extract_img_fail = "No hay "
extract_copy_e = "Copiando archivos a "
extract_moved_old_rom = "Los siguientes han sido movidos a: "
extract_q = "Quieres extraer "
extract_q2 = " al proyecto actual? y / n"
extract_extra_extract = "¿Quieres extraer "
extract_extra_q = "?  y/n  "
extract_extra_include = "¿Quieres incluir los archivos de "
extract_extra_include_q = " al proyecto de tu rom? y / n"
extract_autorom_sudo = "Configurando sudo ahora para que AutoROM no se interrumpa"
extract_use_concat = "Utiliza el plugin Concatimg, luego extrae el System.img"

# by-name
byname_how_to_get_q = "¿Cómo quieres obtener la información de tu partición?"
menu_byname_detect_boot = "Detectar por el nombre de las imágenes de Boot / Recovery (recomendado)"
menu_byname_detect_device = "Detectar por el nombre de tu dispositivo"
menu_byname_detect_manual = "Introduce el nombre manualmente"
menu_byname_detect_mmc = "Detectar particiones mmcblk desde el recovery.img"
byname_usb_debug = "** Habilita la depuración usb en tu dispositivo Android en la configuración de ajustes"
byname_usb_debug2 = "** Conecta tu dispositivo"
byname_usb_debug_root = "Esta operación requiere ser root."
byname_usb_debug_root2 = "Es posible que debas aceptar la función root en tu dispositivo."
byname_error_device = "el nombre no pudo ser detectado desde su dispositivo."
byname_error_device2 = "Intenta detectar particiones mmc desde recovery.img"
byname_no_boot = "Copia boot.img, recovery.img o kernel.elf al"
byname_no_boot2 = "directorio del proyecto y vuelve a intentarlo."
byname_which_img_q = "¿Qué imagen quieres usar?"
byname_detect = "Detectando por nombre de "
byname_no_files = "Necesitas un archivo boot.img, recovery.img o kernel.elf para este proceso."
byname_boot_fail = "el nombre no pudo ser detectado."
byname_try_recovery = "Intenta detectar particiones mmc desde recovery.img"
byname_detect_manual = "Por favor introduce el nombre del directorio y pulsa ENTER"
byname_no_byname = "el nombre del directorio está vacío."
byname_create_mmc = "Creando mmc desde recovery.img ..."
byname_need_recovery = "Necesitas un recovery.img para este proceso."
byname_no_mmc = "La cocina no puede encontrar los bloques mmc."
byname_recovery_fail = "mmc no se pudo detectar desde Recovery.img."
byname_try_boot = "Intenta detectar las particiones desde el boot.img"

# Signature
sig_info = "El nombre que des, se mostrará cuando flashees"
sig_info2 = "el zip y será el nombre de este cuando"
sig_info3 = "el zip esté terminado."
sig_info_q = "¿Cuál será el nombre de tu zip?"
sig_info_error = "No uso / en el nombre del zip"
donate_sig_cust = "Este se mostrará debajo del nombre del zip cuando se esté flasheando,"
donate_sig_cust2 = "la versión estándar mostrará Built with SuperR´s Kitchen."
donate_sig_q = "¿Cuál es tu firma?"

# Zip devices
zipdev_info = "Esta opción comprimirá todos los archivos nuevos del dispositivo para compartir."
zipdev_building = "Creando zip del dispositivo ..."
zipdev_uploading = "Subiendo al servidor ..."
zipdev_finished = "El zip del dispositivo se ha creado:"
zipdev_upload = "¿Desea subirlo ahora para que los nuevos archivos puedan ser"
zipdev_upload2 = "agregados a la base de datos para que otros lo usen? y / n"
support_upload = "¿Deseas cargar tu archivo zip de soporte ahora? y / n"
xdauser_q = "¿Cuál es tu nombre de usuario de XDA (usa 'invitado' si no tienes uno) ?"
zipdev_no_new = "No hay nuevos dispositivos en el directorio de dispositivos."

# Kitchen updater
update_check_kitchen = "Comprobando actualizaciones ..."
update_down = "El servidor debe estar inactivo temporalmente."
update_down2 = "Por favor, inténtalo de nuevo más tarde."
update_update_avail = "¡Hay disponible una actualización!"
update_update_cv = "VERSIÓN ACTUAL: "
update_update_nv = "NUEVA VERSIÓN: "
update_update_now = "Actualizar ahora"
update_update_view = "Ver registro de cambios"
update_changelog = "Registro de cambios (últimas 3 versiones):"
update_updating = "Actualizando ..."
update_finished = "La cocina SuperR´s se ha actualizado y debe reiniciarse."
update_already = "La cocina SuperR´s ya está actualizada"
update_check_launcher = "Buscando actualizaciones del lanzador de la Kitchen..."
update_launcher_avail = "Actualización  disponible"
update_launcher_cv = "VERSIÓN ACTUAL: "
update_launcher_nv = "NUEVA VERSIÓN: "
update_launcher_finished = "Instalador / Lanzador ha sido actualizado"
update_problem_download = "Hubo un problema al descargar la actualización."
update_no_internet = "La Cocina no pudo detectar una conexión a Internet."
update_fail = "Hubo un problema de actualización. Prueba con una"
update_fail2 = "instalación nueva."
update_fail3 = "Perdona las molestias."
update_q = "¿Quieres actualizar ahora? y / n"
update_auto_q = "¿Quieres buscar actualizaciones en el arranque de la cocina? y / n"
update_auto_toggle = "Buscar actualizaciones al inicio"
update_cred_fail = "Sus credenciales no se encontraron en la base de datos."
update_cred_fail2 = "Puede actualizar o descargar la última versión después"
update_cred_fail3 = "de estar registrado y ser aprobada tu suscripción"
update_reg_address = "https://sr-code.com/reg.php"
update_verify = "Verificación de las sumas de comprobación de archivos ..."
update_local = "¿Desea instalar el update.zip?  y/n"
update_latest_version = "no es la versión más reciente. La última versión es"

# New Project
new_q = "Establece el nombre del nuevo proyecto (los espacios se reemplazarán por _):"
new_already = "Ya tienes un proyecto con ese nombre"

# Plugin
donate_plugin_cho = "Elije el plugin para ejecutar:"
donate_plugin_install_cho = "Elije el plugin para instalar:"
donate_plugin_delete_cho = "Elije el plugin para eliminar:"
donate_plugin_error = "Los scripts de plugins de complementos deben estar en un directorio con el mismo nombre"
donate_plugin_error2 = "como el script del plugins."
donate_plugin_server = "Parece que el servidor de plugins no funciona. Por favor, inténtalo de nuevo más tarde"
donate_plugin_none = "No hay nuevos plugins para instalar"
donate_plugin_reinstall_q = "No se puede comprobar si hay actualizaciones porque se instaló antes"
donate_plugin_reinstall_q2 = "el sistema de actualización."
donate_plugin_reinstall_q3 = "¿Quieres reinstalar ahora? y / n"
donate_plugin_crash = "Hubo un fallo en el plugin:"
donate_plugin_crash2 = "Comprueba el archivo plugin.log para más detalles."
donate_plugin_incompat = "El plugin no es compatible con el sistema."

# Sign
sign_ram_check = "Comprobando ram ..."
sign_no_ram = "Puede que no tengas suficiente memoria ram para firmar este zip."
sign_signing = "Firmando "
sign_signed = "Ha sido creado. ¡A Disfrutar!"
sign_fail = "Algo salió mal con la firma."
sign_q = "¿Quieres firmar el zip? y / n"

# Build img
img_add = "Añadiendo"
img_flash_fail = "El flashable no funcionará porque"
img_flash_fail2 = "no hay información de la partición para "
img_create_dat = "Crear una imagen sparse dat para "
img_create_symlinks = "Crear enlaces symlinks para "
img_create_raw = "Creando"
img_fail = "Algo salió mal construyendo la imagen."
img_fail_size = "Imposible determinar el tamaño de la partición."
img_fail_fit = "el empaquetado falló. El directorio no coincide:"
img_fail_log = "el empaquetado falló. Comprueba el log img_build.log para mas detalles."
img_dir_open = "Asegúrate de que el directorio del sistema no está abierto en"
img_dir_open2 = "su administrador de archivos o en cualquier otro lugar y vuelve a intentarlo."
img_flash_failB = "El flashable no funcionará porque no hay"
img_flash_failB2 = "información de la partición. Crea un directorio de tu dispositivo o introduce la"
img_flash_failB3 = "información manualmente después de crear el zip"
img_sparse_q = "¿Qué tipo de system.img debemos crear?"

# Language
reset_language = "El idioma se ha restablecido, y la cocina necesita reiniciarse"
lang_added = "Se han agregado nuevos elementos de idioma inglés a "
lang_translate = "Asegúrate de traducirlos."

# Tools
tools_dl = "Descargando "
tools_dl_failed = "La descarga de las herramientas falló:"
tools_dl_install_failed = "La descarga / instalación de las herramientas falló."
tools_dl_device_failed = "No se puede descargar la base de datos del dispositivo en este momento."
tools_dl_device_failed2 = "Puedes usar Herramientas > Actualizar la base de datos del dispositivo más tarde"
tools_dl_device_failed3 = "para obtener la última versión"
wintools_dl = "(aproximadamente 17 MB de descarga)"
lintools_dl = "(aproximadamente 24 MB de descarga)"
tools_need = "Necesitas herramientas para continuar."
tools_dl_install = "Descargando / Instalando ahora ..."
tools_dl_q = "¿Quieres descargarlos / instalarlos ahora? y / n"

#Example Plugin
plug_example_text = " Añade más plugins a "
