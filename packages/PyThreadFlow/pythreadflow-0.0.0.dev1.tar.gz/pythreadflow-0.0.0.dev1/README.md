# PyThreadFlow V0.0.1.dev1

[skip to changes](https://github.com/nilonic/PyThreadFlow#changes)

PyThreadFlow is a Python threading extension that simplifies and enhances threading functionality by providing an init call, an event loop, and an exit call. These additions make multithreading in Python easier and more reliable.

## How can I download PyThreadFlow?

for the moment, you can download it using this command:

```bash
pip install -i https://test.pypi.org/simple/ PyThreadFlow==0.0.4.dev2
```

## How can I use PyThreadFlow?

To utilize PyThreadFlow, you can follow the example below:

```python
from pyThreadFlow.threadFlowManager import advthreads
# ...

t = advthreads.basicEventThread(mainLoop=main, openLoop=oloop, exitloop=eloop, daemon=True)

t.start()

# ...
```

In the code snippet above, you import the `advthreads` module from `pyThreadFlow.threadFlowManager` and instantiate a `Threads` object named `t`. The `Threads` object requires several parameters: `mainLoop`, `openLoop`, `exitloop`, and `daemon`. however there are some non-required parameters that speak for themselves. Once the object is created, you can call the `start()` method to initiate the thread execution.

PyThreadFlow aims to maintain a syntax similar to regular threads, and it tries to minimize the reliance on the base threading library. However, there are certain scenarios where using the base threading library becomes necessary.

## How can I contribute to PyThreadFlow?

If you are interested in contributing to PyThreadFlow, please refer to the official documentation [here](https://nilonic.github.io/PyThreadFlow/contributing.html) for detailed guidelines and instructions. The documentation provides information on how you can get involved and contribute to the project's development.

## Changes

1. **Added framework for legacy, deprecated, and more wrappers**: This update includes the addition of a framework that handles legacy, deprecated, and other types of wrappers. This framework allows for better management and organization of different types of wrappers within the system. By implementing this framework, it becomes easier to identify and handle code that needs to be phased out or replaced due to being outdated or no longer supported. It also facilitates the introduction of new wrappers or modifications to existing ones.

2. **Added framework for the thread multi-thread parts**: Another significant addition is the implementation of a framework specifically designed to handle the multi-threading aspects of the code. This framework provides the necessary structure and functionality to support multi-threaded operations within the application. While the framework has been implemented, the next step is to incorporate the appropriate callers that will utilize and interact with the multi-threading capabilities. Once these callers are added, the system will be able to effectively leverage multiple threads for concurrent execution, improving performance and efficiency.

3. **Added check in `__init__` so it can't be run directly**: A check has been introduced in the `__init__` function to prevent it from being executed directly. This modification ensures that the initialization process follows the correct procedure and is triggered through the appropriate mechanisms. By disallowing direct execution of the `__init__` function, potential errors or unintended consequences arising from manual invocations can be avoided. This check adds an extra layer of safety and helps maintain the integrity and stability of the codebase.

## TODOs

1. **Add functionality for the init, running, and exit calls for the threading flow manager**: The next task is to implement the necessary functionality for the initialization (`init`), running, and exit calls within the threading flow manager. This involves defining and integrating the required code to properly handle the initialization phase, manage the execution of threaded processes, and handle the clean-up and termination of threads upon program completion. Once these functionalities are in place, the threading flow manager will be able to orchestrate and control the multi-threading operations effectively.

2. **Find more bugs to report**: As an ongoing process of improving the system's reliability and performance, the task of identifying and reporting bugs remains a priority. By actively searching for and documenting any existing issues or glitches in the codebase, it becomes possible to address them systematically and enhance the overall quality of the software. This task involves thorough testing, debugging, and reporting of any anomalies or unexpected behaviors encountered during the development and usage of the application. By continuously striving to find and resolve bugs, the stability and user experience of the software can be significantly improved.
