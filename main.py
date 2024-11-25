import connexion
from flask import Response, request
from src.utils.format_reporting import FormatReporting
from src.utils.data_repository import DataRepository
from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.reports.report_factory import ReportFactory
from src.logics.domain_prototype import DomainPrototype
from src.dto.filter import FilterDTO
from src.logics.transaction_prototype import TransactionPrototype
from src.dto.transaction_filter import TransactionFilterDTO
from src.utils.nomenclature_service import NomenclatureService
from src.process.warehouse_turnover_process import WarehouseTurnoverProcess
from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.logger.logger import Logger
from src.process.process_factory import ProcessFactory
from src.utils.json_deserialization import JSONDeserialization
from src.utils.repository_manager import RepositoryManager

app = connexion.FlaskApp(__name__)

manager = SettingsManager()
repository = DataRepository()

repository_manager = RepositoryManager(repository, manager)
service = StartService(repository, manager, repository_manager)
service.create()
nomenclature_service = NomenclatureService(repository)
data = repository.data.keys()
logger = Logger(manager)


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/reports/formats GET")
    result = []
    for report in FormatReporting:
        result.append({"name": report.name, "value": report.value})
    ObserveService.raise_event(EventType.INFO_LOG, f"Список типов отчётов готов готов")
    ObserveService.raise_event(EventType.DEBUG_LOG, result)
    return result


@app.route("/api/reports/<category>/<format>", methods=["GET"])
def get_report(category, format):
    ObserveService.raise_event(EventType.DEBUG_LOG, f"/api/reports/{category}/{format} GET")
    if category not in data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Указанная категория данных отсутствует!")
        return Response("Указанная категория данных отсутствует!", 400)
    try:
        report_format = FormatReporting[format]
    except:
        ObserveService.raise_event(EventType.ERROR_LOG, "Указанный формат отчёта отсутствует!")
        return Response("Указанный формат отчёта отсутствует!", 400)

    report = ReportFactory(manager).create(report_format)
    report.create(repository.data[category])
    ObserveService.raise_event(EventType.INFO_LOG, f"Отчёт по {category} в формате {format} готов")
    ObserveService.raise_event(EventType.DEBUG_LOG, report_format)
    return Response(report.result, 200)


@app.route("/api/filter/<domain>", methods=["POST"])
def filter_data(domain):
    ObserveService.raise_event(EventType.DEBUG_LOG, f"/api/filter/{domain} POST")
    if domain not in data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Указанная категория данных отсутствует!")
        return Response("Указанная категория данных отсутствует!", 400)

    filter_data = request.get_json()
    filter = FilterDTO().from_dict(filter_data)
    f_data = repository.data[domain]
    if not f_data:
        ObserveService.raise_event(EventType.ERROR_LOG, "В запрашиваемой категории нет данных!")
        return Response("В запрашиваемой категории нет данных!", 404)
    prototype = DomainPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    print(filtered_data.data)
    if not filtered_data.data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данных нет")
        return Response("Данных нет", 404)

    report = ReportFactory(manager).create_default()
    report.create(filtered_data.data)
    ObserveService.raise_event(EventType.INFO_LOG, f"Отчёт по категории {domain} с применением фильтров готов")
    ObserveService.raise_event(EventType.DEBUG_LOG, report.result)
    return report.result

@app.route("/api/transactions", methods=["POST"])
def transactions():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/transactions POST")
    filter_data = request.get_json()
    filter = TransactionFilterDTO().from_dict(filter_data)
    f_data = repository.data['transaction']

    prototype = TransactionPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данных нет")
        return Response("Данных нет", 404)

    report = ReportFactory(manager).create_default()
    report.create(filtered_data.data)
    ObserveService.raise_event(EventType.INFO_LOG, "Отчёт о транзакциях сформирован")
    ObserveService.raise_event(EventType.ERROR_LOG, report.result)
    return report.result

@app.route("/api/turnovers", methods=["POST"])
def turnovers():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/turnovers POST")
    filter_data = request.get_json()
    filter = TransactionFilterDTO().from_dict(filter_data)
    f_data = repository.data['transaction']

    prototype = TransactionPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данных нет")
        return Response("Данных нет", 404)

    process = WarehouseTurnoverProcess()
    process.block_period = manager.settings.block_period
    result = process.process(filtered_data.data)
    report = ReportFactory(manager).create_default()
    report.create(result)
    ObserveService.raise_event(EventType.INFO_LOG, "Отчёт об оборотах сформирован")
    ObserveService.raise_event(EventType.DEBUG_LOG, report.result)
    return report.result

@app.route("/api/block_period", methods=["GET"])
def block_period():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/block_period GET")
    ObserveService.raise_event(EventType.INFO_LOG, f"Дата блокировки получена")
    ObserveService.raise_event(EventType.DEBUG_LOG, manager.settings.block_period)
    return {"block_period": manager.settings.block_period}

@app.route("/api/new_block_period", methods=["POST"])
def new_block_period():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/new_block_period POST")
    try:
        new_block_period = request.get_json()["block_period"]
        manager.settings.block_period = new_block_period
        manager.save()
        ObserveService.raise_event(EventType.INFO_LOG, "Дата блокировки обновлена")
        ObserveService.raise_event(EventType.DEBUG_LOG, manager.settings)
        return {"block_period": str(manager.settings.block_period)}
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 400)

