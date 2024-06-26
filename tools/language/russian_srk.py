# -*- coding: utf-8 -*-

# Main Menu
title_main = "Главное меню"
title_choose = "Выберите проект:"
title_delete = "Удалить проекты:"
title_extract = "Настройка распаковки:"
menu_create = "Создать новый проект"
menu_choose = "Выбрать другой проект"
menu_delete = "Удалить проект"
menu_extract = "Извлечь прошивку"
menu_updates = "Проверка обновлений"
menu_misc = "Разное"
menu_boot_recovery = "Boot/Recovery утилиты"
menu_rom_tools = "Меню редактирования прошивки"
menu_new = "Новый проект"
menu_quit = "Выйти"
menu_back = "Назад"
menu_skip = "Пропустить"

# ROM Tools Menu
menu_deodex = "Деодексировать "
menu_perm_type = "Выбрать тип сборки "
menu_root = "Root права"
menu_asserts = "Проверка имени аппарата"
menu_extra_dir = "Дополнительные каталоги"
menu_rom_debloat = "Очистка мусора"
menu_build_menu = "Сборка"

# Startup
startup_project = "Текущий Проект: "
startup_version = "Версия Android: "
startup_mdepend = "Проверка  зависимостей: "
startup_need_java = "Требуется Java 8 для использования программы."
startup_copy_extract = "Скопируйте прошивку в папку проекта"
startup_copy_extract2 = " и выберите опцию 4 для извлечения."
startup_title_no_rom = "Нет прошивки!"
startup_no_projects = "Нет проекта для редактирования."
startup_prep_updater_script = "Подготовка скрипта установки ..."
startup_no_rom = "Здесь нет прошивки для обработки."
startup_srkuser = "Введите свой логин  (Не почту):"
startup_srkuser_pass = "Пароль: "
startup_srkuser_error = "Не вводите свою почту , только логин."
startup_srkuser_error2 = " не найдено в базе пользователей или"
startup_srkuser_error3 = "неправильный пароль. Проверьте ещё раз"
startup_srkuser_error4 = "Логин/пароль введёте когда вы"
startup_srkuser_error5 = "зарегистрируете программу."
startup_srkuser_noauth = "Этот компьютер не авторизован!."
startup_srkuser_unknown = "Неизвестная ошибка. Свяжитесь с разработчиком SuperR."
startup_srkuser_q = "Это точно ваш логин?  y/n"
startup_srkpass_q = "Хотите сохранить пароль?  y/n"
startup_error = "Ошибки в установке программы. Попробуйте чистую установку."
startup_checksum = "Следующие контрольные суммы не совпадают:"
startup_environ_error = "Запуск невозможен в данной среде"
startup_vdisk_error = "Запуск невозможен в виртуальной среде Live USB"
startup_remdisk_error = "Запуск невозможен с съемного носителя в Live режиме"
startup_wsl_warning = "Запущено в среде WSL1."
startup_wsl_warning2 = "WSL2 рекомендуется для полной совместимости SuperrKitchen."
startup_wsl2_warning = "Не запущено из /home директории."
startup_wsl2_warning2 = "Возможна ошибка Windows при выдаче прав и медленная работа."
startup_win_warning = "Поддержка нативной Windows прекращена."
startup_win_warning2 = "WSL2 лучший метод для запуска Linux kitchen в Windows."

# Build
menu_build_zip = "Сборка полного Zip"
menu_sys_img = "Собрать EXT4 образ"
menu_sign = "Подпись готового zip"
donate_menu_zipalign = "Выровнять apk"
donate_menu_custom_id = "Редактировать ro.build.display.id"
menu_custom_zip = "Пользовательское zip меню"
build_selinux_error = "Либо ваше ядро не поддерживает selinux, или"
build_selinux_error2 = "kitchen не может найти то, что ей нужно. Если вы уверены что ваше"
build_selinux_error3 = "устройство поддерживает selinux, вы можете скопировать file_contexts"
build_selinux_error4 = "файл из ramdisk в директорию проекта 00_project_files"
build_selinux_error5 = "для использования этой функции."
build_selinux_error6 = "Сейчас вам нужно использовать set_perm или raw_img."
build_patient = "Это может занять немного времени. Пожалуйста ждите ..."
build_prep_img = "Подготовка файлов для создания образа ..."
build_check_ziplog = "Что-то пошло не так. Проверьте zip.log на ошибки."
build_prep_sys_img = "Подготовка файлов для создания EXT4 образа ..."
build_img_error = "Произошла ошибка при создании образа."
build_img_which = "Какой EXT4 img вы хотели бы собрать?"
build_img_nocon = "Невозможно найти file_contexts file. Убедитесь"
build_img_nocon2 = "что boot.img находится в директории проекта, или скопируйте"
build_img_nocon3 = "file_contexts в директорию проекта 00_project_files "
build_img_nocon4 = "и попробуйте снова."
build_no_zip = "Отсутствует zip для подписи."
build_no_boot_q = "Ваша прошивка не содержит boot.img или kernel.img/ramdisk.img."
build_no_boot_q2 = "Всё равно хотите продолжить?  y/n"
build_cho_zip = "Выбрать zip для подписи:"
build_man_img_size = "Хотите использовать текущий размер?  y/n"
zipalign_q = "Хотите провести выравнивание перед сборкой zip?  y/n  "
zipalign = "Выравнивание"
zipalign_frame_q = "Хотите выровнять apk файлы в /framework?  y/n  "
zipalign_complete = "Выравнивание завершено"
donate_bdisplay = "Чтобы вы хотели увидеть в строке сборки?"

