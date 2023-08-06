from typing import Callable, Any
from sys import stderr

from je_auto_control.utils.exception.exception_tags import get_bad_trigger_method, get_bad_trigger_function
from je_auto_control.utils.exception.exceptions import CallbackExecutorException
# executor
from je_auto_control.utils.executor.action_executor import execute_action
from je_auto_control.utils.executor.action_executor import execute_files
# file process
from je_auto_control.utils.file_process.get_dir_file_list import get_dir_files_as_list
# html report
from je_auto_control.utils.generate_report.generate_html_report import generate_html
from je_auto_control.utils.generate_report.generate_html_report import generate_html_report
from je_auto_control.utils.generate_report.generate_json_report import generate_json
from je_auto_control.utils.generate_report.generate_json_report import generate_json_report
# xml
from je_auto_control.utils.generate_report.generate_xml_report import generate_xml
from je_auto_control.utils.generate_report.generate_xml_report import generate_xml_report
# utils image
from je_auto_control.utils.image.screenshot import pil_screenshot
# json
from je_auto_control.utils.json.json_file import read_action_json
from je_auto_control.utils.json.json_file import write_action_json
from je_auto_control.utils.package_manager.package_manager_class import \
    package_manager
from je_auto_control.utils.project.create_project_structure import create_project_dir
from je_auto_control.utils.shell_process.shell_exec import ShellManager
# socket server
from je_auto_control.utils.socket_server.auto_control_socket_server import start_autocontrol_socket_server
from je_auto_control.utils.start_exe.start_another_process import start_exe
# test record
from je_auto_control.utils.test_record.record_test_class import test_record_instance
# import image
from je_auto_control.wrapper.auto_control_image import locate_all_image
from je_auto_control.wrapper.auto_control_image import locate_and_click
from je_auto_control.wrapper.auto_control_image import locate_image_center
from je_auto_control.wrapper.auto_control_keyboard import check_key_is_press, get_special_table, get_keyboard_keys_table
from je_auto_control.wrapper.auto_control_keyboard import hotkey
# import keyboard
from je_auto_control.wrapper.auto_control_keyboard import press_keyboard_key
from je_auto_control.wrapper.auto_control_keyboard import release_keyboard_key
from je_auto_control.wrapper.auto_control_keyboard import type_keyboard
from je_auto_control.wrapper.auto_control_keyboard import write
# import mouse
from je_auto_control.wrapper.auto_control_mouse import click_mouse, get_mouse_table
from je_auto_control.wrapper.auto_control_mouse import get_mouse_position
from je_auto_control.wrapper.auto_control_mouse import mouse_scroll
from je_auto_control.wrapper.auto_control_mouse import press_mouse
from je_auto_control.wrapper.auto_control_mouse import release_mouse
from je_auto_control.wrapper.auto_control_mouse import set_mouse_position
# test_record
from je_auto_control.wrapper.auto_control_record import record
from je_auto_control.wrapper.auto_control_record import stop_record
# import screen
from je_auto_control.wrapper.auto_control_screen import screen_size
from je_auto_control.wrapper.auto_control_screen import screenshot


class CallbackFunctionExecutor(object):

    def __init__(self):
        self.event_dict: dict = {
            # mouse
            "mouse_left": click_mouse,
            "mouse_right": click_mouse,
            "mouse_middle": click_mouse,
            "click_mouse": click_mouse,
            "get_mouse_table": get_mouse_table,
            "get_mouse_position": get_mouse_position,
            "press_mouse": press_mouse,
            "release_mouse": release_mouse,
            "mouse_scroll": mouse_scroll,
            "set_mouse_position": set_mouse_position,
            "get_special_table": get_special_table,
            # keyboard
            "get_keyboard_keys_table": get_keyboard_keys_table,
            "type_keyboard": type_keyboard,
            "press_keyboard_key": press_keyboard_key,
            "release_keyboard_key": release_keyboard_key,
            "check_key_is_press": check_key_is_press,
            "write": write,
            "hotkey": hotkey,
            # image
            "locate_all_image": locate_all_image,
            "locate_image_center": locate_image_center,
            "locate_and_click": locate_and_click,
            # screen
            "screen_size": screen_size,
            "screenshot": screenshot,
            # test record
            "set_record_enable": test_record_instance.set_record_enable,
            # only generate
            "generate_html": generate_html,
            "generate_json": generate_json,
            "generate_xml": generate_xml,
            # generate report
            "generate_html_report": generate_html_report,
            "generate_json_report": generate_json_report,
            "generate_xml_report": generate_xml_report,
            # record
            "record": record,
            "stop_record": stop_record,
            # execute
            "execute_action": execute_action,
            "execute_files": execute_files,
            "create_template_dir": create_project_dir,
            "get_dir_files_as_list": get_dir_files_as_list,
            "pil_screenshot": pil_screenshot,
            "read_action_json": read_action_json,
            "write_action_json": write_action_json,
            "start_autocontrol_socket_server": start_autocontrol_socket_server,
            "add_package_to_executor": package_manager.add_package_to_executor,
            "add_package_to_callback_executor": package_manager.add_package_to_callback_executor,
            # project
            "create_project": create_project_dir,
            # Shell
            "shell_command": ShellManager().exec_shell,
            # Another process
            "execute_process": start_exe,
        }

    def callback_function(
            self,
            trigger_function_name: str,
            callback_function: Callable,
            callback_function_param: [dict, None] = None,
            callback_param_method: str = "kwargs",
            **kwargs
    ) -> Any:
        """
        :param trigger_function_name: what function we want to trigger only accept function in event_dict
        :param callback_function: what function we want to callback
        :param callback_function_param: callback function's param only accept dict 
        :param callback_param_method: what type param will use on callback function only accept kwargs and args
        :param kwargs: trigger_function's param
        :return: trigger_function_name return value
        """
        try:
            if trigger_function_name not in self.event_dict.keys():
                raise CallbackExecutorException(get_bad_trigger_function)
            execute_return_value = self.event_dict.get(trigger_function_name)(**kwargs)
            if callback_function_param is not None:
                if callback_param_method not in ["kwargs", "args"]:
                    raise CallbackExecutorException(get_bad_trigger_method)
                if callback_param_method == "kwargs":
                    callback_function(**callback_function_param)
                else:
                    callback_function(*callback_function_param)
            else:
                callback_function()
            return execute_return_value
        except Exception as error:
            print(repr(error), file=stderr)


callback_executor = CallbackFunctionExecutor()
package_manager.callback_executor = callback_executor