@app.route('/api/nomenclature/get', methods=['GET'])
def get_nomenclature():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/nomenclature/get GET")
    try:
        result = nomenclature_service.from_dict(request.json).get_nomenclature()
        report = ReportFactory(manager).create_default()
        report.create(list(result))
        ObserveService.raise_event(EventType.INFO_LOG, f"Номенклатура {request.get_json()['unique_code']} получена")
        ObserveService.raise_event(EventType.DEBUG_LOG, report.result)
        return Response(report.result, 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 400)

@app.route('/api/nomenclature/add', methods=['PUT'])
def add_nomenclature():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/nomenclature/add PUT")
    try:
        result = nomenclature_service.from_dict(request.json).add_nomenclature(request.json)
        report = ReportFactory(manager).create_default()
        report.create([result])
        ObserveService.raise_event(EventType.INFO_LOG, f"Номенклатура {request.get_json()['name']} создана")
        ObserveService.raise_event(EventType.DEBUG_LOG, report.result)
        return Response(report.result, 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 400)


@app.route('/api/nomenclature/update', methods=['PATCH'])
def update_nomenclature():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/nomenclature/update PATCH")
    try:
        statuses = ObserveService.raise_event(EventType.CHANGE_NOMENCLATURE, nomenclature_service.from_dict(request.json))
        status = statuses[type(NomenclatureService).__name__]
        ObserveService.raise_event(EventType.INFO_LOG, f"Номенклатура {request.get_json()['unique_code']} обновлена")
        ObserveService.raise_event(EventType.DEBUG_LOG, status)
        return Response(status, 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 400)

@app.route('/api/nomenclature/delete', methods=['DELETE'])
def delete_nomenclature():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/nomenclature/delete DELETE")
    try:
        statuses = ObserveService.raise_event(EventType.DELETE_NOMENCLATURE, nomenclature_service.from_dict(request.json))
        status = statuses[type(NomenclatureService).__name__]
        ObserveService.raise_event(EventType.INFO_LOG, f"Номенклатура {request.get_json()['unique_code']} удалена")
        ObserveService.raise_event(EventType.DEBUG_LOG, status)
        return Response(status, 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 400)

@app.route("/api/save_data", methods=["POST"])
def save_data():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/save_data POST")
    try:
        ObserveService.raise_event(EventType.SAVE_DATA, None)
        ObserveService.raise_event(EventType.INFO_LOG, f"Данные успешно сохранены в файл")
        return Response("Данные успешно сохранены в файл!", 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 500)

@app.route("/api/load_data", methods=["POST"])
def load_data():
    ObserveService.raise_event(EventType.DEBUG_LOG, "/api/load_data POST")
    try:
        ObserveService.raise_event(EventType.LOAD_DATA, None)
        ObserveService.raise_event(EventType.INFO_LOG, f"Данные успешно загружены из файла")
        return Response("Данные успешно загружены из файла!", 200)
    except Exception as e:
        ObserveService.raise_event(EventType.ERROR_LOG, e)
        return Response(str(e), 500)

@app.route("/api/tbs/<start_date>/<end_date>/<warehouse>", methods=["GET"])
def get_tbs_report(start_date, end_date, warehouse):
    ObserveService.raise_event(EventType.DEBUG_LOG, f"/api/tbs/{start_date}/{end_date}/{warehouse} GET")
    if not start_date:
        ObserveService.raise_event(EventType.ERROR_LOG, "Укажите дату начала")
        return Response("Укажите дату начала", status=400)
    if not end_date:
        ObserveService.raise_event(EventType.ERROR_LOG, "Укажите дату конца")
        return Response("Укажите дату конца", status=400)
    if not warehouse:
        ObserveService.raise_event(EventType.ERROR_LOG, "Укажите склад")
        return Response("Укажите склад'.", status=400)
    if not transactions:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данные о транзакциях не найдены")
        return Response("Данные о транзакциях не найдены", 400)
    filter_before = {
            "warehouse": {
                "name": warehouse,
                "unique_code": "",
                "type": "equals"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "type": "equals"},
            "start_period": "1900-01-01",
            "end_period": start_date
    }
    filter = TransactionFilterDTO().from_dict(filter_before)
    f_data = repository.data['transaction']

    prototype = TransactionPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данные по фильтрам не найдены")
        return Response("Данные по фильтрам не найдены", 400)
    process = WarehouseTurnoverProcess()
    process.block_period = manager.settings.block_period
    result_before = process.process(filtered_data.data)
    filter_between = {
            "warehouse": {
                "name": warehouse,
                "unique_code": "",
                "type": "equals"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "type": "equals"},
            "start_period": start_date,
            "end_period": end_date
    }
    filter = TransactionFilterDTO().from_dict(filter_between)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        ObserveService.raise_event(EventType.ERROR_LOG, "Данные по фильтрам не найдены")
        return Response("Данные по фильтрам не найдены", 400)
    result_between = process.process(filtered_data.data)
    turnover_data = [result_before, result_between]

    report = ReportFactory(manager).create(FormatReporting.TBS)
    report.create(turnover_data)
    ObserveService.raise_event(EventType.INFO_LOG, "TBS-отчёт сформирован")
    ObserveService.raise_event(EventType.DEBUG_LOG, report.result)
    return Response(report.result, 200)

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