# Custom zip
title_cho_cust_zip = "Выберите опции zip для сборки:"
cust_deldir_q = "Выхотите чтобы zip удалял исходные"
cust_deldir_q2 = "директории перед прошивкой?  y/n"
cust_meta_prep = "Подготовка META-INF секции ..."
cust_not_exist = "Одна или несколько директорий для сборки не найдены."
cust_dir_info = "Убедитесь, что у вас есть хотя бы одно из указанного в "
cust_file_check = "Убедитесь в наличии system, META-INF, и boot.img в "
cust_prep = "Подготовка файлов ..."
cust_convert_binary_q = "Хотите сконвертировать  updater-script"
cust_convert_binary_q2 = "в update-binary?  y/n  "
cust_convert_binary = "Конвертирование updater-script в update-binary ..."

# Debloat
menu_debloat = "Очистка прошивки"
menu_debloat_cust = "Пользовательская очистка"
menu_debloat_knox = "Удалить Samsung Knox"
menu_debloat_restore = "Восстановить мусор/Knox"
menu_debloat_refresh = "Обновить статус очистки"
bloat_already_debloated = "Эта прошивка уже очищена"
bloat_rem = "Удаление мусора ..."
bloat_moved = "Мусор перемещён в:"
bloat_cust_info = "Добавьте содержимое в один из следующих файлов, чтобы использовать эту функцию"
bloat_knox_not_exist = "Knox не доступен для данной прошивки"
bloat_knox_rem = "Удаление Knox ..."
bloat_knox_moved = "Knox перемещён в:"
bloat_no_files_restore = "Нет файлов для восстановления"
bloat_restore = "Восстановление мусора ..."
bloat_has_restored = "Мусор восстановлен."
bloat_q = "Хотите очистить вашу прошивку?  y/n  "
bloat_knoz_rem_q = "Хотите удалить Knox?  y/n  "
bloat_restore_q = "Хотите восстановить мусор?  y/n  "
debloated = "Очищено"
bloated = "Замусорено"
bloat_dir_emply = "Пользовательский скрипт очистки пуст"

# Root
title_cho_root_zip = "Выбор Root:"
menu_root_method = "Какой метод Root вы хотите применить?"
menu_ss_method = "Какой тип SuperSU вы хотите установить?"
menu_supersucho = "Разрешить SuperSU автовыбор"
menu_system_install = "Установка в систему (Systemless = false)"
menu_inject = "Внедрить sepolicy патч и установить в систему"
menu_download_inject = "Загрузить/Установить inject-sepolicy-addon"
menu_root_unroot = "Root/Unroot прошивки"
menu_busybox = "Busybox Добавить/Удалить"
menu_add_remove_sud = "Добавить/Удалить su.d поддержку"
root_already = "Уже есть root."
root_must_add = "Сначала добавьте root."
busybox_already = "Уже есть Busybox."
busybox_q = "Хотите добавить Busybox в прошивку?  y/n  "
root_sud_add_q = "Хотите добавить su.d в прошивку?  y/n  "
root_sud_rem_q = "Хотите удалить поддержку su.d?  y/n  "
root_supersu_q = "SuperSU уже мёртвый проект. Уверены что хотите добавить именно его?  y/n"
root_remove = "Удаление root ..."

# General
general_remove_q = "Удалить?  y/n  "
general_continue_q = "Хотите продолжить?  y/n  "
general_cont_anyway_q = "Всё равно хотите продолжить?  y/n  "
general_extracting = "Извлечение "
general_create = "собран в "
general_build = "собирается в "
no_python = "Вы должны установить Python3.5 или выше, чтобы использовать эту функцию."
more_info_link = "Посетите следующую ссылку для получения дополнительной информации:"
spaces_not_allowed = "Пробелы не допускаются"

# Status
enabled = "Включено"
disabled = "Выключено"
add_support = "Добавить поддержку"
yes = "Да"
no = "Нет"
secure = "Защищено"
insecure = "Защита снята"
no_knox = "Нет Knox"
knox = "Knox активен"
no_root = "Нет Root"

