from onnc.forest.core.options import Options
from onnc.forest.runtimes.openvino.runtime import OpenvinoOptions, OpenvinoSettings

def test_openvio_ir():
	# model = Model('resources/resnet18_openvino')
	options = Options('resources/resnet18_openvino')

	assert isinstance(options.settings, OpenvinoSettings)
	assert isinstance(options, OpenvinoOptions)

if __name__ == '__main__':
	test_openvio_ir()