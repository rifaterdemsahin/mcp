2025-06-03T20:49:56.931Z [demo-server] [info] Initializing server...
2025-06-03T20:49:56.958Z [demo-server] [info] Server started and connected successfully
2025-06-03T20:49:56.962Z [demo-server] [info] Message from client: {"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0}
  + Exception Group Traceback (most recent call last):
  |   File "C:\projects\mcp\mcp_server.py", line 206, in <module>
  |     asyncio.run(main())
  |     ~~~~~~~~~~~^^^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\runners.py", line 195, in run
  |     return runner.run(main)
  |            ~~~~~~~~~~^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\runners.py", line 118, in run
  |     return self._loop.run_until_complete(task)
  |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\base_events.py", line 719, in run_until_complete
  |     return future.result()
  |            ~~~~~~~~~~~~~^^
  |   File "C:\projects\mcp\mcp_server.py", line 191, in main
  |     async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
  |                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\contextlib.py", line 235, in __aexit__
  |     await self.gen.athrow(value)
  |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\stdio.py", line 87, in stdio_server
  |     async with anyio.create_task_group() as tg:
  |                ~~~~~~~~~~~~~~~~~~~~~~~^^
  |   File "C:\projects\mcp\mcp_env\Lib\site-packages\anyio\_backends\_asyncio.py", line 772, in __aexit__
  |     raise BaseExceptionGroup(
  |         "unhandled errors in a TaskGroup", self._exceptions
  |     ) from None
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\stdio.py", line 90, in stdio_server
    |     yield read_stream, write_stream
    |   File "C:\projects\mcp\mcp_server.py", line 198, in main
    |     capabilities=server.get_capabilities(
    |                  ~~~~~~~~~~~~~~~~~~~~~~~^
    |         notification_options={},  # Default empty dict for notification options
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |         experimental_capabilities={}  # Default empty dict for experimental capabilities
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |     ),
    |     ^
    |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\lowlevel\server.py", line 205, in get_capabilities
    |     listChanged=notification_options.tools_changed
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    | AttributeError: 'dict' object has no attribute 'tools_changed'
    +------------------------------------
2025-06-03T20:49:57.919Z [demo-server] [info] Server transport closed
2025-06-03T20:49:57.919Z [demo-server] [info] Client transport closed
2025-06-03T20:49:57.919Z [demo-server] [info] Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `console.error('...')` in JavaScript, `print('...', file=sys.stderr)` in python) and it will appear in this log.
2025-06-03T20:49:57.919Z [demo-server] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {"context":"connection"}
2025-06-03T20:49:57.920Z [demo-server] [info] Client transport closed


---