# Boot/Recovery Tools
title_boot = "Boot/Recovery Инструменты"
title_cho_boot = "Выберите boot или recovery img"
title_unpack = "Распакуйте для других опций"
title_current = "Текущее: "
menu_pack_boot = "Запаковать "
menu_insecure = "Нет защиты/Защита  "
menu_dmverity = "Удалить dm-verity"
menu_forcee = "Добавить/Удалить forceencrypt"
menu_deopatch = "Патч sepolicy для деодексации Oreo"
menu_deopatch_fail = "Ошибка патча, или sepolicy уже пропатчен"
menu_deopatch_sepol = "sepolicy не найден"
menu_deopatch_add = "sepolicy был пропатчен для деодексации Oreo"
menu_unpack = "Распаковка "
menu_boot_flashable = "Собрать для прошивки "
menu_boot_restore = "Восстановить оригинал: "
menu_switch_boot = "Переключить boot/recovery"
boot_repack = "Перепаковка "
boot_repack_problem = "Возникла проблема при перепаковке"
boot_packed_d = " запакован"
boot_no_img = "Отсутствует boot.img или recovery.img в "
boot_prop_warn = "Скопируйте build.prop в директорию проекта и попробуйте снова."
boot_prep_build = "Подготовка к сборке ..."
boot_unpack = "Распаковка "
boot_unpack_problem = "Возникла проблема при распаковке "
boot_unpack_noram = "Отсутствует ramdisk в этом boot.img."
boot_need_img = "Вам нужен img для этого процесса."
boot_permission_error = "Ошибка прав доступа. Проверьте boot.log"
boot_permission_error2 = "Возможные решения:"

# Misc Tools Menu
title_misc = "Разное"
menu_plugin_menu = "Менеджер плагинов"
menu_plugin_run = "Запуск плагина"
menu_plugin_install = "Установка плагина"
menu_plugin_delete = "Удаление плагина"
menu_plugin_updates = "Проверить обновления плагинов"
menu_plugin_updates_info = "Доступное обновление:"
menu_plugin_get = "Получение списка плагинов ..."
menu_plugin_bashwin = "Вы не можете запускать Bash плагины в Windows. Используйте"
menu_plugin_bashwin2 = "менеджер плагинов для удаления и переустановки новых версий."
menu_zip_devices = "Запаковать устройства/файлы для отправки"
menu_language = "Сброс языка"
menu_heapsize = "Файл подкачки"
menu_extract_options = "Опции извлечения"
menu_support = "Поддержка: Создать zip для отправки"
menu_ubinary = "Опции для сборки zip "
menu_tools_reset = "Сбросить все настройки"
menu_flashable = "Опции zip для прошивки (глобальные)"
menu_tools_reset_go = "Сброс настроек ..."
menu_device_reset = "Обновить базу девайсов"
menu_choose_server = "Основной сервер"
menu_tools_update = "Обновление будет завершено после перезапуска"
support_create = "Создание support.zip ..."
menu_ext4exe = "Использование ext4fs"
menu_zip_compression = "Уровень сжатия zip для прошивки"
menu_zip_compression2 = "Введите нужный уровень сжатия zip прошивки"

support_finish = " zip для поддержки создан в директории проекта"
support_finish_up = "zip был загружен на поддержку"
heapsize_q = "Пожалуйста введите размер файла подкачки в MB. Он должен быть"
heapsize_q2 = "меньше размера физической памяти:"
heapsize_choose = "Что вы хотите сделать?"
heapsize_custom = "Сменить размер подкачки для java"
heapsize_reset = "Вернуть размер подкачки по умолчанию"
heapsize_num_error = "Введите размер в MB (Пр. 1024)"
heapsize_error = "Размер файла подкачки должен быть меньше или равен"
heapsize_error2 = "физическому размеру памяти."
physical_ram = "Физическая память: "
heapsize_auto = "По умолчанию"
title_ubinary = "Опции для сборки zip  "
ask_b = "Спрашивать всегда о конвертации update-binary script"
ask_s = "Спрашивать всегда"
always_b = "Всегда конвертировать в update-binary script"
always_s = "Всегда конвертировать"
never_b = "Никогда не конвертировать в update-binary script"
never_s = "Никогда не конвертировать"
metasize = "Короткий/Длинный set_metadata updater-script (глобально)"
metasize_s = "Короткий"
metasize_l = "Длинный"
metasize_q = "Какой длины set_metadata updater-script вы хотите использовать?"

# Asserts
menu_add_assert = "Добавить/Удалить ограничения"
menu_asserts_custom = "Добавить особое ограничение"
menu_asserts_remove = "Удалить все ограничения для установки"
menu_asserts_reset = "Сбросить ограничения по умолчанию"
asserts_no_assert = "Нет ограничений для установки."
asserts_current = "Текущие ограничения установки: "
asserts_enter = "Ограничения устройств разрешают/запрещают прошивку. Если вы"
asserts_enter2 = "разрешите прошивку в неверный девайс это может"
asserts_enter3 = "иметь серьёзные последствия. Вы будете предупреждены :)"
asserts_enter4 = "Пожалуйста введите разделяя запятыми разрешённые девайсы."
asserts_enter5 = "Убедитесь что текущее устройство находится "
asserts_enter6 = "в списке. Нажмите ENTER для завершения."
asserts_prep = "Подготовка разрешений ..."
asserts_type = "Введите особое ограничение. Нажмите ENTER для завершения."
asserts_cust_error = "Синтаксис должен быть "
asserts_prep_cust = "Подготовка особых разрешений ..."

