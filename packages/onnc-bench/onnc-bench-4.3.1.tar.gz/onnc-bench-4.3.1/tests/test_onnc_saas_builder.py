import os
import requests

from onnc.bench.core.compiler.onnc_saas import ONNCSaaSBuilder
from onnc.bench.core.compiler.saas_config import URI_MAP

# protocol = 'http'
# host = '127.0.0.1'
# port = 3000

protocol = 'https'
host = 'api.onnc.skymizer.com'
port = 443
SAAS_EMAIL = os.environ["SAAS_EMAIL"]
SAAS_PASSWORD = os.environ["SAAS_PASSWORD"]


def test_http_req():
    sb = ONNCSaaSBuilder(protocol, host, port)
    r = sb._http_req(sb.saas_login)
    assert isinstance(r, requests.models.Response)


def test_login():
    sb = ONNCSaaSBuilder(protocol, host, port)
    saas_res = sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    assert 'token' in saas_res.data
    assert saas_res.success is True


def test_create_project():
    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb.saas_create_project('test', info={})
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)
    assert saas_res.success
    assert 'id' in saas_res.data
    assert 'userId' in saas_res.data


def test_saas_get_project_id_by_name():
    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb.saas_get_project_id_by_name('test')
    assert len(saas_res.data) > 0
    assert 'id' in saas_res.data[0]
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)


def test_saas_upload_file():
    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb.saas_upload_file('resources/model.onnx')
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)
    assert saas_res.success
    assert "files" in saas_res.data
    assert len(saas_res.data["files"]) > 0

    assert "url" in saas_res.data["files"][0]
    assert "size" in saas_res.data["files"][0]


def test_saas_create_compilation():

    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb._saas_create_compilation(
        'resources/vww/models/model.h5',
        'resources/vww/samples/coco_11x96x96x3.npy')
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)

    assert "model" in saas_res
    assert "modelSize" in saas_res
    assert "calibration" in saas_res
    assert "calibrationSize" in saas_res
    assert "compilerParameters" in saas_res


def test_saas_create_build():

    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb.saas_create_build('0', [], 'test')
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)
    assert 'id' in saas_res.data
    assert 'projectId' in saas_res.data
    assert 'boardId' in saas_res.data
    assert 'state' in saas_res.data


def test_saas_get_build_state():
    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_build = sb.saas_create_build('0', [], 'test')
    build_id = saas_build.data["id"]
    saas_res = sb.saas_get_build_state(build_id)
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)
    assert 'id' in saas_res.data
    assert 'projectId' in saas_res.data
    assert 'boardId' in saas_res.data
    assert 'state' in saas_res.data


def test_saas_list_devices():
    sb = ONNCSaaSBuilder(protocol, host, port)
    sb.saas_login(SAAS_EMAIL, SAAS_PASSWORD)
    saas_res = sb.saas_list_devices()

    assert type(saas_res.data) is list
    assert len(saas_res.data) > 0
    # print(saas_res.success)
    # print(saas_res.message)
    # print(saas_res.data)


if __name__ == "__main__":
    test_create_project()
    test_saas_get_project_id_by_name()
    test_saas_upload_file()
    test_saas_create_compilation()
    test_saas_create_build()
    test_saas_get_build_state()
    test_saas_list_devices()
    test_saas_get_build_state()
