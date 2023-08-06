from typing import Any, Callable
import importlib.util
import sys
from subprocess import CompletedProcess
from typing import Any
from datetime import datetime
import os
import re

pih_exists = importlib.util.find_spec("pih.pih") is not None
if not pih_exists:
    sys.path.append("//pih/facade")
from pih.const import CONST, MarkType, PASSWORD, USER_PROPERTIES, FIELD_COLLECTION, PasswordSettings, CheckableSections, HOSTS, AD, PATHS, FILE
from pih import PIH, A, NotFound, ActionValue, ActionStack, Input, Output, Session, while_not_do
from pih.collection import (Mark, User, FullName, 
                            MarkDivision, UserBase, LoginPasswordPair, 
                            MarkGroup, Result, FieldItemList,
                            WorkstationDescription, ResourceStatus, SiteResourceStatus,
                            CTIndicationsValue, Workstation, RobocopyJobStatus, 
                            ChillerIndicationsValueContainer, PrinterReport, DiskStatistics)
from pih import A

class ConsoleAppsApi:

    LINE: str = "........................................................"

    def __init__(self, pih: PIH = None):
        self.pih = pih or PIH
        self.full_name: FullName = None
        self.tab_number: str = None
        self.telephone_number: str = None
        self.division_id: int = None
        self.user_is_exists: bool = False
        self.login: str = None
        self.password: str = None
        self.internal_email: str = None
        self.external_email: str = None
        self.email_password: str = None
        self.polibase_login: str = None
        self.polibase_password: str = None
        self.user_container: UserBase
        self.description: str = None
        self.use_template_user: bool
        self.need_to_create_mark: bool = None

    def create_qr_code_for_mobile_helper_command(self, command: str | None = None, title: str | None = None, show_result: bool = True) -> str | None:
        command = command or self.input.input("Введите название команды")
        title = title or self.input.input("Введите заголовок")
        result = A.A_QR.for_mobile_helper_command(command, title, os.path.join(PATHS.MOBILE_HELPER.QR_CODE_FOLDER, A.PTH.replace_prohibited_symbols_from_path_with_symbol(A.PTH.add_extension(command, FILE.EXTENSION.PNG))), 56)
        qr_code_image_path: str = A.PTH_QR.mobile_helper_command(command)
        if show_result:
            if result:
                self.output.good(
                    f"Файл qr кода {self.bold(title)} создан.\nПуть к файлу:\n{self.bold(qr_code_image_path)}\n")
            else:
                self.output.error("qr код не был создан")
        return qr_code_image_path

    def create_qr_code_for_card_registry_folder(self, card_registry_folder_name: str | None = None, show_result: bool = True) -> list[str]:
        if A.D_C.empty(card_registry_folder_name):
            card_registry_folder_name = self.input.input(f"Введите название папки (или несколько значений названий папок разделенной запятой или пробелом)")
        card_registry_folder_name_list: list[str] = re.split("\W+", card_registry_folder_name)
        card_registry_folder_name_list = list(map(lambda item: str(item).strip(), card_registry_folder_name_list))
        result_path_list: list[str] = []
        for card_registry_folder_name_item in card_registry_folder_name_list:
            card_registry_folder_name_item = A.D_F.polibase_person_card_registry_folder(card_registry_folder_name_item)
            result: bool = A.A_QR.for_polibase_person_card_registry_folder(card_registry_folder_name_item)
            qr_code_image_path: str = PIH.PATH.QR_CODE.polibase_person_card_registry_folder(card_registry_folder_name_item)
            if show_result and len(card_registry_folder_name_list) == 1:
                if not result:
                    self.output.error("qr код не был создан")
            if result:
                result_path_list.append(qr_code_image_path)
        return result_path_list
    
    def disks_information(self, host: str | None = None) -> None:
        host = host or self.input.input("Введите название хоста (компьютера или сервера)")
        if A.C_R.accessibility_by_ping(host):
            disk_statistics_list: list[DiskStatistics] = list(filter(lambda item: item.size > 0, A.PS.get_disk_statistics_list(host)))
            if A.D_C.empty(disk_statistics_list):
                self.output.error("Хост не имеет дисков")
            else:
                self.output.write_line("Информация о дисках:\n")
                for disk_statistics in disk_statistics_list:
                    self.output.write_line(f" {A.CT_V.BULLET} {self.bold(disk_statistics.name)}: {A.D_F.size(disk_statistics.free_space)} из {A.D_F.size(disk_statistics.size)}")
        else:
            self.output.error("Хост не доступен или не найден")

    def resources_and_indications_check(self, checkable_section_list: list[CheckableSections], ask_for_update_before: bool = False, force_update: bool = False, all: bool = False) -> None:
        if CheckableSections.RESOURCES in checkable_section_list or CheckableSections.WS in checkable_section_list:
            def label_function(resource: ResourceStatus, index: int) -> str:
                result: list[str] = [] 
                accessable: bool = resource.accessable
                status: str = A.D_F.yes_no(accessable, True)
                result.append(" ".join((status, self.bold(self.output.blue_str(
                    resource.name)))))
                if isinstance(resource, SiteResourceStatus):
                    if resource.check_free_space_status:
                        free_space_result_list: str = resource.free_space_status.split(" ")
                        result.append(f"      Cвободное место: {free_space_result_list[0]} ({free_space_result_list[1]})")
                    if resource.check_certificate_status:
                        result.append(f"      Сертификат доступен до: {resource.certificate_status}")
                return A.CT.NEW_LINE.join(result)
            force_update = force_update or (ask_for_update_before and self.input.yes_no(
                "Обновить перед получением"))
            if force_update:
                self.output.write_line(
                    self.italic(f"{self.get_formatted_given_name()}, ожидайте получение результата..."))
            for checkable_section in [CheckableSections.RESOURCES, CheckableSections.WS]:
                if checkable_section in checkable_section_list:
                    self.output.new_line()
                    if all:
                        self.output.write_line(self.bold(A.CT_V.BULLET + (" Основные ресурсы" if checkable_section == CheckableSections.RESOURCES else " Наблюдаемые компьютеры")))
                    with self.output.make_indent(2):
                        self.output.write_result(A.R_R.get_status_list([checkable_section], force_update, all if len(checkable_section_list) == 1 and CheckableSections.WS in checkable_section_list else False), False, label_function=label_function, separated_result_item=True)
        if CheckableSections.INDICATIONS in checkable_section_list:
            #self.output.separated_line()
            #self.output.write_line(f"Показания доступны по адрессу:\n{self.bold('http://indications')}, если заходить с рабочего компьютера\nили\n{self.bold('http://192.168.100.138')}, если заходить с мобильного телефона, подключенного к корпоративной wifi сети")
            self.output.new_line()
            self.output.write_line(self.bold(f"{A.CT_V.BULLET} Показания в помещении КТ"))
            with self.output.make_indent(2):
                self.output.write_result(A.R_I.last_ct_value_containers(True))
            self.output.separated_line()
            self.output.write_line(self.bold(f"{A.CT_V.BULLET} Показания в техническом помещении МРТ"))
            chiller_indications_value_container_result: Result[list[ChillerIndicationsValueContainer]] = A.R_I.last_chiller_value_containers(True)
            chiller_indications_value_container: ChillerIndicationsValueContainer = A.R.get_first_element(chiller_indications_value_container_result)
            path: str = A.PTH_I.CHILLER_DATA_IMAGE_LAST
            modification_timstamp: float = os.path.getmtime(path)
            modification_datetime: datetime | None = datetime.fromtimestamp(modification_timstamp if modification_timstamp > 0 else os.path.getctime(path))
            with self.output.make_indent(2):
                self.output.write_result(chiller_indications_value_container_result, title="Показания чиллера\n" if A.D_C.INDICATIONS.chiller_value_actual(chiller_indications_value_container) else f"{self.bold('Внимание!')}: Показания чиллера неактуальны\n", separated_result_item=False)
                self.output.write_image(f"Изображение дисплея чиллера\nВремя снятия: {A.D_F.datetime(modification_datetime)}", A.D_CO.file_to_base64(A.PTH_I.CHILLER_DATA_IMAGE_LAST_RESULT))
        if CheckableSections.VALENTA in checkable_section_list:
            count: int = len(A.PTH.get_file_list_by_directory_info(A.PTH.WS_816_SCAN.VALUE))
            self.output.new_line()
            self.output.write_line(
                self.bold(f"{A.CT_V.BULLET} Новые исследования в Валенте: " + ("Нет" if count == 0 else f"Да ({count})")))
        if CheckableSections.SERVERS in checkable_section_list:
            self.output.new_line()
            self.output.write_line(self.bold(f"{A.CT_V.BULLET} Доступность серверов"))
            with self.output.make_indent(2):
                A.R.every(A.R_SRVS.all_description(), lambda server: self.output.write_line(" " .join((A.D_F.yes_no(A.C_R.accessibility_by_ping(server.name, count=1), True), self.bold(server.name)))))
        if CheckableSections.PRINTERS in checkable_section_list:
            self.output.new_line()
            self.output.separated_line()
            self.output.write_line(
                self.bold(f"{A.CT_V.BULLET} Отчет по принтерам"))
            printer_report_list: list[PrinterReport] = A.R_PR.report(send_to_log=False).data
            for printer_report in printer_report_list:
                self.output.separated_line()
                with self.output.make_indent(2):
                    self.output.write_line(A.D_F.printer_report(printer_report, self.bold))     
        if not all:
            if CheckableSections.BACKUPS in checkable_section_list:
                robocopy_job_status_list: Result[list[RobocopyJobStatus]] = A.R_B.robocopy_job_status_list()
                sort_by_status: bool = self.input.yes_no("Сортировать по статусу", no_label=f"{self.bold(f'Сортировать по дате выполнения - {A.CT_V.NUMBER_SYMBOLS[0]}')}")
                A.R.sort(robocopy_job_status_list, (lambda item: item.last_status or max(A.CT_RBK.STATUS_CODE.keys())) if sort_by_status else lambda item: datetime.fromtimestamp(0) if A.D_C.empty(item.last_created) else A.D.datetime_from_string(item.last_created), sort_by_status)
                def job_status_item_label_function(job_status: RobocopyJobStatus, index: int) -> str:
                    name: str = job_status.name
                    source: str = job_status.source
                    destination: str = job_status.destination 
                    status: int | None = None
                    date: str | None = None
                    if job_status.active:
                        date = "выполняется"
                    else:
                        if job_status.last_created is not None:
                            date = f"{A.D_F.datetime(job_status.last_created)}"
                        status = job_status.last_status
                    variants: list[str] = ["--" if status is None else self.bold(str(status)), "--" if A.D_C.empty(date) else self.bold(date)]
                    return "".join([f" {A.CT_V.BULLET} ", variants[not sort_by_status], ": ", variants[sort_by_status], "".join([ "\n   ", name, ": ", source, A.CT_V.ARROW, destination])])
                variants: list[str] = [self.bold("Статус"), self.bold("Дата выполнения")]
                self.output.write_result(
                    robocopy_job_status_list, False, label_function=job_status_item_label_function, separated_result_item=False, title="".join([f" {A.CT_V.BULLET} ", variants[not sort_by_status], ": ", variants[sort_by_status], "\n", "   Название Robocopy-задания", f"\n{ConsoleAppsApi.LINE}"]))

    def polibase_restart(self, forced: bool = False) -> None:
        if self.input.yes_no("Перезапустить"):
            check_word: str = A.CT_P.NAME
            test: bool = not (check_word == self.input.input(
                f"Введите контрольное слово: {self.bold(check_word)}"))
            if not test and A.C_R.polibase_accessibility(True) and not forced:
                self.output.error(
                    "Перезапуск Polibase: перезапуск невозможен - сервер доступен")
            else:
                notify: bool = test or self.input.yes_no("Уведомить пользователей", True)
                title: str = f"Перезапуск Polibase{' test' if test else ''}"
                polibase_host: str = HOSTS.POLIBASE_TEST.NAME if test else HOSTS.POLIBASE.NAME
                self.output.write_line(A.L.it(
                    f"{title}: Начат процесс закрытия программы Polibase на компьютерах."))
                A.A_P.client_program_close_for_all(notify, None, test)
                self.output.new_line()
                self.output.write_line(A.L.it(
                    f"{title}: Начат процесс перезагрузки сервера Polibase."))
                A.A_P.restart(test)
                while_not_do(lambda: not A.C_R.accessibility_by_ping(
                    polibase_host), sleep_time=5)
                self.output.new_line()
                self.output.write_line(A.L.it(
                     f"{title}: Начат процесс загрузки сервера Polibase."))
                while_not_do(lambda: A.C_R.accessibility_by_ping(polibase_host), sleep_time=5)
                self.output.new_line()
                A.E.wait_server_start(polibase_host)
                self.output.write_line(A.L.it(f"{title}: Завершен процесс загрузки сервера Polibase."))
                A.ME_P.notify_about_polibase_restarted(test)

    def polibase_client_program_close(self, search_value: str | None = None, for_all: bool = False) -> None:
        if for_all:
            check_word: str = A.CT_P.NAME
            test: bool = not (check_word == (search_value or self.input.input(
            f"Введите контрольное слово - {self.bold(check_word)}")))
            A.A_P.client_program_close_for_all(True, self.input.input("Введите сообщение для пользователей Polibase"), test) 
        else:
            try:
                workstation_list: Result[list[Workstation]] = A.R_WS.by_any(search_value or self.input.input("Введите запрос для поиска компьютера"))
                def every_action(workstation: Workstation) -> None:
                    if A.A_P.client_program_close_for_workstation(workstation):
                        self.output.good(f"Программа Polibase закрыта на компьютере {workstation.name}")
                A.R.every(workstation_list, every_action)
            except NotFound as error:
                self.output.error(error.get_details())
                search_value = None

    def process_kill(self, host_name: str, process_name: str) -> None:
        try:
            workstation_list: Result[list[Workstation]] = A.R_WS.by_any(host_name or self.input.input("Введите запрос для поиска компьютера"))
            def every_action(workstation: Workstation, process_name: str) -> None:
                process_value: int | str = process_name
                try:
                    process_value = int(process_value)
                except ValueError:
                    pass
                if A.A_WS.kill_process(process_value, workstation.name):
                    self.output.good(A.D.if_check(isinstance(process_value, str), f"Процесс с именем \"{process_value}\"", f"Программа с идентификационным номером {process_value}") + f"закрыта на компьютере {workstation.name}")
                else:
                    self.output.error("Процесс не найден")
            A.R.every(workstation_list, lambda workstation: every_action(workstation, process_name or self.input.input("Введите название процесса или его PID")))
        except NotFound as error:
            self.output.error(error.get_details())
            host_name = None

       
    @property
    def output(self) -> Output:
        return self.pih.output

    @property
    def input(self) -> Input:
        return self.pih.input

    def send_whatsapp_message(self, telephone_number: str, message: str) -> bool:
        return A.ME_WH_W.send(telephone_number, message, CONST.MESSAGE.WHATSAPP.WAPPI.PROFILE.IT)

    def mark_find(self, value: str | None = None) -> None:
        self.output.mark.by_any(value or self.input.mark.any())

    def arg(self, index: int = 0, default_value: Any = None) -> Any:
        return self.session.arg(index, default_value)

    def register_ct_indications(self) -> None:
        text: str = f"число, которое может содержать дробную часть разделенную {self.bold('точкой')} или {self.bold('запятой')}"
        number_format_notification_text: str = f"- {self.italic(text)}"
        def float_check_function(value: str | None, show_error: bool = True) -> str | None:
            result: float | None = None
            if value is not None:
                result = A.D_E.float(value)
            if show_error and result is None:
                self.output.error(
                    f"Введите {self.bold('число')} {number_format_notification_text}")
            return None if result is None else str(result)
        temperature: float = float_check_function(self.arg(), False) or self.input.input(
            f"Введите значение {self.bold('температуры')} {number_format_notification_text}", check_function=float_check_function)
        humidity: float = float_check_function(self.arg(1), False) or self.input.input(
            f"Введите значение {self.bold('влажности')} {number_format_notification_text}", check_function=float_check_function)
        indications_value: CTIndicationsValue = CTIndicationsValue(temperature, humidity)
        if A.A_I_CT.register(indications_value):
            with self.output.send_to_group(CONST.MESSAGE.WHATSAPP.GROUP.CT_INDICATIONS):
                self.output.write_result(
                    Result(FIELD_COLLECTION.INDICATIONS.CT_VALUE, indications_value), title=f"{self.get_formatted_given_name()}, отправил следующие показания в помещение КТ:")
            self.output.good("Спасибо, показания отправлены")

    def find_free_mark(self, value: str = None) -> None:
        self.output.mark.result(A.R_M.by_any(
            value or self.input.mark.any()), "Список свободных карт доступа:")

    def find_user(self, value: str = None) -> None:
        try:
            result: Result[list[User]] = A.R_U.by_any(
                value or self.input.user.title_any())
        except NotFound as error:
            self.output.error(error.get_details())
        else:
            self.output.user.result(result, "Пользователи:")

    def create_password(self) -> str:
        password: str = None
        password_settings: PasswordSettings = PASSWORD.get(self.input.indexed_field_list(
            "Выберите тип пароля", FIELD_COLLECTION.POLICY.PASSWORD_TYPE))
        while True:
            password = self.input.user.generate_password(
                True, password_settings)
            self.output.value("Пароль", password)
            if self.input.yes_no("Использовать", True):
                break
        if self.input.yes_no("Отправить в ИТ отдел"):
            A.L.it(f"Сгенерированный пароль:")
            A.L.it(password)
        return password

    def make_mark_as_free(self, value: str = None) -> None:
        mark: Mark = self.input.mark.by_any(value)
        mark_type: int = A.D.get(MarkType, mark.type)
        if mark_type == MarkType.FREE:
            self.output.error(
                "Карта доступа с введенным номером уже свободная")
        else:
            if self.input.yes_no("Сделать карту свободной"):
                if mark_type == MarkType.TEMPORARY:
                    temporary_tab_number: int = mark.TabNumber
                    mark = A.R_M.temporary_mark_owner(
                        mark).data
                if A.A_M.make_as_free_by_tab_number(mark.TabNumber):
                    if mark_type == MarkType.TEMPORARY:
                        A.E.it_notify_about_temporary_mark_return(
                            mark, temporary_tab_number)
                    else:
                        A.E.it_notify_about_mark_return(mark)
                    self.output.good(
                        f"Карта доступа с номером {mark.TabNumber} стала свободной")
                else:
                    self.output.error("Ошибка")
            else:
                self.output.error("Отмена")

    def who_lost_the_mark(self, tab_number: str = None):
        try:
            tab_number = tab_number or self.input.tab_number()
            if tab_number is not None:
                try:
                    mark: Mark = self.pih.RESULT.MARK.by_tab_number(
                        tab_number).data
                    mark_type: MarkType = A.D.get(MarkType, mark.type)
                    if mark_type == MarkType.FREE:
                        self.output.good("Это свободная карта доступа")
                    elif mark_type == MarkType.GUEST:
                        self.output.good("Это гостевая карта доступа")
                    else:
                        if mark_type == MarkType.TEMPORARY:
                            mark = self.pih.RESULT.MARK.temporary_mark_owner(
                                mark).data
                            tab_number = mark.TabNumber
                            self.output.good("Это временная карта доступа")
                        if mark is not None:
                            telephone_number: str = mark.telephoneNumber
                            self.output.value("Персона", mark.FullName)
                            if not self.pih.CHECK.telephone_number(telephone_number):
                                user: User = A.R_U.by_tab_number(
                                    tab_number).data
                                if user is not None:
                                    telephone_number = user.telephoneNumber
                            if not self.pih.CHECK.telephone_number(telephone_number):
                                self.output.error(f"Телефон не указан")
                            else:
                                self.output.value(
                                    "Телефон", telephone_number)
                                if self.input.yes_no("Отправить сообщение", True):
                                    details: str = self.input.input(
                                        f"{self.get_formatted_given_name()}, уточните, где забрать найденную карту")
                                    if self.send_whatsapp_message(
                                            telephone_number, f"День добрый, {A.D.to_given_name(mark.FullName)}, вашу карту доступа ({tab_number}) нашли, заберите ее {details}"):
                                        self.output.good(
                                            "Сообщение отправлено")
                                    else:
                                        self.output.error(
                                            "Ошибка при отправке сообщения")
                        else:
                            self.output.error("Телефон не указан")
                except NotFound:
                    self.output.error(
                        "Карта доступа, с введенным номером не найдена")
        except KeyboardInterrupt:
            pass

    def bold(self, value: str) -> str:
        return self.output.bold(value)

    def italic(self, value: str) -> str:
        return self.output.italic(value)

    def run_command(self, command_list: list[str] = None) -> None:
        default_host: str = CONST.HOST.DC2.NAME
        host: str = None
        def get_command_list() -> list[str]:
            command_list: tuple[list[str], list[str]] = A.D.dequotes(
                self.pih.input.input("Введите команду"))
            return list(filter(lambda item: not A.D_C.empty(item), command_list[0] + command_list[1]))
        command_list = command_list or get_command_list()
        use_psexec: bool = A.D_C.empty([value for value in list(map(
            lambda item: item.lower(), command_list)) if value in CONST.PSTOOLS.COMMAND_LIST])
        result: CompletedProcess = None
        if use_psexec:
            if A.D_C.empty(host):
                if self.input.yes_no(f"Использовать хост {self.bold(default_host)}, для выполнения команды", no_label=f"{self.bold('Или введите название хоста')}"):
                    host = default_host
                else:
                    host = self.input.answer
            while True:
                host = host.lower()
                if A.C_R.accessibility_by_ping(host, count=1):
                    self.output.write_line(
                        f"Команда будет запущена на хосте {self.bold(host)}\n")
                    break
                else:
                    self.output.error(f"Хост {self.bold(host)} не доступен")
                    host = self.input.input(
                        "Введите имя хоста, на котором будет выполнена команда")
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.PS.execute_command_list(A.PS.create_command_list_for_psexec_command(
                command_list, host, interactive=True, run_from_system_account=True, run_with_elevetion=True), True, True)
        else:
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.PS.execute_command_list(
                A.PS.create_command_list_for_pstools_command(command_list[0], command_list[1:]), True, True)
        result_out: str = result.stdout
        if not A.D_C.empty(result_out):
            self.output.write_line(result_out)
        if result.returncode != 0:
            error: str = result.stderr
            self.output.write_line(error)

    def create_new_mark(self):

        self.full_name = None
        self.tab_number = None
        self.telephone_number = None
        self.division_id = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполните ФИО персоны")
            self.full_name = self.input.full_name(True)
            user_exists: bool = not self.pih.CHECK.MARK.exists_by_full_name(
                self.full_name)
            if user_exists:
                self.output.error(
                    "Персона с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО персоны", A.D.fullname_to_string(self.full_name))

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполните номер телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_tab_number() -> ActionValue:
            self.output.header("Выбор группы и номера для карты доступа")
            free_mark: Mark = self.input.mark.free()
            group_name: str = free_mark.GroupName
            self.tab_number = free_mark.TabNumber
            self.output.value("Группа карты доступа", group_name)
            return self.output.get_action_value("Номер карты пропуска", self.tab_number)

        def get_division() -> ActionValue:
            self.output.header("Выбор подразделения")
            person_division: MarkDivision = self.input.mark.person_division()
            self.division_id = person_division.id
            return self.output.get_action_value("Подразделение, к которому прикреплена персона", person_division.name)

        ActionStack("Данные пользователя",
                    get_full_name,
                    get_division,
                    get_telephone_number,
                    get_tab_number,
                    input=self.input,
                    output=self.output
                    )
        if self.input.yes_no("Создать карту доступа для персоны", True):
            if self.pih.ACTION.MARK.create(self.full_name, self.division_id, self.tab_number, self.telephone_number):
                self.output.good("Карты доступа создана!")
                self.pih.EVENT.it_notify_about_create_new_mark(
                    self.full_name)
                if self.input.yes_no("Уведомить персону", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, Вам выдана карта доступа с номером {self.tab_number}")
            else:
                self.output.error("Карта доступа не создана!")

    def send_workstation_message_to_all(self) -> None:
        message: str = self.input.message(
            f"{self.get_formatted_given_name()}, введите сообщение для всех пользователей")
        A.ME_WS.to_all_workstations(
            message, None, [CONST.HOST.WS255], self.session)

    @property
    def user(self) -> User:
        return self.session.user

    @property
    def user_description(self) -> str:
        return A.D_F.description(self.user.description)

    def send_workstation_message(self, recipient_name: str = None, message: str | None = None, ask_for_use_dialog: bool = True) -> None:
        recipient: User | WorkstationDescription = None
        while True:
            try:
                recipient = A.D.get_first_item(
                    self.input.user.by_any(recipient_name, True))
                if recipient is not None:
                    break
            except NotFound as error:
                value: str = error.get_value()
                if A.C_WS.name(value):
                    if A.C_WS.exists(value):
                        recipient = A.R_WS.by_name(value).data
                        break
                if recipient is None:
                    recipient_name = None
                    self.output.error(error.get_details())
        if isinstance(recipient, User) and A.R.is_empty(A.R_WS.by_login(recipient.samAccountName)):
            self.output.error(
                f"Пользователь {recipient.name} ({recipient.samAccountName}) не залогинен ни за одним компьютером.")
        else:
            try:
                use_dialog: bool = False
                if ask_for_use_dialog:
                    use_dialog = A.D_C.empty(message) and self.input.yes_no("Начать диалог")
                else:
                    use_dialog = True
                while True:
                    user_given_name: str = self.get_formatted_given_name(self.user_given_name)
                    if isinstance(recipient, User):
                        message = message or self.input.message(
                            f"{user_given_name}, введите сообщение для пользователя {self.get_formatted_given_name(A.D.to_given_name(recipient))}", f"Сообщение от {self.user_given_name} ({self.user_description}): {A.D.to_given_name(recipient)}, ")
                        if A.ME_WS.to_user(recipient, message):
                            self.output.good("Сообщение отправлено")
                    else:
                        message =  message or self.input.message(
                            f"{user_given_name}, введите сообщение для компьютера {recipient.name}", f"Сообщение от {self.user_given_name} ({self.user_description}): ")
                        if A.ME_WS.to_workstation(recipient, message):
                            self.output.good("Сообщение отправлено")
                            message = None
                    if use_dialog:
                        self.output.separated_line()
                    else:
                        break
            except KeyboardInterrupt:
                if use_dialog:
                    self.output.error("Выход из диалога...")
                else:
                    self.output.error("Отмена...")

    @property
    def user_given_name(self) -> str:
        return self.session.user_given_name
    
    def get_formatted_given_name(self, value: str | None = None) -> str:
        return self.output.user.get_formatted_given_name(value or self.user_given_name)

    def create_temporary_mark(self, owner_mark: Mark = None) -> None:
        owner_mark = owner_mark or self.input.mark.by_any()
        mark_group: MarkGroup = None
        if self.input.yes_no("Выдать временную карту доступа из той же группы доступа"):
            mark_group = owner_mark
        temporary_mark: Mark = self.input.mark.free(mark_group)
        self.output.temporary_candidate_for_mark(temporary_mark)
        full_name: str = owner_mark.FullName
        tab_number: str = temporary_mark.TabNumber
        if self.input.yes_no(f"Создать временную карту для {full_name} с табельным номеров {tab_number}", True):
            if A.A_M.make_as_temporary(temporary_mark, owner_mark):
                self.output.good("Временная карта создана")
                telephone_number: str = owner_mark.telephoneNumber
                A.Eit_notify_about_create_temporary_mark(
                    full_name, tab_number)
                if not A.C.telephone_number(telephone_number):
                    user: User = A.R.get_first_element(A.R_U.by_any(
                        owner_mark))
                    if user is not None:
                        telephone_number = user.telephoneNumber
                if A.C.telephone_number(telephone_number):
                    if self.input.yes_no("Уведомить персону", True):
                        self.send_whatsapp_message(
                            telephone_number, f"Сообщение от ИТ отдела: День добрый, {self.get_formatted_given_name(full_name)}, Вам выдана временная карта доступа с номером {tab_number}")
            else:
                self.output.error("Ошибка при создании временной карты")
        else:
            self.output.error("Отмена")

    def telephone_number_fix_action(self, user: User) -> None:
        try:
            telephone: str = self.input.telephone_number()
            if A.A_U.set_telephone_number(user, telephone):
                self.output.good("Сохранен")
                self.output.line()
            else:
                self.output.error("Ошибка")
        except KeyboardInterrupt:
            self.output.new_line()
            self.output.error("Отмена")
            self.output.new_line()

    def start_user_telephone_number_editor(self) -> None:
        only_empty_telephone_number_edit: bool = self.input.yes_no(
            "Редактировать только телефоны, которые не заданы", True)
        result: Result[list[User]] = A.R_U.all(True)
        for user in result.data:
            user: User = user
            if A.C_U.user(user):
                if user.telephoneNumber is None:
                    self.output.error(f"{user.name}: нет телефона")
                    self.telephone_number_fix_action(user)
                elif not A.C.telephone_number(user.telephoneNumber):
                    fixed_telephone: str = A.D_F.telephone_number(
                        user.telephoneNumber)
                    if A.C.telephone_number(fixed_telephone):
                        self.output.good(f"{user.name} телефон исправлен")
                        A.A_U.set_telephone_number(
                            user, fixed_telephone)
                    else:
                        self.output.yellow(
                            f"{user.name}: неправильный формат телефона ({user.telephoneNumber})")
                else:
                    if not only_empty_telephone_number_edit:
                        self.output.good(
                            f"{user.name}: телефон присутствует")
                        self.telephone_number_fix_action(user)
            else:
                self.output.notify(
                    f"{user.name}, похоже не пользователь, у которого должен быть номер телефона")

    def start_user_property_setter(self, property_name: str, search_value: str = None, choose_user: bool = False) -> None:
        try:
            user_list: list[User] = None
            fields: FieldItemList = FIELD_COLLECTION.AD.USER
            active: bool | None = True if (
                property_name == USER_PROPERTIES.PASSWORD or property_name == USER_PROPERTIES.TELEPHONE_NUMBER) else None
            if choose_user:
                user_list = self.input.user.by_any(search_value, active)
            else:
                result: Result[list[User]] = A.R_U.by_any(
                    self.input.user.title_any(), active)
                user_list = result.data
            if property_name == USER_PROPERTIES.USER_STATUS:
                for status in [AD.ACTIVE_USERS_CONTAINER_DN, AD.INACTIVE_USERS_CONTAINER_DN]:
                    work_user_list: list[User] = self.pih.DATA.FILTER.users_by_dn(
                        user_list, AD.INACTIVE_USERS_CONTAINER_DN if status == AD.ACTIVE_USERS_CONTAINER_DN else AD.ACTIVE_USERS_CONTAINER_DN)
                    for index, user in enumerate(work_user_list):
                        try:
                            self.output.user.result(Result(fields, [user]))
                            if self.input.yes_no(f"{'Активировать' if status == AD.ACTIVE_USERS_CONTAINER_DN else 'Деактивировать' } пользователя"):
                                if status == AD.ACTIVE_USERS_CONTAINER_DN:
                                    if self.input.yes_no("Использовать шаблон для пользователя", True):
                                        user_container = self.input.user.template()
                                    else:
                                        user_container = self.input.user.container()
                                else:
                                    user_container = UserBase(
                                        distinguishedName=AD.INACTIVE_USERS_CONTAINER_DN)
                                if self.pih.ACTION.USER.set_status(user, status, user_container):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.new_line()
                                self.output.error("Отмена")
                        except KeyboardInterrupt:
                            self.output.new_line()
                            if index == len(user_list) - 1:
                                self.output.error("Отмена")
                            else:
                                self.output.error("Отмена - следующий")
                            self.output.new_line()
            else:
                for index, user in enumerate(user_list):
                    try:
                        if property_name == USER_PROPERTIES.TELEPHONE_NUMBER:
                            self.output.user.result(
                                Result(fields, [user]), None)
                            telephone = self.input.telephone_number()
                            if self.pih.CHECK.telephone_number(telephone) and self.input.yes_no("Установить", True):
                                if self.pih.ACTION.USER.set_telephone_number(user, telephone):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                        elif property_name == USER_PROPERTIES.PASSWORD:
                            self.output.user.result(
                                Result(fields, [user]), "Пользователи:")
                            password: str = None
                            while True:
                                password = self.input.user.generate_password(True, PASSWORD.get(
                                    self.input.indexed_field_list("Выберите тип пароля", FIELD_COLLECTION.POLICY.PASSWORD_TYPE)))
                                self.output.value("Пароль", password)
                                if self.input.yes_no("Использовать", True):
                                    break
                            if self.input.yes_no("Установить", True):
                                if self.pih.ACTION.USER.set_password(user, password):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                    except KeyboardInterrupt:
                        self.output.new_line()
                        self.output.error(
                            "Отмена" + (" - следующий" if index != len(user_list) - 1 else ""))
                        self.output.new_line()
        except NotFound as error:
            self.output.error(error.get_details())

    @property
    def session(self) -> Session:
        return self.pih.session

    def create_new_user(self) -> None:

        self.full_name = None
        self.tab_number = None
        self.telephone_number = None
        self.division_id = None
        self.user_is_exists = False
        self.login = None
        self.password = None
        self.internal_email = None
        self.external_email = None
        self.email_password = None
        self.polibase_login = None
        self.polibase_password = None
        self.user_container = None
        self.description = None
        self.use_template_user = None
        self.need_to_create_mark = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполнение ФИО пользователя")
            self.full_name = self.input.full_name(True)
            self.user_is_exists = self.pih.CHECK.USER.exists_by_full_name(
                self.full_name)
            if self.user_is_exists:
                self.output.error(
                    "Пользователем с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО пользователя", A.D.fullname_to_string(self.full_name))

        def get_login() -> ActionValue:
            self.output.header("Создание логина для аккаунта пользователя")
            self.login = self.input.user.generate_login(self.full_name)
            return self.output.get_action_value("Логин пользователя", self.login)

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполнение номера телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_description() -> ActionValue:
            self.output.header("Заполнение описания пользователя")
            self.description = self.input.description()
            return self.output.get_action_value("Описание", self.description, False)

        def get_template_user_container_or_user_container() -> ActionValue:
            self.output.header("Выбор контейнера для пользователя")
            if self.input.yes_no("Использовать шаблон для создания аккаунта пользователя", True):
                self.user_container, self.use_template_user = (
                    self.input.user.template(), True)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.description)
            else:
                self.user_container, self.use_template_user = (
                    self.input.user.container(), False)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.distinguishedName)

        def get_pc_password() -> ActionValue:
            self.output.header("Создание пароля для аккаунта пользователя")
            self.password = self.input.user.generate_password(
                settings=PASSWORD.SETTINGS.PC)
            return self.output.get_action_value("Пароль", self.password, False)

        def get_internal_email() -> ActionValue:
            self.output.header("Создание корпоративной электронной почты")
            if self.input.yes_no("Создать", True):
                self.internal_email = A.D_F.email(self.login, add_default_domain = True)
            return self.output.get_action_value("Адресс корпоративной электронной почты пользователя", self.internal_email)

        def get_email_password() -> ActionValue:
            if self.internal_email:
                self.output.header(
                    "Создание пароля для корпоротивной электронной почты")
                if self.input.yes_no("Использовать пароль от аккаунта пользователя", True):
                    self.email_password = self.password
                else:
                    self.email_password = self.input.user.generate_password(
                        settings=PASSWORD.SETTINGS.EMAIL)
                return self.output.get_action_value("Пароль электронной почты",  self.email_password, False)
            return None

        def get_external_email() -> ActionValue:
            self.output.header("Добавление внешней почты")
            if self.input.yes_no("Добавить"):
                self.external_email = self.input.email()
            return self.output.get_action_value("Адресс внешней электронной почты пользователя", self.external_email if self.external_email else "Нет", False)

        def get_division() -> ActionValue:
            full_name_string: str = A.D.fullname_to_string(self.full_name)
            mark: Mark = self.pih.RESULT.MARK.by_name(
                full_name_string, True).data
            if mark is not None:
                if self.input.yes_no(
                        f"Найдена карта доступа для персоны {full_name_string} с номером {mark.TabNumber}. Использовать", True):
                    self.need_to_create_mark = False
                    return None
            self.need_to_create_mark = self.input.yes_no(
                f"Создать карту доступа для персоны '{full_name_string}'", True)
            if self.need_to_create_mark:
                self.output.header("Выбор подразделения")
                person_division: MarkDivision = self.input.mark.person_division()
                self.division_id = person_division.id
                return self.output.get_action_value("Подразделение персоны, которой принадлежит карта доступа", person_division.name)
            return None

        def get_tab_number() -> ActionValue:
            if self.need_to_create_mark:
                self.output.header("Создание карты доступа")
                free_mark: Mark = self.input.mark.free()
                group_name: str = free_mark.GroupName
                self.tab_number = free_mark.TabNumber
                self.output.value("Группа карты доступа", group_name)
                return self.output.get_action_value("Номер карты доступа", self.tab_number)
            return None

        ActionStack(
            "Данные пользователя",
            get_full_name,
            get_login,
            get_telephone_number,
            get_description,
            get_template_user_container_or_user_container,
            get_pc_password,
            get_internal_email,
            get_email_password,
            get_external_email,
            get_division,
            get_tab_number,
            input=self.input,
            output=self.output
        )
        polibase_login: str = self.login
        polibase_password: str = self.password
        if self.input.yes_no("Создать аккаунт для пользователя", True):
            if self.use_template_user:
                self.pih.ACTION.USER.create_from_template(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            else:
                self.pih.ACTION.USER.create_in_container(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            if self.need_to_create_mark:
                self.tab_number = self.tab_number or self.pih.RESULT.MARK.by_name(
                    A.D.fullname_to_string(self.full_name), True).data.TabNumber
                self.pih.ACTION.MARK.create(
                    self.full_name, self.division_id, self.tab_number, self.telephone_number)
            user_account_document_path: str = self.pih.PATH.USER.get_document_name(
                A.D.fullname_to_string(self.full_name), self.login if self.user_is_exists else None)
            if self.pih.ACTION.DOCUMENTS.create_for_user(user_account_document_path, self.full_name, self.tab_number, LoginPasswordPair(self.login, self.password), LoginPasswordPair(
                    polibase_login, polibase_password), LoginPasswordPair(self.internal_email, self.email_password)):
                self.pih.EVENT.hr_notify_about_new_employee(self.login)
                self.pih.EVENT.it_notify_about_user_creation(
                    self.login, self.password)
                if self.need_to_create_mark:
                    self.pih.EVENT.it_notify_about_create_new_mark(
                        self.full_name)
                if self.input.yes_no("Сообщить пользователю о создании документов", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, Вас ожидает документы и карта доступа с номером {self.tab_number} в отделе")
                if self.input.yes_no("Отправить пользователю данные об аккаунте", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, данные Вашего аккаунта:\nЛогин: {self.login}\nПароль: {self.password}\nЭлектронная почта: {self.internal_email}")