# Extra Directory
menu_data = "/data/app"
menu_cust_dir = "Пользователь"
menu_cctr = "Не активно"
extra_data_added = "/data/app поддержка добавлена. Положите приложения в:"
extra_already_data = "Уже есть поддержка /data/app."
extra_already_data2 = "/data директория в проекте сохранена."
extra_already_data3 = "Хотите удалить?  y/n"
extra_data_rem = "/data/app поддержка удалена"
extra_cust_name = "Введите название пользовательского каталога и нажмите ENTER."
extra_cust_loc = "Где должен быть прошит пользовательский каталог?"
extra_cust_name_q = " будет добавлено в прошивку. Надо перенести в раздел?  y/n"
extra_cust_setup = "Настройка "
extra_cust_add = "поддержка добавлена"
extra_data = "Тип разрешений:"
extra_data_q = "Хотите добавить /data/app поддержку?  y/n  "
extra_data_perm = "Выберите тип разрешений /data : "
extra_cust_already = " уже добавлено."

# Selection
select = "Сделайте ваш выбор:  "
select_enter = "Сделайте ваш выбор и нажмите ENTER:  "

# Notices
example = "Например:"
warning = "Предупреждение:"
notice = "Уведомление:"
missing = "Недостающие файлы:"
current = "Текущее"
error = "Ошибка:"
success = "Успешно:"
error_mess = "Что-то пошло не так."

# Press ENTER
enter_rom_tools = "Нажмите ENTER для возврата в меню - Редактирование прошивки"
enter_continue = "Нажмите ENTER для продолжения"
enter_main_menu = "Нажмите ENTER для возврата в Главное Меню"
enter_boot_menu = "Нажмите ENTER для возврата в меню  - Boot/Recovery Инструменты"
enter_build_menu = "Нажмите ENTER для возврата в меню - Сборка прошивки"
enter_change_perm_menu = "Нажмите ENTER для возврата в меню - Методы сборки"
enter_debloat_menu = "Нажмите ENTER для возврата в меню - Очистка прошивки"
enter_extra_dir_menu = "Нажмите ENTER для возврата в меню - Экстра директории"
enter_cho_another_detection = "Нажмите ENTER для выбора другого метода обнаружения"
enter_ready = "Нажмите ENTER когда будете готовы"
enter_kitchen_updater = "Нажмите ENTER для возврата в  - Kitchen обновления"
enter_misc_tools_menu = "Нажмите ENTER для возврата в меню - Разное"
enter_heapsize_menu = "Нажмите ENTER для возврата в меню файла подкачки"
enter_continue_extracting = "Нажмите ENTER для продолжения распаковки"
enter_try_again = "Нажмите ENTER чтобы попробовать снова"
enter_root_menu = "Нажмите ENTER для возврата в меню - Выбор Root"
enter_exit = "Нажмите ENTER для выхода"

# Perm Type
perm_title = "Поменять/Выбрать метод сборки прошивки"
perm_set_metadata_cur = "set_metadata"
perm_set_metadata = "set_metadata (KitKat и выше)"
perm_set_perm = "set_perm (JellyBean и ниже)"
perm_sparse = "Sparse dat"
perm_sparse_red = "Sparse dat (не поддерживается этим устройством)"
perm_raw_img = "raw_img"
perm_check_symlinks = "Проверка симлинков ..."
perm_set_metadata_error = "Эта прошивка НЕ KitKat или выше"
perm_set_perm_error = "Эта прошивка НЕ JellyBean или ниже"
perm_changing_perm = "Смена метода сборки ..."
perm_which = "Какой метод сборки вы хотите использовать?"

# Delete Project
delete_has_been = " был удалён."
delete_q = "будет удалён. Продолжить?  y/n"

