import connexion
from flask import Response
from src.utils.format_reporting import FormatReporting
from src.utils.data_repository import DataRepository
from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.reports.report_factory import ReportFactory

app = connexion.FlaskApp(__name__)

manager = SettingsManager()
repository = DataRepository()
service = StartService(repository, manager)
service.create()


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    result = []
    for report in FormatReporting:
        result.append({"name": report.name, "value": report.value})

    return result


@app.route("/api/reports/<category>/<format>", methods=["GET"])
def get_report(category, format):
    data = {
        'nomenclature': repository.nomenclature_key(),
        'nomenclature_group': repository.nomenclature_group_key(),
        'measurement': repository.measurement_key(),
        'recipe': repository.recipe_key()
    }

    if category not in data:
        return Response("Указанная категория данных отсутствует!", 400)

    try:
        report_format = FormatReporting[format]
    except:
        return Response("Указанный формат отчёта отсутствует!", 400)

    report = ReportFactory(manager).create(report_format)
    report.create(repository.data[data[category]])

    return Response(report.result, 200)


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
