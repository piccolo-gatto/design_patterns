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


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    result = []
    for report in FormatReporting:
        result.append({"name": report.name, "value": report.value})

    return result


@app.route("/api/reports/<category>/<format>", methods=["GET"])
def get_report(category, format):
    if category not in data:
        return Response("Указанная категория данных отсутствует!", 400)

    try:
        report_format = FormatReporting[format]
    except:
        return Response("Указанный формат отчёта отсутствует!", 400)

    report = ReportFactory(manager).create(report_format)
    report.create(repository.data[category])

    return Response(report.result, 200)


@app.route("/api/filter/<domain>", methods=["POST"])
def filter_data(domain):
    if domain not in data:
        return Response("Указанная категория данных отсутствует!", 400)

    filter_data = request.get_json()
    filter = FilterDTO().from_dict(filter_data)
    f_data = repository.data[domain]
    if not f_data:
        return Response("В запрашиваемой категории нет данных!", 404)
    prototype = DomainPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    print(filtered_data.data)
    if not filtered_data.data:
        return Response("Данных нет", 404)

    report = ReportFactory(manager).create_default()
    report.create(filtered_data.data)

    return report.result

@app.route("/api/transactions", methods=["POST"])
def transactions():
    filter_data = request.get_json()
    filter = TransactionFilterDTO().from_dict(filter_data)
    f_data = repository.data['transaction']

    prototype = TransactionPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        return Response("Данных нет", 404)

    report = ReportFactory(manager).create_default()
    report.create(filtered_data.data)
    return report.result

@app.route("/api/turnovers", methods=["POST"])
def turnovers():
    filter_data = request.get_json()
    filter = TransactionFilterDTO().from_dict(filter_data)
    f_data = repository.data['transaction']

    prototype = TransactionPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        return Response("Данных нет", 404)

    process = WarehouseTurnoverProcess()
    process.block_period = manager.settings.block_period
    result = process.process(filtered_data.data)
    report = ReportFactory(manager).create_default()
    report.create(result)
    return report.result

@app.route("/api/block_period", methods=["GET"])
def block_period():
    return {"block_period": manager.settings.block_period}

@app.route("/api/new_block_period", methods=["POST"])
def new_block_period():
    new_block_period = request.get_json()["block_period"]
    manager.settings.block_period = new_block_period
    manager.save()
    return {"block_period": str(manager.settings.block_period)}

@app.route('/api/nomenclature/get', methods=['GET'])
def get_nomenclature():
    result = nomenclature_service.from_dict(request.json).get_nomenclature()
    report = ReportFactory(manager).create_default()
    report.create(list(result))
    return Response(report.result, 200)

@app.route('/api/nomenclature/add', methods=['PUT'])
def add_nomenclature():
    result = nomenclature_service.from_dict(request.json).add_nomenclature(request.json)
    report = ReportFactory(manager).create_default()
    report.create([result])
    return Response(report.result, 200)


@app.route('/api/nomenclature/update', methods=['PATCH'])
def update_nomenclature():
    statuses = ObserveService.raise_event(EventType.CHANGE_NOMENCLATURE, nomenclature_service.from_dict(request.json))
    status = statuses[type(NomenclatureService).__name__]
    return Response(status, 200)

@app.route('/api/nomenclature/delete', methods=['DELETE'])
def delete_nomenclature():
    statuses = ObserveService.raise_event(EventType.DELETE_NOMENCLATURE, nomenclature_service.from_dict(request.json))
    status = statuses[type(NomenclatureService).__name__]
    return Response(status, 200)

@app.route("/api/save_data", methods=["POST"])
def save_data():
    try:
        ObserveService.raise_event(EventType.SAVE_DATA, None)
        return Response("Данные успешно сохранены в файл!", 200)
    except Exception as e:
        return Response(str(e), 500)

@app.route("/api/load_data", methods=["POST"])
def load_data():
    try:
        ObserveService.raise_event(EventType.LOAD_DATA, None)
        return Response("Данные успешно загружены из файла!", 200)
    except Exception as e:
        return Response(str(e), 500)

@app.route("/api/tbs/<start_date>/<end_date>/<warehouse>", methods=["GET"])
def get_tbs_report(start_date, end_date, warehouse):
        if not start_date or not end_date or not warehouse:
            return Response("Необходимо указать 'Дата начала', 'Дата окончания' и 'Склад'.", status=400)
        if not transactions:
            return Response("Нет данных", 400)
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
            return Response("Данных нет", 404)
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
            return Response("Данных нет", 404)
        result_between = process.process(filtered_data.data)
        turnover_data = [result_before, result_between]

        report = ReportFactory(manager).create(FormatReporting.TBS)
        report.create(turnover_data)
        return Response(report.result, 200)

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