# Deodex
deodex_copy_frame_prop = "Скопируйте framework директорию и build.prop"
deodex_copy_frame_prop2 = "из вашей прошивки в "
deodex_no_odex = "Отсутствуют odex файлы в прошивке."
deodex_no_boot_oat = "Отсутствует boot.oat в прошивке. Деодексация невозможна."
deodex_no_plat = "Деодексация данного API не поддерживается на этой платформе"
deodex_no_valgrind = "Пожалуйста установите valgrind, и попробуйте снова"
deodex_disclaimer = "Деодексированная прошивка может не работать. Возможно возникновение"
deodex_disclaimer2 = "ошибок, не загружается, или всё вместе. Я в курсе этих"
deodex_disclaimer3 = "проблем. Если вы знаете как их исправить,"
deodex_disclaimer4 = "пожалуйста не надо писать об этом. Спасибо :)"
deodex_use_method = "Какой метод деодексации хотите применить?"
deodex_oat2dex_ver = "Какую версию oat2dex хотите использовать?"
deodex_oat2dex_official = "Официальную v0.86"
deodex_oat2dex_latest = "Последний релиз"
title_cho_oat2dex = "Выберите oat2dex:"
title_cho_smali = "Выберите smali:"
title_cho_baksmali = "Выберите baksmali:"
deodex_no_api = "Версия Android не найдена."
deodex_config_arch = "Укажите архитектуру вашего устройства."
deodex_config_arch2 = "Совет:"
deodex_config_arch3 = "Проверьте директорию framework , вы сможете увидеть"
deodex_config_arch4 = "внутри другие директории. Они могу называться"
deodex_config_arch5 = "так (пр. arm, arm64, x86)."
deodex_config_arch6 = "Если вы не видите таких директорий, проверьте следущее:"
deodex_config_arch7 = "1. Убедитесь что правильно указали архитектуру вашего устройства."
deodex_config_arch8 = "2. Убедитесь что прошивка уже не деодексирована."
deodex_config_arch9 = "Введите архитектуру вашего устройства и нажмите ENTER."
deodex_extract_txt = "Извлечение odex файлов ..."
deodex_extract = "... Извлечение "
deodex_move = "Перемещение extra apps ..."
deodex_deop = "Распаковка boot.oat ..."
deodex_start_app = "Начало деодексации /system/app ..."
deodex_start_priv = "Начало деодексации /system/priv-app ..."
deodex_start_frame = "Начало деодексации /system/framework ..."
deodex_deodexing = "... Деодексация "
deodex_app_already = " уже деодексировано ..."
deodex_clean = "Очистка ..."
deodex_complete = "Деодексация завершена"
deodex_remain = "Следующие odex файлы остались в прошивке"
deodex_method = "Метод:"
deodex_problems = "Были проблемы при деодексации следующих файлов"
deodex_problems2 = "и это может вызвать проблемы при прошивке."
deodex_problems3 = "Вы были предупреждены:"
deodex_try_smali = "SUGGESTION: Try smali/baksmali"
deodex_api = "API LEVEL: "
deodex_arch = "ARCH: "
deodex_arch2 = "ARCH2: "
deodex_move_odex = "Перемещение odex файлов ..."
deodex_try_anyway = "Всё равно хотите попробовать?  y/n  "
deodex_continue_q = "Хотите продолжить деодексацию?  y/n  "
deodex_del_meta_inf_q = "Android Nougat использует APK Signature Scheme v2, и"
deodex_del_meta_inf_q2 = "это может вызвать проблемы при деодексации. Удаление"
deodex_del_meta_inf_q3 = "META-INF из apk файлов может решить эту проблему."
deodex_del_meta_inf_q4 = "Хотите удалить META-INF директории из"
deodex_del_meta_inf_q5 = "всех apk файлов в прошивке?  y/n  "
deodex_del_meta_inf = "Удаление META-INF из приложений ..."
deodex_del_arch = "Хотите удалить framework директории перечисленные ниже?  y/n"
deodex_pack_jar = "Запаковка dex в jar файлы ..."
deodex_server_disabled = "cdex конвертация на сервере в данный момент отключена"
deodex_server_cdex = "Конвертирование cdex на сервере ..."
deodex_server_error1 = "Ошибка загрузки"
deodex_server_error2 = "Ошибка перемещения файлов в рабочую директорию"
deodex_server_error3 = "ошибка извлечения cdex zip "
deodex_server_error4 = "dex zip ошибка сборки на сервере"

