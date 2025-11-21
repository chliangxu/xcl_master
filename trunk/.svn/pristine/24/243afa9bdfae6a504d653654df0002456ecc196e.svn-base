import subprocess
import os
import sys
from src.modules.tools.model.tool_models import Tool
from src.core.log import LogSystem


class ToolLauncher:
    def __init__(self):
        self.running_processes = {}
        self.logger = LogSystem()

    def launch_tool(self, tool: Tool) -> bool:
        try:
            if not os.path.exists(tool.executable_path):
                self.logger.warning(f"工具可执行文件不存在: {tool.executable_path}")
                return self._launch_placeholder(tool)

            if sys.platform == "win32":
                process = subprocess.Popen([tool.executable_path], shell=True,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen([tool.executable_path],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.running_processes[tool.id] = process
            self.logger.info(f"成功启动工具: {tool.name}")
            return True
        except Exception as e:
            self.logger.error(f"启动工具失败 {tool.name}: {str(e)}")
            return self._launch_placeholder(tool)

    def _launch_placeholder(self, tool: Tool) -> bool:
        try:
            if sys.platform == "win32":
                subprocess.Popen(['notepad.exe'], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(['open', '-a', 'TextEdit'])
            else:
                subprocess.Popen(['gedit'])
            self.logger.info(f"启动占位符程序代替: {tool.name}")
            return True
        except Exception as e:
            self.logger.error(f"启动占位符程序失败: {str(e)}")
            return False

    def is_tool_running(self, tool_id: str) -> bool:
        if tool_id in self.running_processes:
            process = self.running_processes[tool_id]
            return process.poll() is None
        return False

    def stop_tool(self, tool_id: str) -> bool:
        if tool_id in self.running_processes:
            try:
                process = self.running_processes[tool_id]
                process.terminate()
                del self.running_processes[tool_id]
                self.logger.info(f"已停止工具: {tool_id}")
                return True
            except Exception as e:
                self.logger.error(f"停止工具失败: {str(e)}")
                return False
        return False

    def get_running_tools(self) -> list:
        running = []
        for tool_id, process in list(self.running_processes.items()):
            if process.poll() is None:
                running.append(tool_id)
            else:
                del self.running_processes[tool_id]
        return running
