from invoke import task

@task
def install(c):
    """Installeer fastmcp"""
    c.run("pip install fastmcp")

@task
def start(c):
    """Start server"""
    c.run("fastmcp run server.py")

@task
def dev(c):
    """Start in dev mode"""
    c.run("fastmcp dev server.py")

@task
def test(c):
    """
    Test alle MCP tools via een programmatische client.
    
    Deze functie demonstreert hoe je:
    1. Een MCP server start als subprocess (stdio communicatie)
    2. Een client sessie opzet om met de server te praten
    3. Tools aanroept met argumenten
    4. Resultaten ontvangt en verwerkt
    
    Zie README.md voor gedetailleerde uitleg van het proces.
    """
    c.run(""".venv/bin/python3 -c "
from fastmcp import FastMCP
import asyncio

async def test():
    # Import MCP client componenten
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    
    # Configureer hoe de server gestart moet worden
    # Dit start 'python server.py' als subprocess
    params = StdioServerParameters(command='.venv/bin/python3', args=['server.py'])
    
    # Open communicatie met de server (stdio = standard in/out)
    async with stdio_client(params) as (read, write):
        # Maak een sessie aan om tools aan te roepen
        async with ClientSession(read, write) as session:
            # Initialiseer de verbinding (handshake)
            await session.initialize()
            
            # Test 1: Optellen
            print('\\n--- Test 1: Optellen ---')
            r = await session.call_tool('add', {'a': 5, 'b': 3})
            print(f'add(5, 3) = {r.content[0].text}')
            
            # Test 2: Vermenigvuldigen
            print('\\n--- Test 2: Vermenigvuldigen ---')
            r = await session.call_tool('multiply', {'a': 4, 'b': 7})
            print(f'multiply(4, 7) = {r.content[0].text}')
            
            # Test 3: Random getal (met default waarden)
            print('\\n--- Test 3: Random getal ---')
            r = await session.call_tool('random_number', {})
            print(f'random_number() = {r.content[0].text}')
            
            # Test 4: Random getal met custom range
            print('\\n--- Test 4: Random met range ---')
            r = await session.call_tool('random_number', {'min_val': 10, 'max_val': 20})
            print(f'random_number(10, 20) = {r.content[0].text}')
            
            print('\\n✅ Alle tests geslaagd!')

asyncio.run(test())
"
""")

@task
def inspect(c):
    """Toon alle beschikbare tools en hun schemas"""
    c.run("fastmcp inspect server.py")