# Extract
extract_title = "Распаковка"
extract_no_files_message = "1) Добавьте прошивку в  zip, tar/boot.img, system.img/boot.img, или"
extract_no_files_message2 = "   win/boot.win и выберите эту опцию."
extract_no_files_message3 = "2) Получить system, vendor, boot, и recovery образы из вашего"
extract_no_files_message4 = "   рутованного устройства или из кастомного recovery для извлечения."
extract_cho_option = "Выберите опцию для извлечения прошивки"
extract_cho_option2 = "**Если вы получаете ошибки, попробуйте другие методы**"
extract_cho_option3 = "1) Моё устройство загружено в кастомное recovery (прошивка не работает)"
extract_cho_option4 = "2) Моё устройство загружено в Android (должен быть root)"
extract_plug = "** Подключите ваше устройство"
extract_detect_part = "Обнаружение разметки разделов ..."
extract_detect_part2 = "Если на это всё остановилось, попробуйте поменять USB режим на"
extract_detect_part3 = "вашем устройстве с зарядки на передачу файлов (MTP)"
extract_pull_error = "Что-то пошло не так. Скорей всего у вас нет разрешений для"
extract_pull_error2 = "копирования разделов с вашего устройства."
extract_pulling = "Копирование "
extract_prep = "Подготовка к распаковке ..."
extract_zip_fail = "Этот архив не содержит прошивки которая может"
extract_zip_fail2 = "быть распакована."
extract_zip = "Извлечение zip ..."
extract_dat = "Извлечение system.new.dat, system.transfer.list, и boot.img ..."
extract_convert_br = "Распаковка dat.br ..."
extract_convert_sys = "Конвертация в "
extract_img_from_zip = "Извлечение образов из zip ..."
extract_tar_boot = "Извлечение system.ext4.tar.a и boot.img ..."
extract_img = "Извлечение образов..."
extract_fail = "Что-то пошло не так при распаковке."
extract_tar_md5 = "Извлечение tar.md5 файлов ..."
extract_chunk = "Извлечение sparsechunks и boot.img ..."
extract_pbin = "Извлечение payload.bin ..."
extract_multi = "Извлечение multi-part system ..."
extract_convert_chunk = "Конвертирование sparse chunks в файлы образов ..."
extract_fix_img = "исправление "
extract_general = "Извлечение в "
extract_check_firm = "Проверка пакета прошивки ..."
extract_tgz_fail = "Этот tgz архив не может быть"
extract_tgz_fail2 = "официальной прошивкой Nexus ."
extract_files = "Извлечение файлов ..."
extract_md5_fail = "Отсутствует system.img.ext4 в вашем файле tar.md5"
extract_tar_fail = "Looks like the tar file you have is not from a nandroid backup"
extract_tar = "Extracting name"
extract_extra_extract_q = "Хотите извлечь особые разделы (modem.bin, и тд.)?  y/n  "
extract_cache_extract_q = "Хотите извлечь cache.img?  y/n  "
extract_cache_include_q = "Хотите включить файлы извлеченные из cache.img"
extract_cache_include_q2 = "в вашу прошивку?  y/n  "
extract_cache = "Внедрение cache.img файлов ..."
extract_cache_fail = "Отсутствует csc.zip в вашем cache.img"
extract_rom_fail = "Возникла проблема с извлечением прошивки."
extract_cho_part_detect = "Выберите метод обнаружения разметки разделов "
extract_adb_shell = "Из устройства используя adb shell"
extract_project_dir = "Директория проекта (BETA): "
extract_manual = "Ввести вручную"
extract_detect = "Определение размера раздела для "
extract_beta = "Эта опция в версии BETA. Возможны ошибки при прошивке."
extract_beta2 = "Вы можете получить сообщение об ошибке, подобное следующему:"
extract_beta3 = "blkdiscard failed: Неверный аргумент"
extract_beta4 = "Вы можете сменить метод сборки на set_metadata или set_perm to"
extract_beta5 = "чтобы избежать данной опции"
extract_manual_bytes = "Введите размер раздела в байтах для "
extract_detect_fail = " размер раздела пуст или не числовой. Попробуйте снова."
extract_sparse_convert = "Конвертирование sparse img ..."
extract_img_fail = "Здесь нет "
extract_copy_e = "Копирование файлов в "
extract_moved_old_rom = "Следущее было перемещено в:"
extract_q = "Хотите извлечь "
extract_q2 = "в текущий проект?  y/n  "
extract_extra_extract = "Хотите извлечь "
extract_extra_q = "?  y/n  "
extract_extra_include = "Хотите включить файлы из"
extract_extra_include_q = " в вашу прошивку?  y/n  "
extract_autorom_sudo = "Настройте sudo сейчас для непрерывной работы AutoROM "
extract_use_concat = "Используйте concatimg плагин, затем извлекайте system.img"

# by-name
byname_how_to_get_q = "Как вы хотите получить информацию о разделах?"
menu_byname_detect_boot = "Обнаружение разметки из boot/recovery images (рекомендовано)"
menu_byname_detect_device = "Обнаружение разметки из вашего устройства"
menu_byname_detect_manual = "Ввод разметки вручную"
menu_byname_detect_mmc = "Обнаружение разметки из recovery.img"
byname_usb_debug = "** Включите - Отладка USB  - на вашем Android устройстве в Системных настройках"
byname_usb_debug2 = "** Подключите устройство"
byname_usb_debug_root = "Для этой операции требуется root."
byname_usb_debug_root2 = "Вы должны разрешить root доступ на вашем устройстве."
byname_error_device = "Ошибка обнаружения разметки на вашем устройстве."
byname_error_device2 = "Попытка обнаружения разделов в recovery.img"
byname_no_boot = "Скопируйте boot.img, recovery.img, или kernel.elf в"
byname_no_boot2 = "директорию проекта и попробуйте снова."
byname_which_img_q = "Какой из образов хотите использовать?"
byname_detect = "Обнаружение разметки из "
byname_no_files = "Вам нужен boot.img, recovery.img, или kernel.elf для этого метода."
byname_boot_fail = "Разметка разделов не найдена."
byname_try_recovery = "Попытка обнаружения разметки в recovery.img"
byname_detect_manual = "Пожалуйста введите название раздела /system и нажмите ENTER"
byname_no_byname = "Нет названия раздела."
byname_create_mmc = "Чтение разметки из recovery.img ..."
byname_need_recovery = "Вам нужен recovery.img для этого метода."
byname_no_mmc = "Разметка разделов не найдена."
byname_recovery_fail = "Разметка не найдена в recovery.img."
byname_try_boot = "Попытка обнаружения разметки в boot.img"

