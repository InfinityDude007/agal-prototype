import tensorflow as tf

if tf.test.is_built_with_cuda():
    print("TenserFlow GPU Usage: ✅")
else:
    print("TenserFlow GPU Usage: ❌  |  Expected: True  |  Got: ", tf.test.is_built_with_cuda())

if str(tf.config.experimental.list_physical_devices('GPU')) == "[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]":
    print("\nGPU Device: ✅")
else:
    print("\nGPU Device: ❌  |  Expected: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]  |  Got: ", tf.config.experimental.list_physical_devices('GPU'))

if tf.sysconfig.get_build_info()['cuda_version'] == "12.5.1":
    print("\nCUDA version: ✅")
else:
    print("\nCUDA version: ❌  |  Expected: 12.5.1  |  Got: ", tf.sysconfig.get_build_info()['cuda_version'])

if tf.sysconfig.get_build_info()['cudnn_version'] == "9":
    print("\ncuDNN version: ✅")
else:
    print("\ncuDNN version: ❌  |  Expected: 9  |  Got: ", tf.sysconfig.get_build_info()['cudnn_version'])
