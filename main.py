import connexion
from flask import Response, request
from src.utils.format_reporting import FormatReporting
from src.utils.data_repository import DataRepository
from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.reports.report_factory import ReportFactory
from src.logics.domain_prototype import DomainPrototype
from src.dto.filter import FilterDTO

app = connexion.FlaskApp(__name__)

manager = SettingsManager()
repository = DataRepository()
service = StartService(repository, manager)
service.create()
data = {
    'nomenclature': repository.nomenclature_key(),
    'nomenclature_group': repository.nomenclature_group_key(),
    'measurement': repository.measurement_key(),
    'recipe': repository.recipe_key()
}


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
    report.create(repository.data[data[category]])

    return Response(report.result, 200)


@app.route("/api/filter/<domain>", methods=["POST"])
def filter_data(domain):
    if domain not in data:
        return Response("Указанная категория данных отсутствует!", 400)

    filter_data = request.get_json()
    try:
        filter = FilterDTO()
        filter.name = filter_data["name"]
        filter.id = filter_data["unique_code"]
        filter.type = filter_data["type"]
    except Exception as e:
        return Response(f"Ошибка параметров фильтрации: {e}!", 400)
    f_data = repository.data[data[domain]]
    if not f_data:
        return Response("В запрашиваемой категории нет данных!", 404)
    prototype = DomainPrototype(f_data)
    filtered_data = prototype.create(f_data, filter)
    if not filtered_data.data:
        return Response("Данных нет", 404)

    report = ReportFactory(manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)

    return report.result


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