# Signature
sig_info = "Что будет показано в заголовке прошивки"
sig_info2 = " и будет добавлено в название zip когда"
sig_info3 = "прошивка будет собрана."
sig_info_q = "Какое название вашей прошивки?"
sig_info_error = "Не использовать/ в названии прошивки"
donate_sig_cust = "Это будет отображаться после названия в процессе прошивки"
donate_sig_cust2 = "стандартная версия Built with SuperR's Kitchen."
donate_sig_q = "Что хотите написать вы?"

# Zip devices
zipdev_info = "Эта опция будет архивировать все новые устройства, чтобы поделиться."
zipdev_building = "Сборка архива устройств ..."
zipdev_uploading = "Загрузка на сервер ..."
zipdev_finished = "zip устройства создан:"
zipdev_upload = "Хотите загрузить сейчас, чтобы новые файлы могли быть"
zipdev_upload2 = "добавлены в базу для совместного использования?  y/n"
support_upload = "Хотите загрузить прошивку на поддержку сейчас?  y/n"
xdauser_q = "Какой ваш XDA ник (используйте 'guest' если у вас его нет) ?"
zipdev_no_new = "В каталоге устройств нет новых устройств."

# Kitchen updater
update_check_kitchen = "Проверка обновлений ..."
update_down = "Возможно сервер обновлений временно недоступен."
update_down2 = "Пожалуйста попробуйте позже."
update_update_avail = "Доступно обновление!"
update_update_cv = "Текущая Версия: "
update_update_nv = "Новая Версия: "
update_update_now = "Обновить"
update_update_view = "Посмотреть изменения"
update_changelog = "Изменения (последние 3 версии):"
update_updating = "Обновление ..."
update_finished = "SuperR's Kitchen была обновлена и требуется перезапуск."
update_finished_win = "superr1.exe в рабочей директории может быть удалён или проигнорирован."
update_finished_win2 = "Будет удалён автоматически при следующем выходе "
update_finished_win3 = "и перезапуске."
update_already = "SuperR's Kitchen уже обновлена"
update_check_launcher = "Проверка Kitchen Launcher'а обновлений ..."
update_launcher_avail = " Доступно обновление Launcher'а"
update_launcher_cv = "Текущая Версия:"
update_launcher_nv = "Новая Версия:"
update_launcher_finished = "Установщик/Launcher обновлен"
update_problem_download = "Проблема при загрузке обновления."
update_no_internet = "Не удаётся соединиться с сервером, проверьте интернет соединение."
update_fail = "Возникла проблема при обновлении. Попробуйте"
update_fail2 = "чистую установку."
update_fail3 = "Извините за неудобства."
update_q = "Хотите обновить сейчас?  y/n  "
update_auto_q = "Вы хотите проверять обновления автоматически при запуске?  y/n  "
update_auto_toggle = "Проверять обновления при запуске"
update_cred_fail = "Ваши учетные данные не найдены в базе. Вы"
update_cred_fail2 = "можете обновить или загрузить последнюю версию после"
update_cred_fail3 = "регистрации и подтверждения."
update_reg_address = "https://sr-code.com/reg.php"
update_verify = "Проверка контрольных сумм ..."

# New Project
new_q = "Введите название нового проекта (Пробелы буду заменены на _): "
new_already = "Уже существует проект с таким названием"

# Plugin
donate_plugin_cho = "Выберите плагин для запуска:"
donate_plugin_install_cho = "Выберите плагин для установки:"
donate_plugin_delete_cho = "Выберите плагин для удаления:"
donate_plugin_error = "Скрипты плагина должны находится в директории с"
donate_plugin_error2 = "таким же названием."
donate_plugin_server = "Сервер плагинов временно недоступен. Попробуйте позже"
donate_plugin_reinstall_q = "Невозможно проверить на обновления установленный ранее "
donate_plugin_reinstall_q2 = "плагин."
donate_plugin_reinstall_q3 = "Хотите переустановить сейчас?  y/n"
donate_plugin_crash = "Сбой в плагине: "
donate_plugin_crash2 = "Проверьте plugin.log для подробностей."

# Sign
sign_ram_check = "Проверка памяти ..."
sign_no_ram = "Вам может не хватить памяти для подписи этого zip."
sign_signing = "Подпись "
sign_signed = "была создана. Поздравляем!"
sign_fail = "ЧТо-то пошло с подписью не так."
sign_q = "Хотите подписать zip?  y/n  "

