# import pytest

# from ai_assistant.integrations.mcp.client import MCPClient


# @pytest.mark.asyncio
# async def test_client_discovers_tools():

#     client = MCPClient(
#         command="python",
#         args=[
#             "-m",
#             "ai_assistant.mcp.server",
#         ],
#     )

#     try:
#         await client.connect()

#         tools = await client.list_tools()

#         names = {
#             tool.name
#             for tool in tools
#         }

#         assert "hello" in names
#         assert "search_documents" in names
#         assert "ask" in names

#     finally:
#         await client.close()


# @pytest.mark.asyncio
# async def test_client_calls_tool():

#     client = MCPClient(
#         command="python",
#         args=[
#             "-m",
#             "ai_assistant.mcp.server",
#         ],
#     )

#     try:
#         await client.connect()

#         result = await client.call_tool(
#             "hello",
#             {},
#         )

#         assert result.content

#     finally:
#         await client.close()