# Build img
img_add = "Добавление "
img_flash_fail = "Прошивка будет неработоспособна потому что нет"
img_flash_fail2 = "информации о разделе для "
img_create_dat = "Создание sparse dat образа для "
img_create_symlinks = "Создание симлинков для "
img_create_raw = "Создание "
img_fail = "Что-то пошло не так при сборке образа."
img_fail2 = "Убедитесь что размер раздела правильный и"
img_fail3 = "что директория не слишком велика для него."
img_dir_open = "Убедитесь что системный каталог не открыт в"
img_dir_open2 = "проводнике или где нибудь ещё и попробуйте снова."
img_flash_failB = "Прошивка будет неработоспособна потому что нет"
img_flash_failB2 = "информации о разделе. Создайте директорию для девайса или введите "
img_flash_failB3 = "информацию вручную после сборки прошивки"
img_sparse_q = "Какого типа system.img вы хотите создать?"

# Language
reset_language = "Язык был сброшен. Изменения будут применены"
reset_language2 = "при следующем запуске"
lang_added = "Новые English language элементы были добавлены в "
lang_translate = "Убедитесь что вы их перевели."

# Tools
tools_dl = "Загрузка зависимостей "
tools_dl_failed = "Ошибка загрузки зависимостей:"
tools_dl_install_failed = "Ошибка загрузки/установки зависимостей."
tools_dl_device_failed = "В настоящее время база устройств недоступна."
tools_dl_device_failed2 = "Вы можете выбрать - Разное > Обновить базу устройств -  позже"
tools_dl_device_failed3 = "для получения последней версии"
wintools_dl = "(примерно 17MB для скачивания)"
lintools_dl = "(примерно 24MB dдля скачивания)"
tools_need = "Нужны файлы для работы."
tools_dl_install = "Загрузка/Установка ..."
tools_dl_q = "Хотите загрузить/установить их сейчас?  y/n  "

#Example Plugin
plug_example_text = " Добавить ещё плагины в "
brotli_q = "Хотите использовать brotli сжатие? (dat.br)?"
brotli_level = "Введите нужный уровень сжатия brotli "
brotli_menu = "sparse_dat brotli сжатие (dat.br)"
menu_mount_extract = "Использовать монтирование для извлечения img файлов"
menu_case_fix = "Исправление имен файлов без учета регистра "
menu_extract_all_img = "Извлечь и совместить все img файлы"
menu_offline_auth = "Меню Оффлайн Авторизации"
menu_offline_renew = "Обновить Оффлайн Авторизацию"
menu_offline_enable = "Включить/Выключить Оффлайн Авторизацию"
menu_renew_now = "Обновить сейчас"
auth_reset = "Оффлайн авторизация была включена/обновлена.Kitchen требуется перезапустить."
auth_reset2 = "Требуется доступ к сети для первого перезапуска."
auth_max_days = "Максимальное количество дней Оффлайн Авторизации: "
auth_expired = "Оффлайн Аторизация закончилась."
expires = "Заканчивается: "
enter_plug_menu = "Нажмите ENTER для возврата в Менеджер Плагинов"
deodex_no_dex = "Нет dex в vdex. Пропуск."
extract_xz_fail = "Отсутствует system.img в этом xz файле"
extract_rom_fail_ext4 = "Ваш img файл не является ext4."
update_local = "Хотите установить локальный update zip?  y/n"
update_latest_version = "это не последняя версия. Последняя версия это"
update_win_final = "Это последний релиз для нативной Windows."
donate_plugin_none = "Нет новых плагинов для установки"
donate_plugin_incompat = "Плагин несовместим с этой системой."
img_fail_size = "Ошибка размера образа."
img_fail_fit = "Ошибка сборки. Директория не пуста:"
img_fail_log = "Ошибка сборки. Проверьте лог img_build.log на ошибки."
super_exists_cli = "В этом проекте присутствует super.img . Удалите его и попробуйте снова."
super_exists_q = "Удалить raw super.img и собрать новый sparse super.img?  y/n"
no_supersize1 = "Сначала извлеките оригинальный super.img в проект."
no_supersize2 = "Альтернативный метод, можете добавить размер в файл 00_project_files/srk.conf."
no_supersize3 = "Пример:"
no_supersize4 = "Укажите размер raw super.img в байтах."
super_include = "Надо добавить в образ"
super_part_size = "Расчитывается размер раздела ..."
super_no_img1 = "Отсутствуют файлы *img соответсвующие требованиям:"
super_no_img2 = "Все образы *img должны быть собраны в sparse."
super_no_img3 = "Названия файлов *img должны быть либо partition.img, либо partition_new.img."
img_not_included1 = "Следующие файлы не были добавлены потому что"
img_not_included2 = "Невозможно расчитать размер раздела:"
ready_to_build_q = "Готовы собрать super.img с текущими настройками?  y/n"
super_building = "Собираем super.img ..."
super_success = "Super.img Успешно собран!"
super_failed = "Ошибка сборки super.img "
super_not_found = "Super.img не найден в текущем проекте."
files_not_exist = "Отсутствует в текущем проекте"
menu_super_img = "Собрать super.img"
super_sparse_q = "Какого типа super.img хотите создать?"
bloat_list_menu = "Список файлов для удаления"
bloat_list_files = "Следующие файлы будут удалены:"
session_expired = "Сессия Superr kitchen истекла."
session_restart = "Перезапустить сейчас"
